from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
import netaddr

from ipam.fields import IPNetworkField
from ipam.choices import PrefixStatusChoices
from netbox.models import PrimaryModel

__all__ = ('Prefix',)


class Prefix(PrimaryModel):
    prefix = IPNetworkField(
        verbose_name=_('prefix'),
        help_text=_('IPv4 or IPv6 network with mask')
    )
    status = models.CharField(
        max_length=50,
        choices=PrefixStatusChoices,
        default=PrefixStatusChoices.STATUS_ACTIVE,
        verbose_name=_('status'),
        help_text=_('Operational status of this prefix')
    )

    class Meta:
        ordering = ('prefix', 'pk')
        verbose_name = _('prefix')
        verbose_name_plural = _('prefixes')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Cache the original prefix so we can check if they have changed on post_save
        self._prefix = self.__dict__.get('prefix')

    def __str__(self):
        return str(self.prefix)

    def get_absolute_url(self):
        return reverse("ipam:prefix", args=[self.pk])

    def clean(self):
        super().clean()

        if self.prefix:

            # /0 masks are not acceptable
            if self.prefix.prefixlen == 0:
                raise ValidationError({
                    'prefix': _("Cannot create prefix with /0 mask.")
                })

            # Enforce unique IP space (if applicable)
            duplicate_prefixes = self.get_duplicates()
            if duplicate_prefixes:
                raise ValidationError({
                    'prefix': _("Duplicate prefix found in {prefix}").format(
                        prefix=duplicate_prefixes.first(),
                    )
                })

    def save(self, *args, **kwargs):

        if isinstance(self.prefix, netaddr.IPNetwork):

            # Clear host bits from prefix
            self.prefix = self.prefix.cidr

        super().save(*args, **kwargs)

    def get_duplicates(self):
        return Prefix.objects.filter(prefix=str(self.prefix)).exclude(pk=self.pk)
