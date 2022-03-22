from rest_framework import serializers
from taggit_serializer.serializers import TagListSerializerField, TaggitSerializer
from main.models import CarAdvert, ThingsAdvert, ServicesAdvert, Seller


class SellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seller
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
        )

    read_only_fields = ("id",)


class CarSerializer(TaggitSerializer, serializers.ModelSerializer):

    seller = SellerSerializer(read_only=True)
    tags = TagListSerializerField()

    class Meta:
        model = CarAdvert
        exclude = (
            "created",
            "updated",
        )
        read_only_fields = ("id", "created", "updated", "seller")

    def create(self, validated_data):
        request = self.context.get("request")
        caradvert = CarAdvert.objects.create(
            **validated_data, seller=request.user.seller
        )
        return caradvert


class ThingSerializer(serializers.ModelSerializer):
    seller = SellerSerializer(read_only=True)
    tags = TagListSerializerField()

    class Meta:
        model = ThingsAdvert
        exclude = ("created", "updated")
        read_only_fields = ("id", "created", "updated")

    def create(self, validated_data):
        request = self.context.get("request")
        thingdvert = ThingsAdvert.objects.create(
            **validated_data, seller=request.user.seller
        )
        return thingdvert


class ServiceSerializer(serializers.ModelSerializer):
    seller = SellerSerializer(read_only=True)
    tags = TagListSerializerField()

    class Meta:
        model = ServicesAdvert
        exclude = ("created", "updated")
        read_only_fields = ("id", "created", "updated")

    def create(self, validated_data):
        request = self.context.get("request")
        servicedvert = ServicesAdvert.objects.create(
            **validated_data, seller=request.user.seller
        )
        return servicedvert
