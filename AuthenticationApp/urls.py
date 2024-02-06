from django.urls import path
from . import views

urlpatterns = [
    path('signup/<str:_id>/', views.Signup, name="signup"),
    path('create-advisor/', views.create_advisor, name='create-advisor'),
    path('login/',views.Login, name='login'),
    path('logout/',views.Logout, name='logout'),
]