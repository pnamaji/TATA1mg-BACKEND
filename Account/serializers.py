from rest_framework import serializers
from Account.models import *

class UserDataSerializer(serializers.ModelSerializer):
    joined_date = serializers.DateTimeField(source='user.date_joined', read_only=True)
    class Meta:
        model = UserData
        fields = ['email', 'mobile_number', 'joined_date']

class UserAccountSerializer(serializers.Serializer):
    joined_date = serializers.DateTimeField(source='date_joined', read_only=True)
    email = serializers.EmailField(read_only=True)
    # mobile_number = serializers.CharField(source='userdata.mobile_number', read_only=True)
    

    class Meta:
        model = User
        fields = ['joined_date', 'email', 'mobile_number']

class UserProfileSerializer(serializers.ModelSerializer):
    # username = serializers.CharField(source='user.username', read_only=True)  # User model से username को जोड़ें
    is_owner = serializers.SerializerMethodField()
    
    class Meta:
        model = UserProfile
        fields = ['is_owner', 'user', 'profile_img', 'location', 'last_updated', 'created_at']
        
    def get_is_owner(self, obj):
        request = self.context.get('request')
        return obj.user == request.user  # True if the logged-in user is the owner

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity', 'price']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, source='orderitem_set', read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'total_price', 'status', 'order_date', 'shipping_address', 'items']