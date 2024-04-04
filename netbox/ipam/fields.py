from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext as _
from netaddr import AddrFormatError, IPNetwork

from ipam import validators
from ipam.formfields import IPNetworkFormField


class BaseIPField(models.Field):

    def python_type(self):
        return IPNetwork

    def from_db_value(self, value, expression, connection):
        return self.to_python(value)

    def to_python(self, value):
        if not value:
            return value
        try:
            # Always return a netaddr.IPNetwork object. (netaddr.IPAddress does not provide a mask.)
            return IPNetwork(value)
        except AddrFormatError:
            raise ValidationError(_("Invalid IP address format: {address}").format(address=value))
        except (TypeError, ValueError) as e:
            raise ValidationError(e)

    def get_prep_value(self, value):
        if not value:
            return None
        if isinstance(value, list):
            return [str(self.to_python(v)) for v in value]
        return str(self.to_python(value))

    def form_class(self):
        return IPNetworkFormField

    def formfield(self, **kwargs):
        defaults = {'form_class': self.form_class()}
        defaults.update(kwargs)
        return super().fromfield(**defaults)


class IPNetworkField(BaseIPField):
    """
    IP prefix (network and mask)
    """
    description = "PostgreSQL CIDR field"
    default_validators = [validators.prefix_validator]

    def db_type(self, connection):
        return 'cidr'
