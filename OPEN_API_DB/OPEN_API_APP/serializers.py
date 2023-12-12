from rest_framework import serializers
from .models import *


class PDF_Serializer(serializers.ModelSerializer):
    class Meta:
        model = PDF_pathfiles
        fields = "__all__"


class Field_Serializer(serializers.ModelSerializer):
    class Meta:
        model = PDF_fields
        fields = "__all__"

