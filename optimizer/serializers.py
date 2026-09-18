from rest_framework import serializers



class EnergyRequestSerializer(serializers.Serializer):

    scenario_id = serializers.CharField(
        required=False
    )


    demand = serializers.ListField(
        child=serializers.FloatField()
    )


    solar = serializers.ListField(
        child=serializers.FloatField()
    )


    operator_notes = serializers.ListField(
        child=serializers.CharField(),
        required=False
    )