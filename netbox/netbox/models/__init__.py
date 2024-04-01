from django.contrib.contenttypes.fields import GenericForeignKey
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import models


class NetboxModel(models.Model):
    """
    Base model for all NetBox models
    """
    class Meta:
        abstract = True

    def clean(self):
        """
        Validate the model for GenericForeignKey fields to ensure that the content type and object ID exist.
        """
        super().clean()

        for field in self._meta.get_field():
            if isinstance(field, GenericForeignKey):
                ct_value = getattr(self, field.ct_field, None)
                fk_value = getattr(self, field.fk_field, None)

                if ct_value is None and fk_value is not None:
                    raise ValidationError({
                        field.ct_field: "This field cannot be null.",
                    })
                if fk_value is None and ct_value is not None:
                    raise ValidationError({
                        field.fk_field: "This field cannot be null.",
                    })

                if ct_value and fk_value:
                    klass = getattr(self, field.ct_field).model_class()
                    try:
                        obj = klass.objects.get(pk=fk_value)
                    except ObjectDoesNotExist:
                        raise ValidationError({
                            field.fk_field: f"Related object not found using the provided value: {fk_value}."
                        })

                    # update the GFK field value
                    setattr(self, field.name, obj)


#
# NetBox internal base models
#

class PrimaryModel(NetboxModel):
    """
    Primary models represent real objects within the infrastructure being modeled.
    """
    description = models.CharField(
        verbose_name=('description'),
        max_length=200,
        blank=True
    )

    class Meta:
        abstract = True
