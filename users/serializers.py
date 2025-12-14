from rest_framework import serializers

from users.models import User


class UserBaseSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["_id"] = str(instance._id)
        return representation


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("email", "password", "username", "first_name", "last_name")

    def create(self, validated_data):
        user = User(
            email=validated_data["email"],
            username=validated_data["username"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],

        )
        user.set_password(validated_data["password"])
        user.save()

        return user


class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("email", "password")


class UserProfileSerializer(UserBaseSerializer):
    class Meta:
        model = User
        fields = ("email", "first_name", "last_name")
        read_only_fields = fields


class UserRegisterResponseSerializer(UserBaseSerializer):
    class Meta:
        model = User
        fields = ("email", "first_name", "last_name")
