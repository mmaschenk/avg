from django.shortcuts import render
from rest_framework import serializers, viewsets, permissions
from .models import AVGRegisterline, ExternalReference
from .serializers import AVGRegisterlineSerializer, ExternalReferenceSerializer, AVGRegisterlineExternalReferenceSerializer

# Create your views here.


class AVGRegisterlineViewSet(viewsets.ModelViewSet):
    queryset = AVGRegisterline.objects.all()
    serializer_class = AVGRegisterlineSerializer
    permission_classes = [permissions.IsAuthenticated]


class ExternalReferenceViewSet(viewsets.ModelViewSet):
    queryset = ExternalReference.objects.all()
    serializer_class = ExternalReferenceSerializer
    permission_classes = [permissions.IsAuthenticated]


class AVGRegisterLineExternalReferenceViewSet(viewsets.ModelViewSet):
    queryset = ExternalReference.objects.all()
    serializer_class = AVGRegisterlineExternalReferenceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        avg_line = serializer.data
        ext_ref = avg_line.pop("ExternalReference")
        avg_line = AVGRegisterline.objects.create(**avg_line)
        ext_ref.update({"avgregisterline_id": avg_line.id})
        ExternalReference.objects.create(**ext_ref)


