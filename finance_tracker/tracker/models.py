from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.text import slugify

from finance_tracker.commons.models import TimestampedModel


class User(AbstractUser):
    def __str__(self):
        return f"{self.get_full_name()} <{self.email}>"


class PayerOrPayee(TimestampedModel):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, blank=True)
    identification_code = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.pk is None:
            self.slug = slugify(self.name)
        super().save(force_insert, force_update, using, update_fields)


class Account(TimestampedModel):
    bank = models.CharField(max_length=255)
    currency = models.CharField(max_length=255)
    account_number = models.CharField(max_length=255)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.bank}[{self.currency}]: <{self.account_number}>"


class BalanceLine(TimestampedModel):
    class Type:
        CREDIT = "Credit"
        DEBIT = "Debit"

        @classmethod
        def as_choices(cls):
            return (
                (cls.CREDIT, cls.CREDIT),
                (cls.DEBIT, cls.DEBIT),
            )

    account = models.ForeignKey("Account", on_delete=models.CASCADE)
    payer_or_payee = models.ForeignKey("PayerOrPayee", on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=8, decimal_places=2)  # up to 999,999.99
    swift_code = models.CharField(max_length=255, null=True, blank=True)
    payment_purpose = models.TextField(null=True, blank=True)
    type = models.CharField(max_length=255, choices=Type.as_choices(), default=Type.CREDIT)
    action_at = models.DateTimeField()
