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

        print("Doing it")
        ser = self.get_serializer(data=request.data)
        print(request.data)
        print("Valid:", ser.is_valid(), ser.errors)

        if not ser.is_valid():
            return Response({'status': 'ERROR', 'reason': ser.errors})

        source = ser.validated_data['source']
        sourcekey = ser.validated_data['sourcekey']

        try:
            ex = ExternalReference.objects.get(source=source,sourcekey=sourcekey)
            print("Found externalref")

            if 'id' in ser.validated_data['avgregisterline']:
                return Response({'status': 'ERROR', 'detail': 'Cannot enter id with existing externalref'})

            avg = ex.avgregisterline

            self.simplepatch(avg, ser.validated_data['avgregisterline'])

        except ExternalReference.DoesNotExist:
            print( "New externalref")
            ex = ExternalReference(source=source,sourcekey=sourcekey)

            if 'id' in ser.validated_data['avgregisterline']:
                print("Need to find existing record and update")
                avgregisterline = AVGRegisterline.objects.get(id=ser.validated_data['avgregisterline']['id'])
                print('avgregisterline',avgregisterline)

                self.simplepatch(avgregisterline,ser.validated_data['avgregisterline'])
                """
                info = model_meta.get_field_info(avgregisterline)

                for attr, value in ser.validated_data['avgregisterline'].items():
                    if attr not in info.relations:
                        setattr(avgregisterline, attr, value)
                """
            else:
                print("Need to add avg record")
                avgregisterline = AVGRegisterline(**ser.validated_data['avgregisterline'])
                print('avgregisterline',avgregisterline)

            avgregisterline.save()
            ex.avgregisterline = avgregisterline
            ex.save()

        exserial = ExternalReferenceSerializer(ex)

        return Response({'status': 'OK', 'externalreference': exserial.data})


        #print("Checking ", source, sourcekey)

        #ser.is_valid()
        #ser.save()
        
        #print('si', ser.instance.id)
        #print('se', ser._errors)

        #return Response({'status': 'OK', 'avgregisterline': ser.avg.data, 'externalreference': ser.data,
        #    'avgrecordadded': ser.avg._created, 'externalreferenceadded': ser._created})
        """
        try:
            ex = ExternalReference.objects.get(source=source,sourcekey=sourcekey)
            print("Found ", ex)
        except ExternalReference.DoesNotExist:
            print("Need to make a new reference")
            print("validated", ser.validated_data)
            avgdata = ser.validated_data['avgregisterline']
            print('avgdata: ',avgdata)
            avg = AVGRegisterline(**avgdata)
            print('avg', avg)
            if 'id' not in ser.validated_data['avgregisterline']:
                print('Hell no')
                print('id present', avg.id)
            else:
                avg2 = AVGRegisterline.objects.get(id=avg.id)
                print('avg2', avg2)
                ser.avgregisterline.save()
            avg.save()
            newex = ExternalReference(source=source, sourcekey=sourcekey, avgregisterline=avg)
            newex.save()
            print('avg', avg)
            avgserial = AVGRegisterlineSerializer(avg)
            exserial = ExternalReferenceSerializer(newex)
            return Response({'status': 'OK', 'avgregisterline': avgserial.data, 'externalreference': exserial.data})
        """

        #print("Serializer", ser)
        #input = self.get_object()
        #return Response({'status': 'OK'})

class ExternalReferenceViewSet(viewsets.ModelViewSet):
    queryset = ExternalReference.objects.all()
    serializer_class = ExternalReferenceSerializer
    permission_classes = [permissions.IsAuthenticated]