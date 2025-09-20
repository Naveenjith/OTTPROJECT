from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile, Movie, Genre, Subscription, Watchlist, MovieRating, UserActivity


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name', 'description', 'created_at']


class MovieSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True, read_only=True)
    genre_ids = serializers.PrimaryKeyRelatedField(
        queryset=Genre.objects.all(),
        many=True,
        write_only=True,
        source='genre'
    )
    
    class Meta:
        model = Movie
        fields = [
            'id', 'title', 'description', 'release_date', 'thumbnail', 'video',
            'language', 'genre', 'genre_ids', 'duration', 'rating', 'certification',
            'director', 'cast', 'trailer_url', 'is_featured', 'is_trending',
            'view_count', 'created_at', 'updated_at'
        ]
        read_only_fields = ['view_count', 'created_at', 'updated_at']


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = [
            'id', 'email', 'phone_number', 'image', 'date_of_birth',
            'bio', 'is_verified', 'created_at', 'updated_at'
        ]
        read_only_fields = ['is_verified', 'created_at', 'updated_at']


class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'profile']
        read_only_fields = ['id', 'username']


class SubscriptionSerializer(serializers.ModelSerializer):
    is_subscription_active = serializers.ReadOnlyField()
    
    class Meta:
        model = Subscription
        fields = [
            'id', 'subscription_plan', 'status', 'start_date', 'end_date',
            'is_active', 'is_subscription_active', 'stripe_subscription_id',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'start_date', 'created_at', 'updated_at']


class WatchlistSerializer(serializers.ModelSerializer):
    movie = MovieSerializer(read_only=True)
    movie_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = Watchlist
        fields = ['id', 'movie', 'movie_id', 'added_at']
        read_only_fields = ['id', 'added_at']


class MovieRatingSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    movie = MovieSerializer(read_only=True)
    
    class Meta:
        model = MovieRating
        fields = ['id', 'user', 'movie', 'rating', 'review', 'created_at', 'updated_at']
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']


class UserActivitySerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    movie = MovieSerializer(read_only=True)
    
    class Meta:
        model = UserActivity
        fields = [
            'id', 'user', 'activity_type', 'description', 'movie',
            'ip_address', 'user_agent', 'created_at'
        ]
        read_only_fields = ['id', 'user', 'created_at']


class MovieListSerializer(serializers.ModelSerializer):
    """Simplified serializer for movie lists"""
    genre_names = serializers.StringRelatedField(source='genre', many=True, read_only=True)
    
    class Meta:
        model = Movie
        fields = [
            'id', 'title', 'thumbnail', 'language', 'genre_names',
            'rating', 'certification', 'is_featured', 'is_trending'
        ]


class MovieDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for individual movie pages"""
    genre = GenreSerializer(many=True, read_only=True)
    average_rating = serializers.SerializerMethodField()
    total_ratings = serializers.SerializerMethodField()
    
    class Meta:
        model = Movie
        fields = [
            'id', 'title', 'description', 'release_date', 'thumbnail', 'video',
            'language', 'genre', 'duration', 'rating', 'certification',
            'director', 'cast', 'trailer_url', 'is_featured', 'is_trending',
            'view_count', 'average_rating', 'total_ratings', 'created_at', 'updated_at'
        ]
    
    def get_average_rating(self, obj):
        ratings = MovieRating.objects.filter(movie=obj)
        if ratings.exists():
            return sum(rating.rating for rating in ratings) / ratings.count()
        return 0.0
    
    def get_total_ratings(self, obj):
        return MovieRating.objects.filter(movie=obj).count()
