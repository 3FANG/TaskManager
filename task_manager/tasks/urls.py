from django.urls import path

from task_manager.tasks import views


urlpatterns = [
    path('', views.IndexTasksView.as_view(), name='all_tasks'),
    path('create/', views.CreateTaskView.as_view(), name='create_task'),
    path('<int:task_id>/', views.ShowTaskView.as_view(), name='show_task'),
    path('<int:task_id>/update/', views.UpdateTaskView.as_view(), name='update_task'),
    path('<int:task_id>/delete/', views.DeleteTaskView.as_view(), name='delete_task'),
]
