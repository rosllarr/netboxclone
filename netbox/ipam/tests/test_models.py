from django.test import TestCase
from netaddr import IPNetwork

from ipam.models.ip import Prefix


class TestPrefix(TestCase):

    def test_get_duplicates(self):
        prefixes = Prefix.objects.bulk_create((
            Prefix(prefix=IPNetwork('192.0.2.0/24')),
            Prefix(prefix=IPNetwork('192.0.2.0/24')),
            Prefix(prefix=IPNetwork('192.0.2.0/24')),
        ))
        duplicate_prefix_pks = [p.pk for p in prefixes[0].get_duplicates()]

        self.assertSetEqual(set(duplicate_prefix_pks), {prefixes[1].pk, prefixes[2].pk})
