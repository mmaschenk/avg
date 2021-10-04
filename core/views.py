from django.shortcuts import render
from rest_framework import serializers, viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import AVGRegisterline, ExternalReference
from .serializers import AVGRegisterlineSerializer, ExternalReferenceSerializer

# Create your views here.

class AVGRegisterlineViewSet(viewsets.ModelViewSet):
    queryset = AVGRegisterline.objects.all()
    serializer_class = AVGRegisterlineSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, serializer_class=ExternalReferenceSerializer, methods=['post'] )
    def external(self, request):
        """
        This action updates or inserts a record based on the record in an external system.

        The identifier in the external system should be given in the input parameter **sourcekey** (eg "8273").

        The external system needs to be uniquely identified in the parameter **source** (eg "dmponline").

        The **avgregisterline** supplied will be used to update/patch (in case the source/sourcekey combination
        wass already present) or insert (if this is a new source/sourcekey combination) the avgregister-record.
        """

        print("Doing it")
        ser = self.get_serializer(data=request.data)
        print("Valid:", ser.is_valid(), ser.errors)

        if not ser.is_valid():
            return Response({'status': 'ERROR', 'reason': ser.errors})

        source = ser.validated_data['source']
        sourcekey = ser.validated_data['sourcekey']

        print("Checking ", source, sourcekey)

        try:
            ex = ExternalReference.objects.get(source=source,sourcekey=sourcekey)
            print("Found ", ex)
        except ExternalReference.DoesNotExist:
            print("Need to make a new reference")
            avgdata = ser.validated_data['avgregisterline']
            print('avgdata: ',avgdata)
            avg = AVGRegisterline(**avgdata)
            avg.save()
            newex = ExternalReference(source=source, sourcekey=sourcekey, avgregisterline=avg)
            newex.save()
            print('avg', avg)
            avgserial = AVGRegisterlineSerializer(avg)
            exserial = ExternalReferenceSerializer(newex)
            return Response({'status': 'OK', 'avg': avgserial.data, 'externalreference': exserial.data})

        #print("Serializer", ser)
        #input = self.get_object()
        return Response({'status': 'OK'})

class ExternalReferenceViewSet(viewsets.ModelViewSet):
    queryset = ExternalReference.objects.all()
    serializer_class = ExternalReferenceSerializer
    permission_classes = [permissions.IsAuthenticated]