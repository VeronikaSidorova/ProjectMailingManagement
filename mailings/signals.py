# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from .models import Campaign
# from .services import send_campaign
#
#
# @receiver(post_save, sender=Campaign)
# def send_campaign_on_create(sender, instance, created, **kwargs):
#     if created:
#         # Запускаем при создании нового объекта
#         send_campaign(instance.id)
#     else:
#         # Запускаем при обновлении существующего объекта
#         send_campaign(instance.id)