class IPNetworkField(BaseIPField):
    """
    IP prefix (network and mask)
    """
    description = "PostgreSQL CIDR field"
    default_validators = [validators.prefix_validator]

    def db_type(self, connect):
        return 'cidr'
