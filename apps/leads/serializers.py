from rest_framework import serializers
from .models import Lead, FunnelStage, LeadInteraction

class FunnelStageSerializer(serializers.ModelSerializer):
    class Meta:
        model = FunnelStage
        fields = "__all__"

class LeadInteractionSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeadInteraction
        fields = "__all__"

class LeadSerializer(serializers.ModelSerializer):
    interactions = LeadInteractionSerializer(many=True, read_only=True)
    stage_name = serializers.CharField(source="stage.name", read_only=True)

    class Meta:
        model = Lead
        fields = "__all__"
