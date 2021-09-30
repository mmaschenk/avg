from .models import AVGRegisterline, ExternalReference
from rest_framework import serializers


class ExternalReferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExternalReference
        fields = ["source", "sourcekey", "last_updated"]


class AVGRegisterlineSerializer(serializers.ModelSerializer):
    external_reference = ExternalReferenceSerializer()

    class Meta:
        model = AVGRegisterline
        exclude = []

    def update(self, instance, validated_data):
        nested_serializer = self.fields['external_reference']
        nested_instance = instance.external_reference
        nested_data = validated_data.pop('external_reference')
        nested_serializer.update(nested_instance, nested_data)
        return super(AVGRegisterlineSerializer, self).update(instance, validated_data)
