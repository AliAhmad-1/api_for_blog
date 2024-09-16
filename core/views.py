from .models import *
from taggit.models import Tag
import uuid
#________________
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView,ListAPIView,UpdateAPIView
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import permission_classes,authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import BasicAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication

#__________
from .serializers import *
#________
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.contrib.postgres.search import SearchVector,SearchQuery,SearchRank


class PostListCreateView(ListCreateAPIView):
    serializer_class=PostSerializer
    pagination_class=PageNumberPagination


    def get_queryset(self):
        tag_slug=self.kwargs.get('tag_slug')
        query=self.request.query_params.get('search',None)
        post_list=Post.published.all()
       

        if query is not None:
            search_vector=SearchVector('title','text')
            search_query=SearchQuery(query)
            
            post_list=Post.published.annotate(search=search_vector,rank=SearchRank(search_vector,search_query)).filter(search=search_query).order_by('-rank')
            return post_list
        tag=None
        if tag_slug:
            tag=get_object_or_404(Tag,slug=tag_slug)
            post_list=post_list.filter(tags__in=[tag])
        return post_list

        


    


class PostUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    serializer_class=PostDetailSerializer
   
    def get_object(self):
        year=self.kwargs.get('year')
        month=self.kwargs.get('month')
        day=self.kwargs.get('day')
        slug_post=self.kwargs.get('slug_post')
        queryset=get_object_or_404(Post,publish__year=year,publish__month=month,publish__day=day,slug=slug_post)
        return queryset


class PostShareView(APIView):
    def post(self,request,post_id,format=None):
        post=Post.published.get(uid=post_id)
        serializers=EmailPostSerializer(data=request.data)
        serializers.is_valid(raise_exception=True)
        post_url=request.build_absolute_uri(post.get_absolute_url())
        name=request.data.get('name')
        email=request.data.get('email')
        to=request.data.get('to')
        subject = ( f"{name} ({email}) " f"recommends you read {post.title}")
        message = (f"Read {post.title} at {post_url}\n\n"f"{name}\'s comments: {request.data.get('comment')}")
        send_mail(subject=subject,message=message,from_email=email,recipient_list=[to])
        return Response({'msg':"this post was shared succussfully.."},status=status.HTTP_200_OK)



class CommentListView(ListAPIView):
    serializer_class=CommentSerializer
    permission_classes=[IsAuthenticated]
    authentication_classes=[JWTAuthentication]
    pagination_class=None

    def get_queryset(self):
        post=get_object_or_404(Post,uid=self.kwargs.get('id'),status=Post.Status.PUBLISHED)
        query=post.post_comments.all()
        return query


class CommentCreateView(APIView):
    permission_classes=[IsAuthenticated]
    authentication_classes=[BasicAuthentication]
    def post(self,request,id,format=None):
        post=get_object_or_404(Post,uid=id)
        user=self.request.user
        serializers=CommentSerializer(data=request.data)
        serializers.is_valid(raise_exception=True)
        serializers.validated_data['post']=post
        serializers.validated_data['user']=user
        serializers.save()
        return Response({'msg':'your comment was added successfully'},status=status.HTTP_201_CREATED)

class CommentUpdateView(UpdateAPIView):
    serializer_class=CommentSerializer
    permission_classes=[IsAuthenticated]
    authentication_classes=[BasicAuthentication]
    queryset=Comment.objects.all()
    lookup_field='uid'
    lookup_url_kwarg='comment_id'



class MostCommentedPost(APIView):
    def get(self,request,format=None):
        posts=Post.published.annotate(total_comments=Count('post_comments')).order_by('-total_comments')[:3]
        serializers=PostSerializer(posts,many=True)
        return Response(serializers.data,status=status.HTTP_200_OK)




class LikePostView(APIView):

    def post(self,request,post_id,format=None):
        post=get_object_or_404(Post,uid=post_id)
        user=self.request.user
        action='Like'
        if user in  post.users_like.all():
            post.users_like.remove(user)
            action='Dislike'
        else:
            post.users_like.add(user)
            
        return Response({'msg':f'You are {action}d this Post'},status=status.HTTP_200_OK)
        
        