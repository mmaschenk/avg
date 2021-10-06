from .models import AVGRegisterline, ExternalReference
from rest_framework import serializers

class AVGRegisterlineSerializer(serializers.ModelSerializer):
    class Meta:
        model = AVGRegisterline
        fields = '__all__'
        exclude = [ ]
        read_only_fields = []

class EmbeddedAVGRegisterlineSerializer(AVGRegisterlineSerializer):
    id = serializers.IntegerField(label='ID', required=False)

class ExternalReferenceSerializer(serializers.ModelSerializer):
    avgregisterline = EmbeddedAVGRegisterlineSerializer()
    class Meta:
        model = ExternalReference
        fields = '__all__'