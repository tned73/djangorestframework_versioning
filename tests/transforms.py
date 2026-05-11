from rest_framework import serializers

from drf_versioning.transforms import AddField, RemoveField
from tests import versions


class ThingTransformAddNumber(AddField):
    field_name = "number"
    description = "Added Thing.number field."
    version = versions.VERSION_2_1_0


class ThingAddStatus(AddField):
    field_name = "status"
    description = "Added Thing.status field"
    version = versions.VERSION_2_2_0


class ThingAddDateUpdated(AddField):
    field_name = "date_updated"
    description = "Added Thing.date_updated field"
    version = versions.VERSION_2_2_0


class ThingRemoveFoo(RemoveField):
    field_name = "foo"
    serializer = serializers.IntegerField(allow_null=True)
    version = versions.VERSION_2_0_0
    description = "Removed Thing.foo field"


class PersonAddBirthday(AddField):
    field_name = "birthday"
    description = "Added Person.birthday"
    version = versions.VERSION_2_3_0
