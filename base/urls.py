from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_user, name='login-user'),
    path('register-user/', views.register_user, name='register-user'),
    path('logout-user/', views.logout_user, name='logout-user'),

    path('upload-data/', views.upload_data, name='upload-data'),
    path('query-data/', views.query_data, name='query-data'),

]