from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def prefix_validator(prefix):
    if prefix.ip != prefix.cidr.ip:
        raise ValidationError(
            _("{prefix} is not a valid prefix. Did you mean {suggestion}?").format(
                prefix=prefix, suggestion=prefix.cidr
            )
        )
