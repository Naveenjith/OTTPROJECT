from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse, StreamingHttpResponse, Http404
from django.views import View
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages 
from django.db.models import Q, Avg, Count, Sum
from django.core.paginator import Paginator
from django.utils import timezone
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers
from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
import logging
import os
import mimetypes
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

from .forms import (
    CustomUserCreationForm, SubscriptionForm, UserProfileForm, 
    MovieForm, MovieRatingForm, SearchForm
)
from .models import (
    UserProfile, Movie, Subscription, Genre, Watchlist, 
    MovieRating, UserActivity
)
from .serializers import (
    MovieSerializer, MovieListSerializer, MovieDetailSerializer,
    UserSerializer, UserProfileSerializer, SubscriptionSerializer,
    WatchlistSerializer, MovieRatingSerializer, UserActivitySerializer
)

logger = logging.getLogger(__name__)

# Create your views here.
class SignupView(View):
    template_name = 'signup.html'

    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            try:
                email = form.cleaned_data['email']
                phone_number = form.cleaned_data['phone_number']
                user = form.save()
            
                UserProfile.objects.create(
                    user=user,
                    email=email,
                    phone_number=phone_number
                )

            # Log user activity
                UserActivity.objects.create(
                    user=user,
                    activity_type='profile_update',
                    description='User account created',
                    ip_address=request.META.get('REMOTE_ADDR'),
                    user_agent=request.META.get('HTTP_USER_AGENT', '')
                )

                login(request, user)
                messages.success(request, 'Account created successfully!')
                return redirect('index')

            except Exception as e:
                logger.error(f"Error creating user: {e}")
                messages.error(request, 'An error occurred while creating your account.')
        else:
            messages.error(request, 'Please correct the errors below.')
    
        return render(request, self.template_name, {'form': form})

class SigninView(View):
    template_name = 'signin.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('index')
        form = AuthenticationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                
                # Log user activity
                UserActivity.objects.create(
                    user=user,
                    activity_type='login',
                    description='User logged in',
                    ip_address=request.META.get('REMOTE_ADDR'),
                    user_agent=request.META.get('HTTP_USER_AGENT', '')
                )
                
                messages.success(request, f'Welcome back, {user.username}!')
                return redirect("index")
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Please correct the errors below.')
        
        return render(request, self.template_name, {'form': form})

class SignoutView(View):
    def get(self, request):
        if 'username' in request.session:
            del request.session['username']
        logout(request)
        return redirect('signin')


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            return redirect(view_user_details)  
    else:
        form = PasswordChangeForm(request.user)
        return render(request, 'changepass.html', {"form": form})
    
class IndexView(View):
    template_name = 'index.html'

    def get(self, request):
        if request.user.is_authenticated:
            if Subscription.objects.filter(user=request.user).exists():
                return redirect('movie_list')
            return render(request, self.template_name, {})
        else:
            return redirect('signin')

class MovieListView(LoginRequiredMixin, View):
    template_name = 'movies_list.html'
    login_url = '/signin/'  

    @method_decorator(cache_page(60 * 15))  # cache GET requests for 15 min
    def get(self, request, *args, **kwargs):
        try:
            # Get query parameters
            search_query = request.GET.get('search', '')
            language = request.GET.get('language', '')
            genre = request.GET.get('genre', '')
            featured = request.GET.get('featured', '')
            trending = request.GET.get('trending', '')
            
            # Start with all movies
            movies = Movie.objects.all()

            # Apply filters
            if search_query:
                movies = movies.filter(
                    Q(title__icontains=search_query) |
                    Q(description__icontains=search_query) |
                    Q(director__icontains=search_query) |
                    Q(cast__icontains=search_query)
                )
            
            if language:
                movies = movies.filter(language=language)
            
            if genre:
                movies = movies.filter(genre__name=genre)
            
            if featured == 'true':
                movies = movies.filter(is_featured=True)
            
            if trending == 'true':
                movies = movies.filter(is_trending=True)
            
            # Order by creation date
            movies = movies.order_by('-created_at')
            
            # Pagination
            paginator = Paginator(movies, 12)  # 12 movies per page
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            
            # Get genres for filter dropdown
            genres = Genre.objects.all()
            
            context = {
                'movies': page_obj,
                'genres': genres,
                'search_query': search_query,
                'selected_language': language,
                'selected_genre': genre,
                'featured': featured,
                'trending': trending,
            }
            
            return render(request, self.template_name, context)
            
        except Exception as e:
            logger.error(f"Error in MovieListView: {e}")
            messages.error(request, 'An error occurred while loading movies.')
            return render(request, self.template_name, {'movies': []})


def stream_video(request, movie_id):
    """Stream video file for better performance"""
    try:
        movie = get_object_or_404(Movie, id=movie_id)
        
        # Check if user has active subscription
        if not request.user.is_authenticated:
            raise Http404("Authentication required")
        
        # Check subscription status
        try:
            subscription = Subscription.objects.get(user=request.user)
            if not subscription.is_subscription_active():
                raise Http404("Active subscription required")
        except Subscription.DoesNotExist:
            raise Http404("Subscription required")
        
        # Increment view count
        movie.view_count += 1
        movie.save()
        
        # Log user activity
        UserActivity.objects.create(
            user=request.user,
            activity_type='movie_view',
            description=f'Viewed movie: {movie.title}',
            movie=movie,
            ip_address=request.META.get('REMOTE_ADDR'),
            user_agent=request.META.get('HTTP_USER_AGENT', '')
        )
        
        # Get file path
        file_path = movie.video.path
        
        if not os.path.exists(file_path):
            raise Http404("Video file not found")
        
        # Get file size
        file_size = os.path.getsize(file_path)
        
        # Get range header for partial content
        range_header = request.META.get('HTTP_RANGE', '').strip()
        range_match = range_header.match(r'bytes=(\d*)-(\d*)')
        
        if range_match:
            first_byte, last_byte = range_match.groups()
            first_byte = int(first_byte) if first_byte else 0
            last_byte = int(last_byte) if last_byte else file_size - 1
            
            if first_byte >= file_size:
                return HttpResponse(status=416)
            
            length = last_byte - first_byte + 1
            response = StreamingHttpResponse(
                file_generator(file_path, first_byte, length),
                status=206
            )
            response['Content-Range'] = f'bytes {first_byte}-{last_byte}/{file_size}'
            response['Accept-Ranges'] = 'bytes'
            response['Content-Length'] = str(length)
        else:
            response = StreamingHttpResponse(
                file_generator(file_path),
                status=200
            )
            response['Content-Length'] = str(file_size)
        
        # Set content type
        content_type, _ = mimetypes.guess_type(file_path)
        response['Content-Type'] = content_type or 'video/mp4'
        
        return response
        
    except Exception as e:
        logger.error(f"Error streaming video {movie_id}: {e}")
        raise Http404("Error streaming video")


def file_generator(file_path, start=0, length=None):
    """Generator function to stream file in chunks"""
    with open(file_path, 'rb') as f:
        f.seek(start)
        remaining = length
        while True:
            if remaining:
                chunk_size = min(8192, remaining)
                remaining -= chunk_size
            else:
                chunk_size = 8192
            
            chunk = f.read(chunk_size)
            if not chunk:
                break
            yield chunk


# API Viewsets
class MovieViewSet(viewsets.ReadOnlyModelViewSet):
    """API viewset for movies"""
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'list':
            return MovieListSerializer
        elif self.action == 'retrieve':
            return MovieDetailSerializer
        return MovieSerializer
    
    @action(detail=False, methods=['get'])
    def search(self, request):
        """Search movies by title, description, director, or cast"""
        query = request.query_params.get('q', '')
        if query:
            movies = self.queryset.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(director__icontains=query) |
                Q(cast__icontains=query)
            )
        else:
            movies = self.queryset.none()
        
        serializer = self.get_serializer(movies, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def featured(self, request):
        """Get featured movies"""
        movies = self.queryset.filter(is_featured=True)
        serializer = self.get_serializer(movies, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def trending(self, request):
        """Get trending movies"""
        movies = self.queryset.filter(is_trending=True)
        serializer = self.get_serializer(movies, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def rate(self, request, pk=None):
        """Rate a movie"""
        movie = self.get_object()
        rating = request.data.get('rating')
        review = request.data.get('review', '')
        
        if not rating or not (1 <= float(rating) <= 10):
            return Response(
                {'error': 'Rating must be between 1 and 10'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        rating_obj, created = MovieRating.objects.get_or_create(
            user=request.user,
            movie=movie,
            defaults={'rating': rating, 'review': review}
        )
        
        if not created:
            rating_obj.rating = rating
            rating_obj.review = review
            rating_obj.save()
        
        serializer = MovieRatingSerializer(rating_obj)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def add_to_watchlist(self, request, pk=None):
        """Add movie to user's watchlist"""
        movie = self.get_object()
        watchlist, created = Watchlist.objects.get_or_create(
            user=request.user,
            movie=movie
        )
        
        if created:
            return Response({'message': 'Added to watchlist'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'message': 'Already in watchlist'}, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['delete'])
    def remove_from_watchlist(self, request, pk=None):
        """Remove movie from user's watchlist"""
        movie = self.get_object()
        try:
            watchlist = Watchlist.objects.get(user=request.user, movie=movie)
            watchlist.delete()
            return Response({'message': 'Removed from watchlist'}, status=status.HTTP_200_OK)
        except Watchlist.DoesNotExist:
            return Response({'error': 'Not in watchlist'}, status=status.HTTP_404_NOT_FOUND)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """API viewset for users"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        """Get current user's profile"""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def watchlist(self, request):
        """Get user's watchlist"""
        watchlist = Watchlist.objects.filter(user=request.user)
        serializer = WatchlistSerializer(watchlist, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def activity(self, request):
        """Get user's activity"""
        activity = UserActivity.objects.filter(user=request.user)[:50]
        serializer = UserActivitySerializer(activity, many=True)
        return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def movie_statistics(request):
    """Get movie statistics"""
    stats = {
        'total_movies': Movie.objects.count(),
        'featured_movies': Movie.objects.filter(is_featured=True).count(),
        'trending_movies': Movie.objects.filter(is_trending=True).count(),
        'total_views': Movie.objects.aggregate(total=Sum('view_count'))['total'] or 0,
        'average_rating': Movie.objects.aggregate(avg=Avg('rating'))['avg'] or 0,
        'movies_by_language': dict(Movie.objects.values('language').annotate(count=Count('id')).values_list('language', 'count')),
    }
    return Response(stats)






def subscribe(request):
    if request.method == 'POST':
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            # Check if the user already has a subscription
            try:
                # Attempt to fetch an existing subscription for the user
                subscription = Subscription.objects.get(user=request.user)
                # If it exists, you can choose to update it or raise an error
                #  update the subscription plan:
                subscription_plan = form.cleaned_data['subscription_plan']
                subscription.subscription_plan = subscription_plan
                subscription.save()

                # Redirect to Stripe payment based on the plan
                if subscription_plan == 'basic':
                    return redirect('https://buy.stripe.com/test_7sI28d3yjgC1azu9AA')
                elif subscription_plan == 'standard':
                    return redirect('https://buy.stripe.com/test_eVa5kpecX1H77ni145')
                elif subscription_plan == 'premium':
                    return redirect('https://buy.stripe.com/test_28oaEJ6KvclL6jeaEG')

            except Subscription.DoesNotExist:
                # Create a new subscription if none exists
                subscription = form.save(commit=False)
                subscription.user = request.user
                subscription.save()

                subscription_plan = form.cleaned_data['subscription_plan']
                if subscription_plan == 'basic':
                    return redirect('https://buy.stripe.com/test_7sI28d3yjgC1azu9AA')
                elif subscription_plan == 'standard':
                    return redirect('https://buy.stripe.com/test_eVa5kpecX1H77ni145')
                elif subscription_plan == 'premium':
                    return redirect('https://buy.stripe.com/test_28oaEJ6KvclL6jeaEG')

    else:
        form = SubscriptionForm()

    return render(request, 'subscribe.html', {'form': form})




def movie_tamil(request):
    # Filter movies by language (e.g., Tamil)
    tamil_movies = Movie.objects.filter(language='Tamil')

    context = {'movies': tamil_movies}
    return render(request, 'tamil.html', context)


def movie_malayalam(request):
    # Filter movies by language (e.g., malayalam)
    tamil_movies = Movie.objects.filter(language='Malayalam')

    context = {'movies': tamil_movies}
    return render(request, 'malayalam.html', context)

def movie_telugu(request):
    # Filter movies by language (e.g., Telugu)
    tamil_movies = Movie.objects.filter(language='Telugu')

    context = {'movies': tamil_movies}
    return render(request, 'telugu.html', context)



def movie_english(request):
    # Filter movies by language (e.g., english)
    tamil_movies = Movie.objects.filter(language='English')

    context = {'movies': tamil_movies}
    return render(request, 'english.html', context)


def movie_hindi(request):
    # Filter movies by language (e.g., hindi)
    tamil_movies = Movie.objects.filter(language='hindi')

    context = {'movies': tamil_movies}
    return render(request, 'hindi.html', context)

def view_user_details(request):
    user= UserProfile.objects.get(user=request.user)
    return render(request, 'view_profile.html', {'user':user })



def edit_user_profile(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        # If UserProfile doesn't exist, create a new one
        UserProfile.objects.create(user=request.user, email='', phone_number='', image='')

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully.')
            return redirect(view_user_details)  
    else:
        form = UserProfileForm(instance=user_profile)

    return render(request, 'edit_user_profile.html', {'form': form})



  
def searchtemp(request):
        return render(request, 'search.html')


class SearchView2(View):
    def get(self, request):
        query = request.GET.get('data', '')
        print(query, "fyfuhuyftuihuhg")
        results = Movie.objects.filter(title__icontains=query)
        print(results)
        
        data = []
        for result in results:
            thumbnail_url = result.thumbnail.url if result.thumbnail else ''
            video_url = result.video.url if result.video else ''
            data.append({
                'title': result.title,
                'description': result.description,
                'language': result.language,
                'video_url': video_url,
                'thumbnail_url': thumbnail_url
            })
        
        return JsonResponse({'data': data})
