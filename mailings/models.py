from django.db import models


class Recipient(models.Model):
    email = models.EmailField(unique=True, verbose_name="E-mail")
    full_name = models.CharField(max_length=255, verbose_name="Ф. И. О.")
    comment = models.TextField(blank=True, null=True, verbose_name="Комментарий")

    def __str__(self):
        return f"{self.full_name} ({self.email})"


class Message(models.Model):
    subject = models.CharField(max_length=255, verbose_name="Тема письма")
    body = models.TextField(verbose_name="Тело письма")

    def __str__(self):
        return self.subject


class Campaign(models.Model):
    STATUS_CHOICES = [
        ("Создана", "Создана"),
        ("Запущена", "Запущена"),
        ("Завершена", "Завершена"),
    ]

    start_time = models.DateTimeField(
        null=True, blank=True, verbose_name="Дата и время первой отправки"
    )
    end_time = models.DateTimeField(
        null=True, blank=True, verbose_name="Дата и время окончания отправки "
    )
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default="Создана", verbose_name="Статус"
    )
    message = models.ForeignKey(
        Message, on_delete=models.CASCADE, verbose_name="Сообщение "
    )
    recipients = models.ManyToManyField(Recipient, verbose_name="Получатели")

    def __str__(self):
        return f"Рассылка {self.id} - {self.status}"


class SendAttempt(models.Model):
    campaign = models.ForeignKey(
        Campaign, on_delete=models.CASCADE, verbose_name="Рассылка"
    )
    attempt_time = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата и время попытки"
    )
    status_choices = [
        ("Успешно", "Успешно"),
        ("Не успешно", "Не успешно"),
    ]
    status = models.CharField(
        max_length=10, choices=status_choices, verbose_name="Статус"
    )
    server_response = models.TextField(verbose_name="Ответ почтового сервера")


class SendLog(models.Model):
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    recipient = models.ForeignKey(Recipient, on_delete=models.CASCADE)
    attempt_time = models.DateTimeField(auto_now_add=True)
    status_choices = [
        ("Успешно", "Успешно"),
        ("Не успешно", "Не успешно"),
    ]
    status = models.CharField(max_length=10, choices=status_choices)
    server_response = models.TextField()
