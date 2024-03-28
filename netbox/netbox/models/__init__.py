from django.contrib.contenttypes.fields import GenericForeignKey
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

        for field in self.__meta.get_field():
            if isinstance(field, GenericForeignKey):


#
# NetBox internal base models
#

class PrimaryModel():
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
