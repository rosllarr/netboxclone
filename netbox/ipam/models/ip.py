from netbox.models import PrimaryModel


class Prefix(PrimaryModel):
    prefix = IPNetworkField()