from django.shortcuts import render
from rest_framework import serializers, viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.utils import model_meta
from .models import AVGRegisterline, ExternalReference
from .serializers import AVGRegisterlineSerializer, ExternalReferenceSerializer

# Create your views here.

class AVGRegisterlineViewSet(viewsets.ModelViewSet):
    queryset = AVGRegisterline.objects.all()
    serializer_class = AVGRegisterlineSerializer
    permission_classes = [permissions.IsAuthenticated]

    @staticmethod
    def simplepatch(original, newdata):
        info = model_meta.get_field_info(original)

        for attr, value in newdata.items():
            if attr not in info.relations:
                setattr(original, attr, value)


    @action(detail=False, serializer_class=ExternalReferenceSerializer, methods=['post'] )
    def external(self, request):
        """
        This action updates or inserts a record based on the record in an external system.

        The identifier in the external system should be given in the input parameter **sourcekey** (eg "8273").

        The external system needs to be uniquely identified in the parameter **source** (eg "dmponline").
        
        The **avgregisterline** supplied will be used to update/patch (in case the source/sourcekey combination
        was already present) or insert (if this is a new source/sourcekey combination) the avgregister-record.
        """

        ser = self.get_serializer(data=request.data)

        if not ser.is_valid():
            return Response({'status': 'ERROR', 'reason': ser.errors})

        source = ser.validated_data['source']
        sourcekey = ser.validated_data['sourcekey']

        try:
            ex = ExternalReference.objects.get(source=source,sourcekey=sourcekey)

            if 'id' in ser.validated_data['avgregisterline']:
                return Response({'status': 'ERROR', 'detail': 'Cannot enter id with existing externalref'})

            avgregisterline = ex.avgregisterline
            self.simplepatch(avgregisterline, ser.validated_data['avgregisterline'])
            avgregisterline.save()

        except ExternalReference.DoesNotExist:
            ex = ExternalReference(source=source,sourcekey=sourcekey)

            if 'id' in ser.validated_data['avgregisterline']:
                avgregisterline = AVGRegisterline.objects.get(id=ser.validated_data['avgregisterline']['id'])
                self.simplepatch(avgregisterline,ser.validated_data['avgregisterline'])
            else:
                avgregisterline = AVGRegisterline(**ser.validated_data['avgregisterline'])

            avgregisterline.save()
            ex.avgregisterline = avgregisterline
            ex.save()

        exserial = ExternalReferenceSerializer(ex)

        return Response({'status': 'OK', 'externalreference': exserial.data})


class ExternalReferenceViewSet(viewsets.ModelViewSet):
    queryset = ExternalReference.objects.all()
    serializer_class = ExternalReferenceSerializer
    permission_classes = [permissions.IsAuthenticated]