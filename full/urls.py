from django.urls import path
from . import views

urlpatterns = [
    path('',views.Signup,name='Signup'),
    path('login/',views.login1,name='login'),
    path('profile/',views.profile,name='profile'),
    path('logout/',views.logout1,name='logout'),
    path('passchange/',views.password2,name='pass'),
    path('activate/<uidb64>/<token>',views.activate,name='activate'),
]
