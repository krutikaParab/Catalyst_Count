from django.urls import path
from . import views
from django.urls import path
from base.views import ChunkedUploadDemo, MyChunkedUploadView, FileChunkUploadCompleteView

urlpatterns = [
    path('', views.login_user, name='login-user'),
    path('register-user/', views.register_user, name='register-user'),
    path('logout-user/', views.logout_user, name='logout-user'),

    path('chunked-upload-start/', ChunkedUploadDemo.as_view(), name='chunked-upload-start'),
    path('chunked-upload-complete/', FileChunkUploadCompleteView.as_view(), name='chunked-upload-complete'),
    path('chunked-upload/', MyChunkedUploadView.as_view(), name='chunked-upload'),

    path('get-all-users-and-status/', views.get_all_users_and_status, name='get-all-users-and-status')
]