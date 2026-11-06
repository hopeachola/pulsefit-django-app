from django.urls import path
from . import views

urlpatterns = [
    path('', views.fitness_home, name='fitness_home'),
    path('workouts/', views.workouts_catalog, name='workouts_catalog'),
    path('log/', views.calorie_log, name='calorie_log'),
    path('launch/<str:routine_id>/', views.launch_routine, name='launch_routine'),
    path('log/delete/<int:item_id>/', views.delete_calorie_log, name='delete_calorie_log'),
    
    # User Account Auth Paths
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),

    # Add these lines inside your urlpatterns array list in myapp/urls.py
path('recover/', views.recover_credentials, name='recover_credentials'),
path('recover/reset/<int:user_id>/', views.reset_password, name='reset_password'),

]
