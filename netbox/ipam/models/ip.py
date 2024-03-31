from django.utils.translation import gettext_lazy as _

from netbox.ipam.fields import IPNetworkField
from netbox.models import PrimaryModel


class Prefix(PrimaryModel):
    prefix = IPNetworkField(
        verbose_name=_('prefix'),
        help_text=_('IPv4 or IPv6 network with mask')
    )
