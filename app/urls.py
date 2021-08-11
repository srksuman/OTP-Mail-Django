from django.urls import path
from . import views
urlpatterns = [
    path('register/',views.createUser,name="register"),
    path('verify/',views.verifyUser,name="verify"),
    path('',views.login_function,name="login"),
    path('success/',views.success,name="success"),
    path('logout/',views.logout_function,name='logout')
]
