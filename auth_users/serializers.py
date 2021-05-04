from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['username', 'password']


# class UserSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = get_user_model()
#         fields = ('id', 'username', 'password')
#         extra_kwargs = {
#             'password': {'write_only': True},
#         }
#
#     def create(self, validated_data):
#         user = get_user_model().objects.create_user(**validated_data)
#         user.set_password(validated_data['password'])
#         user.save()
#         return user
#
#     def update(self, instance, validated_data):
#         if 'password' in validated_data:
#             password = validated_data.pop('password')
#             instance.set_password(password)
#         return super(UserSerializer, self).update(instance, validated_data)

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = get_user_model()
        fields = ('username', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        user = get_user_model().objects.create(
            username=validated_data['username'],
        )
        user.set_password(validated_data['password'])
        user.save()

        return user
