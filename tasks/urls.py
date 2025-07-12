from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.task_list, name='task_list'),
    path('create/', views.task_create, name='task_create'),
    path('update/<int:pk>/', views.task_update, name='task_update'),
    path('delete/<int:pk>/', views.task_delete, name='task_delete'),
    path('delete-all/', views.delete_all_tasks, name='delete_all_tasks'),
    path('delete-account/', views.delete_account, name='delete_account'),
    path('password-change/', auth_views.PasswordChangeView.as_view(
        template_name='tasks/password_change.html',
        success_url='/'
    ), name='password_change'),

    path('password-change-done/', auth_views.PasswordChangeDoneView.as_view(
        template_name='tasks/password_change_done.html'
    ), name='password_change_done'),

    path('update-profile-picture/', views.update_profile_picture, name='update_profile_picture'),
]