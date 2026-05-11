import pytest
from django.utils import timezone
from rest_framework import serializers

from drf_versioning.transforms import AddField, RemoveField, Transform
from drf_versioning.versions import Version
from tests.models import Thing


def test_transform_notimplemented():
    trans = Transform()
    with pytest.raises(NotImplementedError):
        trans.to_internal_value("data", "request")
    with pytest.raises(NotImplementedError):
        trans.to_representation("data", "request", "instance")


@pytest.mark.parametrize(
    "incoming_data, expected_result",
    [
        ({}, {}),  # if the field isn't present, it shouldn't cause problems
        ({"foo": "this should be ignored"}, {}),
        (
            {"foo": "this should be ignored", "other": "unchanged"},
            {"other": "unchanged"},
        ),
    ],
)
def test_addfield_to_internal_value(incoming_data, expected_result):
    trans = AddField()
    trans.field_name = "foo"
    trans.to_internal_value(data=incoming_data, request=...)
    assert incoming_data == expected_result


@pytest.mark.parametrize(
    "outgoing_data, expected_result",
    [
        ({}, {}),
        ({"foo": "this should be ignored"}, {}),
        (
            {"foo": "this should be ignored", "other": "unchanged"},
            {"other": "unchanged"},
        ),
    ],
)
def test_addfield_to_representation(outgoing_data, expected_result):
    trans = AddField()
    trans.field_name = "foo"
    trans.to_representation(data=outgoing_data, request=..., instance=...)
    assert outgoing_data == expected_result


@pytest.mark.django_db
@pytest.mark.parametrize(
    "outgoing_data, expected_result",
    [
        ({}, {"foo": 0}),
        ({"foo": "this should be ignored"}, {"foo": 0}),
        (
            {"other": "unchanged"},
            {"foo": 0, "other": "unchanged"},
        ),
    ],
)
def test_removefield_to_representation(outgoing_data, expected_result):
    thing = Thing.objects.create(
        id=1,
        name="bar",
        number=420,
        date_updated=timezone.now(),
    )
    trans = RemoveField()
    trans.field_name = "foo"
    trans.serializer = serializers.IntegerField()
    trans.to_representation(data=outgoing_data, request=..., instance=thing)
    assert outgoing_data == expected_result


@pytest.mark.parametrize(
    "outgoing_data, expected_result",
    [
        ({"foo": 0, "other": "unchanged"}, {"foo": 0}),
        ({"foo": 1}, {"foo": 1}),
        (
            {"other": "unchanged"},
            {},
        ),
        pytest.param({"foo": None}, {"foo": None}, marks=pytest.mark.xfail),
    ],
)
def test_removefield_to_internal_value(outgoing_data, expected_result):
    trans = RemoveField()
    trans.field_name = "foo"
    trans.serializer = serializers.IntegerField()
    assert trans.to_internal_value(data=outgoing_data, request=...) == expected_result


@pytest.mark.parametrize(
    "outgoing_data, expected_result",
    [
        ({"foo": 0, "other": "unchanged"}, {"foo": 0}),
        ({"foo": 1}, {"foo": 1}),
        (
            {"other": "unchanged"},
            {},
        ),
        ({"foo": None}, {"foo": None}),
    ],
)
def test_removefield_to_internal_value_allow_null(outgoing_data, expected_result):
    trans = RemoveField()
    trans.field_name = "foo"
    trans.serializer = serializers.IntegerField(allow_null=True)
    assert trans.to_internal_value(data=outgoing_data, request=...) == expected_result


def test_transform_meta():
    v420 = Version("4.20")

    class TransformSubclass(Transform):
        version = v420

    assert TransformSubclass in v420.transforms

    class SubclassOfAddField(AddField):
        version = v420

    assert SubclassOfAddField in v420.transforms
