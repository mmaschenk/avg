from django.shortcuts import render
from rest_framework import serializers, viewsets, permissions
from .models import AVGRegisterline
from .serializers import AVGRegisterlineSerializer

# Create your views here.

class AVGRegisterlineViewSet(viewsets.ModelViewSet):
    queryset = AVGRegisterline.objects.all()
    serializer_class = AVGRegisterlineSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]