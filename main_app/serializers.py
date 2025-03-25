from rest_framework import serializers
from .models import Book, Pizza


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = "__all__" # accept all fields from our Book model

class HWDataSerializer(serializers.Serializer):
    first_list = serializers.ListField(child=serializers.IntegerField(), allow_empty=False)
    second_list = serializers.ListField(child=serializers.IntegerField(), allow_empty=False)

class PizzaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pizza
        fields = "__all__"
