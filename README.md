# NAVFLIX - OTT Platform

A modern Over-The-Top (OTT) streaming platform built with Django, featuring movie streaming, user subscriptions, and comprehensive admin management.

## 🚀 Features

### Core Features
- **User Authentication & Profiles**: Complete user management with profile customization
- **Movie Management**: Upload, categorize, and manage movies with detailed metadata
- **Subscription System**: Multiple subscription tiers with Stripe integration
- **Video Streaming**: Optimized video streaming with range request support
- **Search & Filtering**: Advanced search with language, genre, and feature filters
- **Watchlist & Ratings**: User watchlists and movie rating system
- **Activity Tracking**: Comprehensive user activity logging
- **Admin Dashboard**: Full-featured admin interface for content management

### Technical Features
- **RESTful API**: Complete API with DRF for frontend integration
- **Caching**: Redis-based caching for improved performance
- **Security**: Enhanced security with proper authentication and authorization
- **Docker Support**: Containerized deployment with Docker Compose
- **Database**: MySQL with optimized queries and relationships
- **Logging**: Comprehensive logging system for monitoring
- **Responsive Design**: Mobile-friendly interface

## 🛠 Technology Stack

- **Backend**: Django 5.0.1, Django REST Framework
- **Database**: MySQL 8.0
- **Cache**: Redis 7
- **Web Server**: Gunicorn + Nginx
- **Containerization**: Docker & Docker Compose
- **Payment**: Stripe
- **Frontend**: Bootstrap 5, HTML5, CSS3, JavaScript

## 📋 Prerequisites

- Python 3.8+
- Docker & Docker Compose (recommended)
- MySQL 8.0 (if not using Docker)
- Redis (if not using Docker)

## 🚀 Quick Start

### Using Docker (Recommended)

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd OTT
   ```

2. **Create environment file**
   ```bash
   cp env_template.txt .env
   # Edit .env with your actual values
   ```

3. **Start the application**
   ```bash
   docker-compose up -d
   ```

4. **Create sample data**
   ```bash
   docker-compose exec web python manage.py create_sample_data
   ```

5. **Access the application**
   - Web App: http://localhost:8000
   - Admin Panel: http://localhost:8000/admin
   - API: http://localhost:8000/api/
   - phpMyAdmin: http://localhost:8080

### Manual Setup

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up environment variables**
   ```bash
   cp env_template.txt .env
   # Edit .env with your configuration
   ```

3. **Set up database**
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   python manage.py create_sample_data
   ```

4. **Run the server**
   ```bash
   python manage.py runserver
   ```

## 🔧 Configuration

### Environment Variables

Create a `.env` file with the following variables:

```env
# Django Settings
SECRET_KEY=your-super-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database Settings
DB_NAME=ottdata
DB_USER=root
DB_PASSWORD=your-secure-password
DB_HOST=localhost
DB_PORT=3306

# Stripe Settings
STRIPE_PUBLISHABLE_KEY=pk_test_your_publishable_key
STRIPE_SECRET_KEY=sk_test_your_secret_key

# Redis Settings
REDIS_URL=redis://localhost:6379/1
```

### Database Configuration

The application uses MySQL as the primary database. Make sure to:

1. Create a MySQL database
2. Update the database credentials in `.env`
3. Run migrations: `python manage.py migrate`

## 📚 API Documentation

### Authentication
- **POST** `/api-auth/login/` - Login
- **POST** `/api-auth/logout/` - Logout

### Movies
- **GET** `/api/movies/` - List all movies
- **GET** `/api/movies/{id}/` - Get movie details
- **GET** `/api/movies/search/?q=query` - Search movies
- **GET** `/api/movies/featured/` - Get featured movies
- **GET** `/api/movies/trending/` - Get trending movies
- **POST** `/api/movies/{id}/rate/` - Rate a movie
- **POST** `/api/movies/{id}/add_to_watchlist/` - Add to watchlist
- **DELETE** `/api/movies/{id}/remove_from_watchlist/` - Remove from watchlist

### Users
- **GET** `/api/users/me/` - Get current user profile
- **GET** `/api/users/watchlist/` - Get user's watchlist
- **GET** `/api/users/activity/` - Get user's activity

### Statistics
- **GET** `/api/statistics/` - Get platform statistics

## 🎬 Usage

### For Users

1. **Sign Up**: Create an account with email and phone number
2. **Subscribe**: Choose a subscription plan (Basic, Standard, Premium)
3. **Browse Movies**: Explore movies by language, genre, or search
4. **Watch**: Stream movies with optimized video player
5. **Rate & Review**: Rate movies and add them to your watchlist

### For Administrators

1. **Access Admin**: Go to `/admin/` and login with superuser credentials
2. **Manage Content**: Add, edit, or delete movies and genres
3. **User Management**: View and manage user accounts and subscriptions
4. **Analytics**: Monitor user activity and platform statistics

## 🔒 Security Features

- **CSRF Protection**: Cross-site request forgery protection
- **XSS Protection**: Cross-site scripting protection
- **Secure Headers**: Security headers for enhanced protection
- **Input Validation**: Comprehensive form and API validation
- **Authentication**: Secure user authentication and session management
- **Authorization**: Role-based access control

## 📊 Performance Optimizations

- **Caching**: Redis-based caching for frequently accessed data
- **Database Optimization**: Optimized queries with select_related and prefetch_related
- **Video Streaming**: Range request support for efficient video streaming
- **Static Files**: Optimized static file serving with WhiteNoise
- **Pagination**: Efficient pagination for large datasets

## 🐳 Docker Configuration

The application includes comprehensive Docker configuration:

- **Multi-service setup**: Web, Database, Redis, Nginx
- **Environment variables**: Secure configuration management
- **Volume persistence**: Data persistence across container restarts
- **Health checks**: Container health monitoring
- **Production ready**: Optimized for production deployment

## 🧪 Testing

Run the test suite:

```bash
python manage.py test
```

Or with coverage:

```bash
coverage run --source='.' manage.py test
coverage report
```

## 📈 Monitoring & Logging

- **Application Logs**: Comprehensive logging in `logs/django.log`
- **Error Tracking**: Detailed error logging and monitoring
- **User Activity**: Complete user activity tracking
- **Performance Metrics**: Database query optimization and monitoring

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:

- Create an issue in the repository
- Check the documentation
- Review the admin panel for configuration options

## 🔄 Updates & Maintenance

### Regular Maintenance Tasks

1. **Database Cleanup**: Regular cleanup of old activity logs
2. **Cache Management**: Monitor and optimize cache usage
3. **Security Updates**: Keep dependencies updated
4. **Backup**: Regular database and media backups

### Deployment Checklist

- [ ] Update environment variables for production
- [ ] Set DEBUG=False
- [ ] Configure proper ALLOWED_HOSTS
- [ ] Set up SSL certificates
- [ ] Configure email settings
- [ ] Set up monitoring and logging
- [ ] Test all functionality
- [ ] Run database migrations
- [ ] Collect static files

## 🎯 Future Enhancements

- **Mobile App**: React Native mobile application
- **Recommendation Engine**: AI-powered movie recommendations
- **Live Streaming**: Live event streaming capabilities
- **Social Features**: User reviews, comments, and social sharing
- **Analytics Dashboard**: Advanced analytics and reporting
- **Multi-language Support**: Internationalization support
- **CDN Integration**: Content delivery network for global performance

---

**NAVFLIX** - Your Gateway to Unlimited Entertainment! 🎬✨
