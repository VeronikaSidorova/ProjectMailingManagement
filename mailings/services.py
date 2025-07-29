from django.conf import settings
from django.contrib import messages
from django.core.cache import cache
from django.shortcuts import get_object_or_404, redirect

from config.settings import CACHE_ENABLED
from .models import Campaign, Recipient, SendAttempt, SendLog, Message
from django.core.mail import send_mail


def send_campaign(campaign_id):
    """
    Отправляет сообщения по выбранной кампании.
    Создает запись SendAttempt и логирует каждое письмо в SendLog.
    """
    try:
        campaign = Campaign.objects.get(pk=campaign_id)
    except Campaign.DoesNotExist:
        raise ValueError(f"Рассылка с id={campaign_id} не найдена.")

    recipients = campaign.recipients.all()
    message = campaign.message

    # Создаем запись о попытке отправки
    send_attempt = SendAttempt.objects.create(
        campaign=campaign, status="Не успешно", server_response="Начало отправки"  # по умолчанию, обновим позже
    )

    all_successful = True  # флаг для итогового статуса

    for recipient in recipients:
        try:
            send_mail(
                subject=message.subject,
                message=message.body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[recipient.email],
            )
            campaign.status = "Запущена"
            campaign.save()
            # Логируем успешную отправку
            SendLog.objects.create(
                campaign=campaign,
                recipient=recipient,
                status="Успешно",
                server_response="Письмо успешно отправлено.",
            )
        except Exception as e:
            all_successful = False  # есть ошибка, значит не все успешно
            # Логируем ошибку
            SendLog.objects.create(
                campaign=campaign,
                recipient=recipient,
                status="Не успешно",
                server_response=str(e),
            )

    # Обновляем статус Attempt в зависимости от результата
    if all_successful:
        send_attempt.status = "Успешно"
        send_attempt.server_response = "Все письма успешно отправлены."
    else:
        send_attempt.status = "Не успешно"
        send_attempt.server_response = "Некоторые письма не были отправлены. Проверьте логи."

    send_attempt.save()


def manual_send_campaign(request, pk):
    campaign = get_object_or_404(Campaign, pk=pk)
    if campaign.status == "Завершена":
        messages.error(request, "Невозможно запустить рассылку, статус — завершена(заблокирована менеджером).")
        return redirect("mailings:campaign_detail", pk=pk)
    if request.method == "POST":
        # Запускаем отправку
        send_campaign(campaign.id)
        # Обновляем статус
        campaign.status = "Запущена"
        campaign.save()
        messages.success(request, "Рассылка успешно запущена вручную.")
        return redirect("mailings:campaign_detail", pk=pk)
    else:
        return redirect("mailings:campaign_detail", pk=pk)


def get_recipient_from_cache():
    if not CACHE_ENABLED:
        return Recipient.objects.all()
    key = "recipient_list"
    recipients = cache.get(key)
    if recipients is not None:
        return recipients
    recipients = Recipient.objects.all()
    cache.set(key, recipients)
    return recipients


def get_message_from_cache():
    if not CACHE_ENABLED:
        return Message.objects.all()
    key = "message_list"
    messagies = cache.get(key)
    if messagies is not None:
        return messagies
    messagies = Message.objects.all()
    cache.set(key, messagies)
    return messagies


def get_campaign_from_cache():
    if not CACHE_ENABLED:
        return Campaign.objects.all()
    key = "campaign_list"
    campaigns = cache.get(key)
    if campaigns is not None:
        return campaigns
    campaigns = Campaign.objects.all()
    cache.set(key, campaigns)
    return campaigns
