from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import CalorieLog, WorkoutLog
from .forms import CalorieLogForm

@login_required(login_url='login')
def fitness_home(request):
    today = timezone.now().date()
    
    # Filter statistics explicitly by the logged-in user
    today_workouts = WorkoutLog.objects.filter(user=request.user, date_completed=today)
    total_burned = today_workouts.aggregate(Sum('calories_burned'))['calories_burned__sum'] or 0
    active_time = today_workouts.aggregate(Sum('duration'))['duration__sum'] or 0
    
    # Calculate daily streak dynamically for this user
    daily_streak = 0
    streak_date = today
    while WorkoutLog.objects.filter(user=request.user, date_completed=streak_date).exists():
        daily_streak += 1
        streak_date -= timedelta(days=1)
    if daily_streak == 0:
        yesterday = today - timedelta(days=1)
        streak_date = yesterday
        while WorkoutLog.objects.filter(user=request.user, date_completed=streak_date).exists():
            daily_streak += 1
            streak_date -= timedelta(days=1)

    context = {
        'total_burned': total_burned,
        'daily_streak': daily_streak,
        'active_time': active_time,
    }
    return render(request, 'fitness_home.html', context)

@login_required(login_url='login')
def workouts_catalog(request):
    return render(request, 'workouts.html')

@login_required(login_url='login')
def calorie_log(request):
    if request.method == 'POST':
        form = CalorieLogForm(request.POST)
        if form.is_valid():
            log_instance = form.save(commit=False)
            log_instance.user = request.user  
            log_instance.save()
            return redirect('calorie_log')
    else:
        form = CalorieLogForm()

    # Query only this user's logs
    logs = CalorieLog.objects.filter(user=request.user).order_by('-id')
    daily_target = 1850
    total_logged = logs.aggregate(Sum('calories'))['calories__sum'] or 0
    remaining_calories = max(0, daily_target - total_logged)

    # Fetch logs grouped by date specifically for timeseries charts
    history_raw = (
        CalorieLog.objects.filter(user=request.user)
        .values('date_logged')
        .annotate(total_day_calories=Sum('calories'))
        .order_by('date_logged')[:7]  
    )
    
    chart_dates = [entry['date_logged'].strftime('%b %d') for entry in history_raw]
    chart_intakes = [entry['total_day_calories'] for entry in history_raw]

    context = {
        'form': form,
        'logs': logs,
        'daily_target': daily_target,
        'total_logged': total_logged,
        'remaining_calories': remaining_calories,
        'chart_dates': chart_dates,
        'chart_intakes': chart_intakes,
    }
    return render(request, 'calorie_log.html', context)

@login_required(login_url='login')
def launch_routine(request, routine_id):
    if request.method == 'POST':
        if routine_id == "strength":
            WorkoutLog.objects.create(user=request.user, routine_id="strength", title="Strength Base Routine", duration=45, calories_burned=320)
        else:
            WorkoutLog.objects.create(user=request.user, routine_id="cardio", title="Fat Burn Engine Routine", duration=25, calories_burned=410)
        return redirect('fitness_home')

    if routine_id == "strength":
        title = "Strength Base Routine"
        exercises = ["Barbell Squats (3 Sets x 5 Reps)", "Overhead Press (3 Sets x 5 Reps)", "Pull-Ups (3 Sets x Max Reps)"]
        duration = 45
    else:
        title = "Fat Burn Engine Routine"
        exercises = ["Sprints (5 Rounds)", "Kettlebell Swings (4 Sets x 15 Reps)", "Burpees (4 Sets x 12 Reps)"]
        duration = 25

    context = {
        'title': title,
        'exercises': exercises,
        'duration': duration,
        'routine_id': routine_id
    }
    return render(request, 'launch_routine.html', context)

@login_required(login_url='login')
def delete_calorie_log(request, item_id):
    log_item = get_object_or_404(CalorieLog, id=item_id, user=request.user)
    log_item.delete()
    return redirect('calorie_log')

# ==========================================
# AUTHENTICATION VIEWS
# ==========================================
def register_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('fitness_home')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_user(request):
    error_message = None
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('fitness_home')
        else:
            error_message = "Invalid username or password configuration."
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form, 'error_message': error_message})

def logout_user(request):
    logout(request)
    return redirect('login')

# ==========================================
# ACCOUNT RECOVERY VIEWS
# ==========================================
def recover_credentials(request):
    error_message = None
    username_found = None
    user_obj = None

    if request.method == 'POST':
        email_lookup = request.POST.get('email')
        if email_lookup:
            try:
                user_obj = User.objects.get(email=email_lookup)
                username_found = user_obj.username
            except User.DoesNotExist:
                error_message = "No account found associated with that email address."

    context = {
        'error_message': error_message,
        'username_found': username_found,
        'user_obj': user_obj,
    }
    return render(request, 'recover_credentials.html', context)

def reset_password(request, user_id):
    user_obj = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        new_pass = request.POST.get('new_password')
        confirm_pass = request.POST.get('confirm_password')
        
        if new_pass == confirm_pass:
            user_obj.set_password(new_pass)
            user_obj.save()
            return redirect('login')
        else:
            messages.error(request, "Passwords do not match.")
            
    return render(request, 'reset_password.html', {'user_obj': user_obj})
