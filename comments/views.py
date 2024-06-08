from django.shortcuts import render
from rest_framework import generics, viewsets, mixins
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


from .models import Comment
from .serializers import CommentSerializer

def index(request):
    return render(request, 'index.html')


class AddCommentView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    authentication_classes = (JWTAuthentication, )
        
    def perform_create(self, serializer):
        comment = serializer.save()
        user = self.request.user

        if user.is_authenticated:
            comment.created_by = user.created_by
            comment.email = user.email
            comment.save()
            
        comment_data = CommentSerializer(comment).data
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'comments_group',
            {
                'type': 'add_comment',
                'comment': comment_data
            }
        )
        
    

        



    
    
    