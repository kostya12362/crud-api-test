from crud.models import Post, Comment
from rest_framework import viewsets, views, status, permissions
from rest_framework.response import Response
from crud.serializers import PostSerializer, PostDetailSerializer, CommentSerializer


class PostViews(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return PostSerializer
        return PostDetailSerializer

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            self.permission_classes = (permissions.IsAuthenticated,)
        return super(PostViews, self).get_permissions()

    def destroy(self, request, *args, **kwargs):
        if request.user == Post.objects.get(pk=kwargs["pk"]).author:
            Post.objects.get(pk=kwargs["pk"]).delete()
            return Response({"message": "you deleted the object"})
        else:
            return Response({"error": "you can`t deleted the object"})


class CommentViews(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def destroy(self, request, *args, **kwargs):
        if request.user == Comment.objects.get(pk=kwargs["pk"]).author:
            Comment.objects.get(pk=kwargs["pk"]).delete()
            return Response({"message": "you deleted your comment"})
        else:
            return Response({"error": "This comment was not created by you"})


class UpvotePostView(views.APIView):
    """
    Upvoting posts.
    """

    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, pk):
        post = Post.objects.get(id=pk)
        post.add_upvote(user=request.user)
        return Response(status=status.HTTP_200_OK)
