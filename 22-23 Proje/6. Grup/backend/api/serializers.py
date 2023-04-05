from rest_framework import serializers
from . import models
from django.contrib.auth.models import User

class InterestSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.Interest
        fields="__all__"

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','email','password','is_superuser','date_joined','last_login','is_authenticated']

        extra_kwargs = {'password':{
            'write_only':True,
            'required' :True
        }}


class ProfileSerializer(serializers.ModelSerializer):

    interests = serializers.SerializerMethodField('get_interests')
    user = serializers.SerializerMethodField('get_user')
    class Meta:
        model = models.Profile
        fields = "__all__"

    def get_interests(self,profile):
        if profile.interests:
            interests = InterestSerializer(profile.interests,many=True)
            return interests.data
        else:
            return None
        
    def get_user(self,profile):
        if profile.user:
            data = UserSerializer(profile.user,many=False)
            return data.data 
        else:
            return None

class PostSerializer(serializers.ModelSerializer):

    profile = serializers.SerializerMethodField('get_profile')
    class Meta:
        model=models.Post
        fields=['profile','text']

    def get_profile(self,post):
        if post.profile:
            profile = ProfileSerializer(post.profile,many=False)
            return profile.data
        else:
            return None