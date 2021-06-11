from .models import AVGRegisterline
from rest_framework import serializers

class AVGRegisterlineSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = AVGRegisterline
        #fields = [ 'applicatienaam', 'naam_opslagmedium' ]
        fields = '__all__'