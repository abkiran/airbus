from rest_framework import serializers

from inventory.models import Inventory, CATEGORY_CHOICES


class InventorySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    product_id = serializers.CharField(max_length=10, allow_blank=False)
    product_category = serializers.ChoiceField(choices=CATEGORY_CHOICES, allow_blank=False)
    product_name = serializers.CharField(max_length=100, allow_blank=False)
    product_description = serializers.CharField(default=None)
    units = serializers.IntegerField(default=0)
    created = serializers.DateTimeField(read_only=True)
    updated = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        """
        Create and return a new `Inventory` instance, given the validated data.
        """
        return Inventory.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Inventory` instance, given the validated data.
        """
        instance.product_id = validated_data.get('product_id', instance.product_id)
        instance.product_category = validated_data.get('product_category', instance.product_category)
        instance.product_name = validated_data.get('product_name', instance.product_name)
        instance.product_description = validated_data.get('product_description', instance.product_description)
        instance.units = validated_data.get('units', instance.units)
        instance.save()
        return instance
