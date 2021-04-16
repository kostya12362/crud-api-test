from django.urls import path, include
from crud import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r"posts", views.PostViews)
router.register(r"comments", views.CommentViews)

urlpatterns = [
    path("", include(router.urls)),
    path("upvote/<int:pk>/", views.UpvotePostView.as_view()),
]
