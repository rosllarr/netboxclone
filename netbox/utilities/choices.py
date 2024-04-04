class ChoiceSetMeta(type):
    """
    Metaclass for ChoiceSet
    """
    def __new__(mcs, name, bases, attrs):
        new_class = super().__new__(mcs, name, bases, attrs)


class ChoiceSet(metaclass=ChoiceSetMeta):
    """
    Holds an iterable of choice tuples suitable for passing to a Django model or form field. Choices can be defined
    statically within the class as CHOICES and/or gleaned from the FIELD_CHOICES configuration parameter.
    """
    CHOICES = list()

    @classmethod
    def values(cls):
        return [c[0] for c in unpack_grouped_choices(cls._choices)]


def unpack_grouped_choices(choices):
    """

    """
    pass
