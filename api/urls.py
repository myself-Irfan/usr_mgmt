from django.urls import path
from .views import *

urlpatterns = [
    path('token', ObtainAuthTokenV.as_view(), name='obtain_token'),
    path('sign_up', SignUpV.as_view(), name='sign_up'),
    path('home', HomeV.as_view(), name='home'),
    path('create_post', CreatePostV.as_view(), name='create_post'),
    path('delete_post/<int:post_id>', DeletePostV.as_view(), name='delete_post')
]