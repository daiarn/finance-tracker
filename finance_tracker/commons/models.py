from django.db import models
from django.utils.translation import gettext_lazy as _

def generic_model_str(model, only=None):
    field_values = {
        f.name: getattr(model, f.name, None)
        for f in model._meta.get_fields()
        if not getattr(f, "field", None) and (only is None or f.name in only)
    }
    pairs = " ".join(f"{k}={v!r}" for k, v in field_values.items())
    return pairs


class TimestampedModel(models.Model):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)
