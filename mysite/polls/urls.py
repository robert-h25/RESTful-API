from django.urls import path

from . import views

urlpatterns = [
    path('api/login', views.login_user, name='login'),
    path('api/logout', views.logout_user, name='logout'),
    path('api/stories', views.post_stories, name='post_stories'),
    path('api/stories', views.get_stories, name='get_stories'),
    path('api/stories/<int:key>', views.delete, name='delete_story'),
    path('accounts/login/',views.temp, name = 'redirect_login')
]