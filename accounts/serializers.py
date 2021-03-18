from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_jwt.settings import authenticate

# User Serializer
class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email', )

# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields  ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

        def create(self, validate_data):
            user = User.objects.create_user(validate_data['username'])

            return user

# Login Serializer
class LoginSerializer(serializer.Serialize):
    username = serializer.CharField()
    password = serializer.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializer.ValidationError("Incorrect Credentials")

# class UserSerializerWithToken(serializers.ModelSerializer):

#     token = serializers.SerializerMethodField()
#     password = serializers.CharField(write_only=True)

#     def get_token(self, obj):
#         jwt_payload_handler = api_settings.JWT_payload_handler
#         jwt_encode_handler = api_settings.jwt_encode_handler

#         payload = jwt_payload_handler(obj)
#         token = jwt_encode_handler(payload)
#         return token
    
#     def create(self, validated_data):
#         password = validated_data.pop('password', None)
#         instance = self.Meta.model(**validated_data)
#         if password is not None:
#             instance.set_password(password)
#         instance.save()
#         return instance

#     class Meta:
#         model = User
#         fields = ('token', 'username', 'password')