from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views 
from .views import (
    SignupView, SigninView, SignoutView, IndexView, MovieListView, 
    SearchView2, MovieViewSet, UserViewSet, movie_statistics,
    stream_video
)

# API Router
router = DefaultRouter()
router.register(r'movies', MovieViewSet, basename='movie')
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    # Authentication URLs
    path('', SigninView.as_view(), name='signin'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('signout/', SignoutView.as_view(), name='signout'),
    path('change_password/', views.change_password, name='change_password'),
    
    # Main App URLs
    path('index/', IndexView.as_view(), name='index'),
    path('subscribe/', views.subscribe, name='subscribe'),
    path('movie_list/', MovieListView.as_view(), name='movie_list'),
    
    # Language-specific movie URLs
    path('movie_tamil/', views.movie_tamil, name='movie_tamil'),
    path('movie_malayalam/', views.movie_malayalam, name='movie_malayalam'),
    path('movie_hindi/', views.movie_hindi, name='movie_hindi'),
    path('movie_english/', views.movie_english, name='movie_english'),
    path('movie_telugu/', views.movie_telugu, name='movie_telugu'),
    
    # User Profile URLs
    path('view/', views.view_user_details, name='view_profile'),
    path('edit_user_profile/', views.edit_user_profile, name='edit_user_profile'),
    
    # Search URLs
    path('searchtemp/', views.searchtemp, name='searchtemp'),
    path('search2/', SearchView2.as_view(), name='search2'),
    
    # Video streaming
    path('stream/<int:movie_id>/', stream_video, name='stream_video'),
    
    # API URLs
    path('api/', include(router.urls)),
    path('api/statistics/', movie_statistics, name='movie_statistics'),
    path('api-auth/', include('rest_framework.urls')),
]