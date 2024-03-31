from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from netaddr import AddrFormatError, IPNetwork


class IPNetworkFormField(forms.Field):
    default_error_message = {
        'invalid': _("Enter a valid IPv4 or IPv6 address (with CIDR mask)."),
    }

    def to_python(self, value):
        if not value:
            return None

        if isinstance(value, IPNetwork):
            return value

        # Ensure that a subnet mask has been specified. This prevents IPs from defaulting to a /32 or /128.
        if len(value.split('/')) != 2:
            raise ValidationError(_("CIDR mask (e.g. /24) is required."))

        try:
            return IPNetwork(value)
        except AddrFormatError:
            raise ValidationError(_("Please specify a valid IPv4 or IPv6 address."))
