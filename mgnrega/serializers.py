from rest_framework import serializers
from .models import District, MGNREGAData

class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = '__all__'

class MGNREGADataSerializer(serializers.ModelSerializer):
    district_name = serializers.CharField(source='district.district_name', read_only=True)
    state_name = serializers.CharField(source='district.state_name', read_only=True)
    
    class Meta:
        model = MGNREGAData
        fields = '__all__'