from django.urls import path, include
from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from helpdesk.models import Requisitions, Comment


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'password2')

    def create(self, validated_data):
        user = User.objects.create_user(username=validated_data['username'])
        user.set_password(validated_data['password'])
        user.save()
        return user

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError('Password does not match')
        return data


class RequisitionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Requisitions
        fields = ('id', 'status', 'title', 'text', 'active_status',)
        read_only = 'id'


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'text', 'requisitions')
        read_only = 'id'
