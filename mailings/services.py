from django.conf import settings
from django.core.mail import send_mail

from .models import Campaign, SendLog


def send_campaign(campaign_id):
    """
    Отправляет сообщения по выбранной кампании.
    Создает записи SendLog для каждого отправленного сообщения.
    """
    try:
        campaign = Campaign.objects.get(pk=campaign_id)
    except Campaign.DoesNotExist:
        raise ValueError(f"Кампания с id={campaign_id} не найдена.")

    recipients = campaign.recipients.all()
    message = campaign.message

    for recipient in recipients:
        try:
            send_mail(
                subject=message.subject,
                message=message.body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[recipient.email],
            )
            # Логируем успешную отправку
            SendLog.objects.create(
                campaign=campaign,
                recipient=recipient,
                status="sent",
            )
        except Exception as e:
            # Логируем ошибку
            SendLog.objects.create(
                campaign=campaign,
                recipient=recipient,
                status="failed",
                error=str(e),
            )
