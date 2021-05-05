from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password


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


class ChangeUserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True, allow_blank=True)
    new_password = serializers.CharField(write_only=True, allow_blank=True)
    old_password = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'password', 'old_password', 'new_password', 'confirm_password']
        read_only_fields = ['password']

    def update(self, instance, validated_data):

        instance.password = validated_data.get('password', instance.password)
        instance.username = validated_data.get('username', instance.username)

        if not validated_data['old_password']:
            raise serializers.ValidationError({'old_password': 'not found'})

        if not instance.check_password(validated_data['old_password']):
            raise serializers.ValidationError({'old_password': 'wrong password'})

        if validated_data['new_password'] != validated_data['confirm_password']:
            raise serializers.ValidationError({'passwords': 'passwords do not match'})

        if instance.check_password(validated_data['old_password']):
            if validated_data['new_password'] != '' and validated_data['new_password'] == validated_data['confirm_password']:
                instance.set_password(validated_data['new_password'])
            instance.save()
            return instance

        return instance
