from django.urls import path

from task_manager.labels import views


urlpatterns = [
    path('', views.IndexLabelsView.as_view(), name="all_labels"),
    path('create/', views.CreateLabelView.as_view(), name="create_label"),
    path('<int:label_id>/update/', views.UpdateLabelView.as_view(), name="update_label"),
    path('<int:label_id>/delete/', views.DeleteLabelView.as_view(), name="delete_label"),
]
