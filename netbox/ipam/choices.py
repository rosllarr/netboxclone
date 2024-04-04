from django.utils.translation import gettext_lazy as _


class PrefixStatusChoices():
    key = 'Prefix.status'

    STATUS_CONTAINER = 'container'
    STATUS_ACTIVE = 'active'
    STATUS_RESERVED = 'reserved'
    STATUS_DEPRECATED = 'deprecated'

    CHOICES = [
        (STATUS_CONTAINER, _('Container'), 'gray'),
        (STATUS_ACTIVE, _('Active'), 'blue'),
        (STATUS_RESERVED, _('Reserved'), 'cyan'),
        (STATUS_DEPRECATED, _('Deprecated'), 'red'),
    ]
