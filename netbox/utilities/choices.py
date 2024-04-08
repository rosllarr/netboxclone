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
    Unpack a grouped choices hierarchy into a flat list of two-tuples. For example:

    choices = (
        ('Foo', (
            (1, 'A'),
            (2, 'B')
        )),
        ('Bar', (
            (3, 'C'),
            (4, 'D')
        ))
    )

    becomes:

    choices = (
        (1, 'A'),
        (2, 'B'),
        (3, 'C'),
        (4, 'D')
    )
    """
    unpacked_choices = []
    for key, value in choices:
        if isinstance(value, (list, tuple)):
            # Entered an optgroup
            for optgroup_key, optgroup_value in value:
                unpacked_choices.append((optgroup_key, optgroup_value))
        else:
            unpacked_choices.append((key, value))
    return unpacked_choices
