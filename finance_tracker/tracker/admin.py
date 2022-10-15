from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from finance_tracker.tracker.models import User, PayerOrPayee, Account, BalanceLine


class AccountInline(admin.TabularInline):
    model = Account
    extra = 0


class BalanceLineInline(admin.TabularInline):
    model = BalanceLine
    extra = 0


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    inlines = (
        AccountInline,
    )


@admin.register(PayerOrPayee)
class PayerOrPayeeAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "identification_code",
    )


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = (
        "__str__",
        "user",
    )

    list_filter = (
        "bank",
        "account_number",
        "currency",
    )

    search_fields = (
        "bank",
        "user__first_name",
        "user__last_name",
        "user__email",
        "user__username",
    )

    inlines = (
        BalanceLineInline,
    )
