from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Q
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    ListView,
    TemplateView,
    UpdateView, DetailView,
)

from .forms import CampaignForm
from .models import Campaign, Message, Recipient, SendAttempt
from .services import send_campaign, get_recipient_from_cache, get_message_from_cache, get_campaign_from_cache


# Получатели
class RecipientListView(ListView):
    model = Recipient
    template_name = "recipient_list.html"
    ordering = ['id']

    def get_queryset(self):
        recipients = get_recipient_from_cache()
        user = self.request.user
        if user.groups.filter(name='managers').exists():
            return recipients
        else:
            return recipients.filter(owner=user)


class RecipientCreateView(LoginRequiredMixin, CreateView):
    model = Recipient
    fields = ["email", "full_name", "comment"]
    template_name = "recipient_form.html"
    success_url = reverse_lazy("mailings:recipient_list")

    def form_valid(self, form):
        recipient = form.save()
        user = self.request.user
        recipient.owner = user
        recipient.save()
        response = super().form_valid(form)
        return response


class RecipientDetailView(LoginRequiredMixin, DetailView):
    model = Recipient
    template_name = "recipient_detail.html"
    context_object_name = "recipient"


class RecipientUpdateView(LoginRequiredMixin, UpdateView):
    model = Recipient
    fields = ["email", "full_name", "comment"]
    template_name = "recipient_form.html"
    success_url = reverse_lazy("mailings:recipient_list")


class RecipientDeleteView(DeleteView):
    model = Recipient
    template_name = "recipient_confirm_delete.html"
    success_url = reverse_lazy("mailings:recipient_list")


# Сообщения
class MessageListView(ListView):
    model = Message
    template_name = "message_list.html"
    ordering = ['id']

    def get_queryset(self):
        messagies = get_message_from_cache()
        user = self.request.user
        if user.groups.filter(name='managers').exists():
            return messagies
        else:
            return messagies.filter(owner=user)


class MessageCreateView(CreateView):
    model = Message
    fields = ["subject", "body"]
    template_name = "message_form.html"
    success_url = reverse_lazy("mailings:message_list")

    def form_valid(self, form):
        message = form.save()
        user = self.request.user
        message.owner = user
        message.save()
        response = super().form_valid(form)
        return response


class MessageDetailView(LoginRequiredMixin, DetailView):
    model = Message
    template_name = "message_detail.html"
    context_object_name = "message"


class MessageUpdateView(UpdateView):
    model = Message
    fields = ["subject", "body"]
    template_name = "message_form.html"
    success_url = reverse_lazy("mailings:message_list")


class MessageDeleteView(DeleteView):
    model = Message
    template_name = "message_confirm_delete.html"
    success_url = reverse_lazy("mailings:message_list")


# Рассылки
class CampaignListView(ListView):
    model = Campaign
    template_name = "campaign_list.html"
    ordering = ['id']

    def get_queryset(self):
        campaigns = get_campaign_from_cache()
        user = self.request.user
        if user.groups.filter(name='managers').exists():
            return campaigns
        else:
            return campaigns.filter(owner=user)


class CampaignCreateView(LoginRequiredMixin, CreateView):
    model = Campaign
    form_class = CampaignForm
    template_name = "campaign_form.html"

    def get_success_url(self):
        return reverse_lazy("mailings:campaign_detail", kwargs={"pk": self.object.pk})

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user  # передаем пользователя в форму
        return kwargs

    def form_valid(self, form):
        campaign = form.save(commit=False)
        campaign.owner = self.request.user  # назначаем владельца до сохранения
        campaign.save()
        form.save_m2m()
        return super().form_valid(form)


class CampaignDetailView(LoginRequiredMixin, DetailView):
    model = Campaign
    template_name = "campaign_detail.html"
    context_object_name = "campaign"


class CampaignUpdateView(UpdateView):
    model = Campaign
    form_class = CampaignForm

    template_name = "campaign_form.html"

    def get_success_url(self):
        return reverse_lazy("mailings:campaign_detail", kwargs={"pk": self.object.pk})

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user  # передаем пользователя в форму
        return kwargs

    def form_valid(self, form):
        campaign = form.save(commit=False)
        campaign.owner = self.request.user  # назначаем владельца до сохранения
        campaign.save()
        form.save_m2m()
        return super().form_valid(form)


class CampaignDeleteView(DeleteView):
    model = Campaign
    template_name = "campaign_confirm_delete.html"

    success_url = reverse_lazy("mailings:campaign_list")


class DashboardView(TemplateView):
    template_name = "dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_campaigns"] = Campaign.objects.count()
        context["active_campaigns"] = Campaign.objects.filter(status="Запущена").count()
        context["unique_recipients"] = Recipient.objects.count()
        return context


def view_statistics(campaign_id):
    campaigns_stats = Campaign.objects.annotate(
        total_sent=Count('sendattempt'),
        success_count=Count('sendattempt', filter=Q(sendattempt__status='Успешно')),
        failure_count=Count('sendattempt', filter=Q(sendattempt__status='Не успешно')),
    ).values('id', 'total_sent', 'success_count', 'failure_count')

    return render(request, 'statistics.html', {
        'campaigns_stats': campaigns_stats,
    })


def campaign_statistics_detail_view(request, campaign_id):
    campaign = get_object_or_404(Campaign, pk=campaign_id)
    stats = SendAttempt.objects.filter(campaign_id=campaign_id).values('status').annotate(count=Count('id'))

    result = {
        'total_sent': SendAttempt.objects.filter(campaign_id=campaign_id).count(),
        'success_count': next((item['count'] for item in stats if item['status'] == "Успешно"), 0),
        'failure_count': next((item['count'] for item in stats if item['status'] == "Не успешно"), 0),
    }

    return render(request, 'campaign_statistics_detail.html', {
        'campaign': campaign,
        'stats': result,
    })
