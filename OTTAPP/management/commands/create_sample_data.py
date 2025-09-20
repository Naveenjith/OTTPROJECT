from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from OTTAPP.models import Genre, Movie, UserProfile, Subscription
from datetime import datetime, timedelta
import random


class Command(BaseCommand):
    help = 'Create sample data for the OTT platform'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample data...')
        
        # Create genres
        genres_data = [
            {'name': 'Action', 'description': 'High-energy movies with physical stunts and chases'},
            {'name': 'Comedy', 'description': 'Movies designed to make the audience laugh'},
            {'name': 'Drama', 'description': 'Serious, plot-driven presentations'},
            {'name': 'Horror', 'description': 'Movies designed to frighten, unsettle, or scare'},
            {'name': 'Romance', 'description': 'Love stories and romantic relationships'},
            {'name': 'Sci-Fi', 'description': 'Science fiction and futuristic themes'},
            {'name': 'Thriller', 'description': 'Suspenseful and exciting movies'},
            {'name': 'Documentary', 'description': 'Non-fiction films documenting reality'},
            {'name': 'Animation', 'description': 'Animated films and cartoons'},
            {'name': 'Crime', 'description': 'Movies about criminal activities'},
        ]
        
        genres = []
        for genre_data in genres_data:
            genre, created = Genre.objects.get_or_create(
                name=genre_data['name'],
                defaults={'description': genre_data['description']}
            )
            genres.append(genre)
            if created:
                self.stdout.write(f'Created genre: {genre.name}')
        
        # Create sample movies
        movies_data = [
            {
                'title': 'The Dark Knight',
                'description': 'When the menace known as the Joker wreaks havoc and chaos on the people of Gotham, Batman must accept one of the greatest psychological and physical tests of his ability to fight injustice.',
                'language': 'English',
                'director': 'Christopher Nolan',
                'cast': 'Christian Bale, Heath Ledger, Aaron Eckhart',
                'rating': 9.0,
                'certification': 'A',
                'is_featured': True,
                'is_trending': True,
                'genre_names': ['Action', 'Crime', 'Drama']
            },
            {
                'title': 'Inception',
                'description': 'A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea into the mind of a C.E.O.',
                'language': 'English',
                'director': 'Christopher Nolan',
                'cast': 'Leonardo DiCaprio, Marion Cotillard, Tom Hardy',
                'rating': 8.8,
                'certification': 'A',
                'is_featured': True,
                'is_trending': False,
                'genre_names': ['Action', 'Sci-Fi', 'Thriller']
            },
            {
                'title': 'Baahubali 2: The Conclusion',
                'description': 'When Shiva, the son of Bahubali, learns about his heritage, he begins to look for answers. His story is juxtaposed with past events that unfolded in the Mahishmati Kingdom.',
                'language': 'Telugu',
                'director': 'S.S. Rajamouli',
                'cast': 'Prabhas, Rana Daggubati, Anushka Shetty',
                'rating': 8.2,
                'certification': 'U/A',
                'is_featured': True,
                'is_trending': True,
                'genre_names': ['Action', 'Drama', 'Fantasy']
            },
            {
                'title': 'Dangal',
                'description': 'Former wrestler Mahavir Singh Phogat and his two wrestler daughters struggle towards glory at the Commonwealth Games in the face of societal oppression.',
                'language': 'Hindi',
                'director': 'Nitesh Tiwari',
                'cast': 'Aamir Khan, Sakshi Tanwar, Fatima Sana Shaikh',
                'rating': 8.4,
                'certification': 'U',
                'is_featured': False,
                'is_trending': True,
                'genre_names': ['Biography', 'Drama', 'Sport']
            },
            {
                'title': 'Jailer',
                'description': 'Muthuvel Pandian is a retired jailer living happily with his family. The story is about how he avenges his son against the mastermind behind large-scale smuggling.',
                'language': 'Tamil',
                'director': 'Nelson Dilipkumar',
                'cast': 'Rajinikanth, Vinayakan, Ramya Krishnan',
                'rating': 7.5,
                'certification': 'U/A',
                'is_featured': True,
                'is_trending': False,
                'genre_names': ['Action', 'Comedy', 'Crime']
            },
            {
                'title': '2018: Everyone is a Hero',
                'description': 'The story takes place in Kerala during the 2018 deluge where life came to a standstill due to floods.',
                'language': 'Malayalam',
                'director': 'Jude Anthany Joseph',
                'cast': 'Tovino Thomas, Kunchacko Boban, Asif Ali',
                'rating': 8.1,
                'certification': 'U',
                'is_featured': False,
                'is_trending': True,
                'genre_names': ['Drama', 'Thriller']
            }
        ]
        
        for movie_data in movies_data:
            # Get genres for this movie
            movie_genres = [g for g in genres if g.name in movie_data['genre_names']]
            
            movie, created = Movie.objects.get_or_create(
                title=movie_data['title'],
                defaults={
                    'description': movie_data['description'],
                    'language': movie_data['language'],
                    'director': movie_data['director'],
                    'cast': movie_data['cast'],
                    'rating': movie_data['rating'],
                    'certification': movie_data['certification'],
                    'is_featured': movie_data['is_featured'],
                    'is_trending': movie_data['is_trending'],
                    'release_date': datetime.now().date() - timedelta(days=random.randint(30, 365)),
                    'view_count': random.randint(100, 10000)
                }
            )
            
            if created:
                movie.genre.set(movie_genres)
                self.stdout.write(f'Created movie: {movie.title}')
        
        # Create a superuser if it doesn't exist
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@navflix.com',
                password='admin123'
            )
            self.stdout.write('Created superuser: admin (password: admin123)')
        
        # Create some regular users
        for i in range(1, 6):
            username = f'user{i}'
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(
                    username=username,
                    email=f'{username}@example.com',
                    password='password123',
                    first_name=f'User{i}',
                    last_name='Test'
                )
                
                # Create user profile
                UserProfile.objects.create(
                    user=user,
                    email=f'{username}@example.com',
                    phone_number=f'987654321{i}',
                    is_verified=True
                )
                
                # Create subscription for some users
                if i <= 3:
                    Subscription.objects.create(
                        user=user,
                        subscription_plan=random.choice(['basic', 'standard', 'premium']),
                        status='active',
                        end_date=datetime.now() + timedelta(days=30)
                    )
                
                self.stdout.write(f'Created user: {username}')
        
        self.stdout.write(
            self.style.SUCCESS('Successfully created sample data!')
        )
