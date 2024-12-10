from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import ChangeLog

@receiver(post_save)
def log_save(sender, instance, created, **kwargs):
    if sender.__name__ == 'ChangeLog':  # Avoid logging changes to the ChangeLog table itself
        return

    change_type = 'Created' if created else 'Updated'
    ChangeLog.objects.create(
        table_name=sender.__name__,
        change_type=change_type,
        description=str(instance),
    )

@receiver(post_delete)
def log_delete(sender, instance, **kwargs):
    if sender.__name__ == 'ChangeLog':  # Avoid logging changes to the ChangeLog table itself
        return

    ChangeLog.objects.create(
        table_name=sender.__name__,
        change_type='Deleted',
        description=str(instance),
    )
