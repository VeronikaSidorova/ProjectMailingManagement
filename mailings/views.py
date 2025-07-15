from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    ListView,
    TemplateView,
    UpdateView,
)

from .models import Campaign, Message, Recipient, SendAttempt, SendLog
from .services import send_campaign


# Получатели
class RecipientListView(ListView):
    model = Recipient
    template_name = "recipient_list.html"


class RecipientCreateView(CreateView):
    model = Recipient
    fields = ["email", "full_name", "comment"]
    template_name = "recipient_form.html"
    success_url = reverse_lazy("recipient_list")


class RecipientUpdateView(UpdateView):
    model = Recipient
    fields = ["email", "full_name", "comment"]
    template_name = "recipient_form.html"
    success_url = reverse_lazy("recipient_list")


class RecipientDeleteView(DeleteView):
    model = Recipient
    template_name = "recipient_confirm_delete.html"
    success_url = reverse_lazy("recipient_list")


# Сообщения
class MessageListView(ListView):
    model = Message
    template_name = "message_list.html"


class MessageCreateView(CreateView):
    model = Message
    fields = ["subject", "body"]
    template_name = "message_form.html"
    success_url = reverse_lazy("message_list")


class MessageUpdateView(UpdateView):
    model = Message
    fields = ["subject", "body"]
    template_name = "message_form.html"
    success_url = reverse_lazy("message_list")


class MessageDeleteView(DeleteView):
    model = Message
    template_name = "message_confirm_delete.html"
    success_url = reverse_lazy("message_list")


# Рассылки
class CampaignListView(ListView):
    model = Campaign
    template_name = "campaign_list.html"


class CampaignCreateView(CreateView):
    model = Campaign
    fields = ["start_time", "end_time", "status", "message", "recipients"]

    template_name = "campaign_form.html"

    def get_success_url(self):
        return reverse_lazy("campaign_detail", kwargs={"pk": self.object.pk})


class CampaignUpdateView(UpdateView):
    model = Campaign
    fields = ["start_time", "end_time", "status", "message", "recipients"]

    template_name = "campaign_form.html"

    def get_success_url(self):
        return reverse_lazy("campaign_detail", kwargs={"pk": self.object.pk})


class CampaignDeleteView(DeleteView):
    model = Campaign
    template_name = "campaign_confirm_delete.html"

    success_url = reverse_lazy("campaign_list")


# Попытки отправки (обычно создаются автоматически при запуске рассылки)
class SendAttemptListView(ListView):
    model = SendAttempt
    template_name = "sendattempt_list.html"


class SendAttemptCreateView(CreateView):
    model = SendAttempt
    fields = ["campaign", "status", "server_response"]

    template_name = "sendattempt_form.html"

    def get_success_url(self):
        return reverse_lazy("sendattempt_detail", kwargs={"pk": self.object.pk})


class SendAttemptUpdateView(UpdateView):
    model = SendAttempt
    fields = ["campaign", "status", "server_response"]
    template_name = "sendattempt_form.html"

    def get_success_url(self):
        return reverse_lazy("sendattempt_detail", kwargs={"pk": self.object.pk})


class SendAttemptDeleteView(DeleteView):
    model = SendAttempt

    template_name = "sendattempt_confirm_delete.html"

    success_url = reverse_lazy("sendattempt_list")


# Логи отправки писем
class SendLogListView(ListView):
    model = SendLog
    template_name = "sendlog_list.html"


class SendLogCreateView(CreateView):
    model = SendLog
    fields = ["campaign", "recipient", "status", "server_response"]

    template_name = "sendlog_form.html"

    def get_success_url(self):
        return reverse_lazy("sendlog_detail", kwargs={"pk": self.object.pk})


class SendLogUpdateView(UpdateView):
    model = SendLog
    fields = ["campaign", "recipient", "status", "server_response"]

    template_name = "sendlog_form.html"

    def get_success_url(self):
        return reverse_lazy("sendlog_detail", kwargs={"pk": self.object.pk})


class SendLogDeleteView(DeleteView):
    model = SendLog

    template_name = "sendlog_confirm_delete.html"

    success_url = reverse_lazy("sendlog_list")


class DashboardView(TemplateView):
    template_name = "dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_campaigns"] = Campaign.objects.count()
        context["active_campaigns"] = Campaign.objects.filter(status="Запущена").count()
        context["unique_recipients"] = Recipient.objects.count()
        return context


def manual_send_campaign(request, pk):
    campaign = get_object_or_404(Campaign, pk=pk)
    try:
        send_campaign(campaign.id)
        messages.success(request, f"Рассылка '{campaign}' запущена вручную.")
    except Exception as e:
        messages.error(request, f"Ошибка при отправке: {e}")
    return redirect("campaign_detail", pk=pk)
