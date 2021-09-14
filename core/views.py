from django.shortcuts import render
from rest_framework import serializers, viewsets, permissions
from .models import AVGRegisterline, ExternalReference
from .serializers import AVGRegisterlineSerializer, ExternalReferenceSerializer

# Create your views here.


class AVGRegisterlineViewSet(viewsets.ModelViewSet):
    queryset = AVGRegisterline.objects.all()
    serializer_class = AVGRegisterlineSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        avg_line = serializer.data
        ext_ref = avg_line.pop("external_reference")
        avg_line = AVGRegisterline.objects.create(**avg_line)
        ExternalReference.objects.create(avgregisterline_id=avg_line.id, **ext_ref)
"""
    def perform_update(self, serializer):
        # print(serializer.data)
        # print(serializer)
        serializer.save()
        #avg_line = serializer.data
        #ext_ref = avg_line.pop("external_reference")
        #AVGRegisterline.objects.filter(**avg_line).update(**avg_line)
        #ExternalReference.objects.filter(**ext_ref).update(**ext_ref)
"""

class ExternalReferenceViewSet(viewsets.ModelViewSet):
    queryset = ExternalReference.objects.all()
    serializer_class = ExternalReferenceSerializer
    permission_classes = [permissions.IsAuthenticated]


