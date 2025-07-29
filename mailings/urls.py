from django.urls import path
from django.views.decorators.cache import cache_page

from mailings import services, views
from mailings.apps import MailingsConfig
from mailings.views import (
    CampaignCreateView,
    CampaignDeleteView,
    CampaignListView,
    CampaignUpdateView,
    DashboardView,
    MessageCreateView,
    MessageDeleteView,
    MessageListView,
    MessageUpdateView,
    RecipientCreateView,
    RecipientDeleteView,
    RecipientListView,
    RecipientUpdateView,
    RecipientDetailView,
    MessageDetailView,
    CampaignDetailView
)

app_name = MailingsConfig.name

urlpatterns = [
    path("", DashboardView.as_view(), name="dashboard"),

    path("recipients/", RecipientListView.as_view(), name="recipient_list"),
    path("recipients/add/", RecipientCreateView.as_view(), name="recipient_form"),
    path("recipients/<int:pk>/", cache_page(60)(RecipientDetailView.as_view()), name="recipient_detail"),
    path(
        "recipients/<int:pk>/edit/",
        RecipientUpdateView.as_view(),
        name="recipient_edit",
    ),
    path(
        "recipients/<int:pk>/delete/",
        RecipientDeleteView.as_view(),
        name="recipient_delete",
    ),

    path("messages/", MessageListView.as_view(), name="message_list"),
    path("messages/add/", MessageCreateView.as_view(), name="message_form"),
    path("messages/<int:pk>/", cache_page(60)(MessageDetailView.as_view()), name="message_detail"),
    path("messages/<int:pk>/edit/", MessageUpdateView.as_view(), name="message_edit"),
    path(
        "messages/<int:pk>/delete/", MessageDeleteView.as_view(), name="message_delete"
    ),

    path("campaigns/", CampaignListView.as_view(), name="campaign_list"),
    path("campaigns/add/", CampaignCreateView.as_view(), name="campaign_form"),
    path("campaigns/<int:pk>/", cache_page(60)(CampaignDetailView.as_view()), name="campaign_detail"),
    path(
        "campaigns/<int:pk>/edit/", CampaignUpdateView.as_view(), name="campaign_edit"
    ),
    path(
        "campaigns/<int:pk>/delete/",
        CampaignDeleteView.as_view(),
        name="campaign_delete",
    ),
    path("campaign/<int:pk>/send/", services.manual_send_campaign, name='manual_send_campaign'),

    path("statistics/", views.view_statistics, name="statistics"),
    path("statistics/<int:campaign_id>/", views.campaign_statistics_detail_view, name='campaign_statistics_detail'),
]
