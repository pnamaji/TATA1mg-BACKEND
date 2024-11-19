from rest_framework import serializers
from .models import *

class MedicineSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    class Meta:
        model = Medicine
        fields = ['id', 'name', 'salt_composition', 'marketer', 'unit_type', 'description', 'storage', 'image', 'mrp', 'prescription_required', 'sku', 'created_at']

    def get_image(self, obj):
        if obj.image:  # Ensure the image exists
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url  # Fallback if no request context
        return None  # If no image is uploaded