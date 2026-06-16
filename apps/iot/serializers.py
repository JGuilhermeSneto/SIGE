from rest_framework import serializers
from .models import RFIDTag

class RFIDTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = RFIDTag
        fields = ['id', 'uid', 'user', 'created_at']
        read_only_fields = ['id', 'created_at']
