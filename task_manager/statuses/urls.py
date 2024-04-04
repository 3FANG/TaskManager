from django.urls import path

from task_manager.statuses import views


urlpatterns = [
    path('', views.IndexStatusesView.as_view(), name='all_statuses'),
    path('create/', views.CreateStatusView.as_view(), name='create_status'),
    path('<int:status_id>/update/', views.UpdateStatusView.as_view(), name='update_status'),
    path('<int:status_id>/delete/', views.DeleteStatusView.as_view(), name='delete_status'),
]