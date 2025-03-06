from django.urls import path
from . import views 
from .views import SignupView,SigninView,SignoutView,IndexView,MovieListView,SearchView2

urlpatterns = [
    path('signup/',SignupView.as_view(), name='signup'),
     path('',SigninView.as_view(), name='signin'),
     path('signout/',SignoutView.as_view(), name='signout'),
     path('change_password/', views.change_password, name='change_password'),
     path('index/',IndexView.as_view(), name='index'),
     path('subscribe/', views.subscribe, name='subscribe'),
    path('movie_list/',MovieListView.as_view(), name='movie_list'),
    path('movie_tamil/',views.movie_tamil, name='movie_tamil'),
    path('movie_malayalam/',views.movie_malayalam, name='movie_malayalam'),
    path('movie_hindi/',views.movie_hindi, name='movie_hindi'),
    path('movie_english/',views.movie_english, name='movie_english'),
    path('movie_telugu/',views.movie_telugu, name='movie_telugu'),
    path('view/',views.view_user_details, name='view_profile'),
    path('change_password/', views.change_password, name='change_password'),
    path('edit_user_profile/', views.edit_user_profile, name='edit_user_profile'),
    path('searchtemp/', views.searchtemp, name='searchtemp'),
     #path('expsub/',expsub.as_view(), name='expsub'),
     #path('search/', searchview.as_view(), name='search'),
     path('search2/', SearchView2.as_view(), name='search2'),

]