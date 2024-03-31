from django.urls import path

from task_manager.users import views


urlpatterns = [
    path('', views.GetUsersView.as_view(), name="all_users"),
    path('<int:user_id>/update/', views.UserUpdateView.as_view(), name="update_user"),
    path('<int:user_id>/delete/', views.UserDeleteView.as_view(), name="delete_user"),
    path('create/', views.RegisterUserView.as_view(), name="signup_user"),
]