from django.core.management.base import BaseCommand

from mailings.services import send_campaign


class Command(BaseCommand):
    help = "Отправить рассылку по ID кампании"

    def add_arguments(self, parser):
        parser.add_argument("campaign_id", type=int)

    def handle(self, *args, **kwargs):
        campaign_id = kwargs["campaign_id"]
        try:
            send_campaign(campaign_id)
            self.stdout.write(f"Рассылка кампании {campaign_id} запущена.")
        except Exception as e:
            self.stderr.write(f"Ошибка: {e}")
