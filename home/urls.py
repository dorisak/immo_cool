from django.urls import path, include
from home import views


app_name = 'home'

urlpatterns = [
    path('', views.home, name='index'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_view, name='logout'),

]
