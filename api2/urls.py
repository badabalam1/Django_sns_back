from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import *

urlpatterns = [
    path("user/<int:user_id>/", view=UserPage.as_view(), name='test'),
    path("login/", view=UserLogin.as_view(), name='Login'),
    path("register/", view=UserRegister.as_view(), name='Register'),
    path("passwordChange/", view=PasswordChange.as_view(), name='PasswordChange'),
    path("<int:user_id>/follow/", view=Follow.as_view(), name='follow'),
    path("<int:user_id>/followers/", view=Followers.as_view(), name='followers'),
    path("<int:user_id>/following/", view=Following.as_view(), name='following')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
