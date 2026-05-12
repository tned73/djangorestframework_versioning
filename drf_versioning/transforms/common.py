from typing import Any

from rest_framework import serializers

from .transform import Transform


class AddField(Transform):
    field_name: str

    def to_internal_value(self, data: dict, request):
        data.pop(self.field_name, None)
        return {}

    def to_representation(self, data: dict, request, instance) -> None:
        data.pop(self.field_name, None)


class RemoveField(Transform):
    field_name: str
    serializer: serializers.Field
    default: Any

    def to_internal_value(self, data: dict, request) -> dict[str, Any]:
        if self.field_name in data and hasattr(self, "serializer"):
            return {
                self.field_name: (
                    self.serializer.to_internal_value(data[self.field_name])
                    if data[self.field_name] is not None
                    or not self.serializer.allow_null
                    else None
                )
            }
        return {}

    def to_representation(self, data: dict, request, instance):
        if hasattr(self, "default"):
            data[self.field_name] = self.default
            return
        value = getattr(instance, self.field_name)
        if value is None and self.serializer.allow_null:
            representation = value
        else:
            representation = self.serializer.to_representation(value)

        data[self.field_name] = representation
