from rest_framework import serializers
from Account.models import UserData, UserProfile

class UserDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserData
        fields = ['email', 'mobile_number', 'first_name', 'last_name']

class UserProfileSerializer(serializers.ModelSerializer):
    # username = serializers.CharField(source='user.username', read_only=True)  # User model से username को जोड़ें
    is_owner = serializers.SerializerMethodField()
    
    class Meta:
        model = UserProfile
        fields = ['is_owner', 'user', 'profile_img', 'location', 'last_updated', 'created_at']
        
    def get_is_owner(self, obj):
        request = self.context.get('request')
        return obj.user == request.user  # True if the logged-in user is the owner