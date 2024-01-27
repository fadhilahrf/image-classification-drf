from rest_framework import serializers

class ModelSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=500)
    image = serializers.ImageField()
    size = serializers.IntegerField()