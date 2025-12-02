from django.core.mail import send_mail
from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver
from core.models import Task
from taskflow import settings



@receiver(post_save, sender=Task)
def send_task_assignment_email(sender, instance, created, **kwargs):
    if created:
        subject = f"Yeni Task Teyin Olundu: {instance.title}"
        message = f"Size Yeni Task Teyin Olundu.\n\nBasliq: {instance.title}\nTesvir: {instance.description}\nDeadline: {instance.deadline}"

        for user in instance.assigned_users.all():
            if user.email:
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [user.email],
                    fail_silently=False,
                )



@receiver(post_save, sender=Task)
def send_task_update_email(sender, instance, created, **kwargs):
    if not created:
        subject = f"Task Yenilendi: {instance.title}"
        message = (
            f"Salam,\n\n"
            f"Sizin uzerinizde olan task yenilendi.\n\n"
            f"Basliq: {instance.title}\n"
            f"Tesvir: {instance.description}\n"
            f"Status: {instance.status}\n"
            f"Deadline: {instance.deadline}\n"

        )
        for user in instance.assigned_users.all():
            if user.email:
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [user.email],
                    fail_silently=False,
                )