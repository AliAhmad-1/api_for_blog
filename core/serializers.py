from rest_framework import serializers
from .models import *
from django.db.models import Count
from taggit.serializers import (TagListSerializerField,TaggitSerializer)



class CommentSerializer(serializers.ModelSerializer):
    # post=serializers.StringRelatedField(read_only=True)
    post=serializers.PrimaryKeyRelatedField(read_only=True)
    user=serializers.StringRelatedField()
    class Meta:
        model=Comment
        fields=['uid','body','created','updated','post','user']



class PostSerializer(TaggitSerializer,serializers.ModelSerializer):
    post_comments=CommentSerializer(many=True,read_only=True)
    tags=TagListSerializerField()
    class Meta:
        model=Post
        fields=['uid','title','slug','status','text','publish','created','updated','author','post_comments','tags']


class PostDetailSerializer(PostSerializer):
    similar_posts=serializers.SerializerMethodField('get_similar_posts')

    def get_similar_posts(self,obj):
        post_id=getattr(obj,'uid')
        post_tags_ids=obj.tags.values_list('id',flat=True)
        similar_posts=Post.published.filter(tags__in=post_tags_ids).exclude(uid=post_id)
        similar_posts=similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags','-publish')[:4]
     

        return PostSerializer(similar_posts,many=True).data

    class Meta:
        model=Post
        fields=PostSerializer.Meta.fields + ['similar_posts']
        



class EmailPostSerializer(serializers.Serializer):
    name=serializers.CharField(max_length=100)
    email=serializers.EmailField(required=True)
    to=serializers.EmailField(required=True)
    comment=serializers.CharField(max_length=250)


class SearchSerializer(serializers.Serializer):
    query=serializers.CharField()