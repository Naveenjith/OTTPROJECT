from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import (
    UserProfile, Movie, Genre, Subscription, Watchlist, 
    MovieRating, UserActivity
)


# Unregister the default User admin
admin.site.unregister(User)


# Custom User admin with profile inline
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'date_joined')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'date_joined')
    search_fields = ('username', 'first_name', 'last_name', 'email')


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'email', 'phone_number', 'is_verified', 'created_at')
    list_filter = ('is_verified', 'created_at')
    search_fields = ('user__username', 'email', 'phone_number')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at',)


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'language', 'rating', 'is_featured', 'is_trending', 'view_count', 'created_at')
    list_filter = ('language', 'is_featured', 'is_trending', 'certification', 'created_at')
    search_fields = ('title', 'description', 'director', 'cast')
    filter_horizontal = ('genre',)
    readonly_fields = ('view_count', 'created_at', 'updated_at')
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'release_date', 'language', 'certification')
        }),
        ('Media', {
            'fields': ('thumbnail', 'video', 'trailer_url')
        }),
        ('Details', {
            'fields': ('director', 'cast', 'duration', 'rating', 'genre')
        }),
        ('Status', {
            'fields': ('is_featured', 'is_trending', 'view_count')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'subscription_plan', 'status', 'is_active', 'start_date', 'end_date')
    list_filter = ('subscription_plan', 'status', 'is_active', 'start_date')
    search_fields = ('user__username', 'user__email', 'stripe_subscription_id')
    readonly_fields = ('created_at', 'updated_at')
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')


@admin.register(Watchlist)
class WatchlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'movie', 'added_at')
    list_filter = ('added_at',)
    search_fields = ('user__username', 'movie__title')
    readonly_fields = ('added_at',)
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'movie')


@admin.register(MovieRating)
class MovieRatingAdmin(admin.ModelAdmin):
    list_display = ('user', 'movie', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('user__username', 'movie__title', 'review')
    readonly_fields = ('created_at', 'updated_at')
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'movie')


@admin.register(UserActivity)
class UserActivityAdmin(admin.ModelAdmin):
    list_display = ('user', 'activity_type', 'description', 'created_at')
    list_filter = ('activity_type', 'created_at')
    search_fields = ('user__username', 'description')
    readonly_fields = ('created_at',)
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'movie')
    
    def has_add_permission(self, request):
        return False  # Prevent manual creation of activity logs


# Customize admin site
admin.site.site_header = "NAVFLIX Administration"
admin.site.site_title = "NAVFLIX Admin"
admin.site.index_title = "Welcome to NAVFLIX Administration"
