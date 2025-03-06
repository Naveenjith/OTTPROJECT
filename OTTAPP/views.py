from django.shortcuts import render,redirect
from.forms import customUserCreatonForm,SubscriptionForm,UserProfileForm
from.models import UserProfile,Movie,Subscription
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.forms import AuthenticationForm,PasswordChangeForm
from datetime import datetime,timedelta
from django.http import JsonResponse
from django.views import View
#from rest_framework.views import APIView
#from rest_framework.generics import RetrieveAPIView
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib import messages 
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
class SignupView(View):
    template_name = 'signup.html'

    def get(self, request):
        form = customUserCreatonForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = customUserCreatonForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            user = form.save()
            UserProfile.objects.create(user=user, email=email, phone_number=phone_number)
            login(request, user)
            return redirect('signin')
        else:
            return render(request, self.template_name, {'form': form})

class SigninView(View):
    template_name = 'signin.html'

    def get(self, request):
        form = AuthenticationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            request.session['username'] = username
            if user is not None:
                login(request, user)
                return redirect("index")
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

class MovieListView(LoginRequiredMixin,View):
    template_name = 'movies_list.html'
    login_url = '/signin/'  

    
    def get(self, request):
        movies = Movie.objects.all()
        return render(request, self.template_name, {'movies': movies})






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
