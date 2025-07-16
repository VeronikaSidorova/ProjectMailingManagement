from django.urls import path

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
    SendAttemptCreateView,
    SendAttemptDeleteView,
    SendAttemptListView,
    SendAttemptUpdateView,
    SendLogCreateView,
    SendLogDeleteView,
    SendLogListView,
    SendLogUpdateView, RecipientDetailView,
)

app_name = MailingsConfig.name

urlpatterns = [
    path("", DashboardView.as_view(), name="dashboard"),
    path("recipients/", RecipientListView.as_view(), name="recipient_list"),
    path("recipients/add/", RecipientCreateView.as_view(), name="recipient_form"),
    path("recipients/<int:pk>/", RecipientDetailView.as_view(), name="recipient_detail"),
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
    path("messages/add/", MessageCreateView.as_view(), name="message_add"),
    path("messages/<int:pk>/edit/", MessageUpdateView.as_view(), name="message_edit"),
    path(
        "messages/<int:pk>/delete/", MessageDeleteView.as_view(), name="message_delete"
    ),

    path("campaigns/", CampaignListView.as_view(), name="campaign_list"),
    path("campaigns/add/", CampaignCreateView.as_view(), name="campaign_add"),
    path(
        "campaigns/<int:pk>/edit/", CampaignUpdateView.as_view(), name="campaign_edit"
    ),
    path(
        "campaigns/<int:pk>/delete/",
        CampaignDeleteView.as_view(),
        name="campaign_delete",
    ),

    path("sendattempts/", SendAttemptListView.as_view(), name="sendattempt_list"),
    path("sendattempts/add/", SendAttemptCreateView.as_view(), name="sendattempt_add"),
    path(
        "sendattempts/<int:pk>/edit/",
        SendAttemptUpdateView.as_view(),
        name="sendattempt_edit",
    ),
    path(
        "sendattempts/<int:pk>/delete/",
        SendAttemptDeleteView.as_view(),
        name="sendattempt_delete",
    ),

    path("sendlogs/", SendLogListView.as_view(), name="sendlog_list"),
    path("sendlogs/add/", SendLogCreateView.as_view(), name="sendlog_add"),
    path("sendlogs/<int:pk>/edit/", SendLogUpdateView.as_view(), name="sendlog_edit"),
    path(
        "sendlogs/<int:pk>/delete/", SendLogDeleteView.as_view(), name="sendlog_delete"
    ),
]
