from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import generics, status
from django.contrib.auth import authenticate, get_user_model
from apps.user.models import User
from django.core.mail import send_mail
import random

User = get_user_model()

class LoginInSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    email = serializers.EmailField(required=False)
    password = serializers.CharField(write_only=True)
    token = serializers.CharField(source="get_auth_token", read_only=True)

    class Meta:
        model = User
        fields = ("id", "username", "email", "password", "token")

    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")
        email = attrs.get("email")

        print(attrs)

        if not username or not password:
            raise serializers.ValidationError("Username and password are required.")

        # Check if user with username exists
        user_qs = User.objects.filter(username=username)

        if user_qs.exists():
            # Try login
            print("Login")
            user = authenticate(username=username, password=password)
            if not user:
                raise serializers.ValidationError("Invalid credentials. Please try again.")
            attrs["user"] = user
            attrs["status"] = "signin"
        else:
            # Signup path
            if not email:
                raise serializers.ValidationError("Email is required for signup.")
            if User.objects.filter(email=email).exists():
                raise serializers.ValidationError("Email already in use.")
            if User.objects.filter(username=username).exists():
                raise serializers.ValidationError("Username already in use.")

            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            attrs["user"] = user
            attrs["status"] = "signup"

        return attrs



    

