from django.contrib.auth.models import User
from rest_framework import serializers
from .models import *

class UserRegisterSerializer(serializers.ModelSerializer):

    username=serializers.CharField(max_length=150,required=True)
    email=serializers.EmailField(required=True)

    class Meta:
        model=User
        fields=['username','first_name','last_name','email','password']
        extra_kwargs={
        'password':{'write_only':True}
        }

    def validate_username(self,value):
        found=User.objects.filter(username=value).exists()
        if found:
            raise serializers.ValidationError('this username already exists !!!')
        return value


class UserLoginSerializer(serializers.ModelSerializer):
    password=serializers.CharField(write_only=True,style={'input_type':'password'})
    username=serializers.CharField(max_length=100,min_length=2,required=True)
    
    class Meta:
        model=User
        fields=['username','password']

class LogoutSerializer(serializers.Serializer):
    refresh_token=serializers.CharField()
    def validate(self,data):
        self.token=data.get('refresh_token')
        return data
    def save(self,**kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail('bad_token')


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=Profile
        fields=['user','bio','image']
        read_only_fields=['user']