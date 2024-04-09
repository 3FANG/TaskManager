from django.contrib.auth import get_user_model

from task_manager.tasks.models import Tasks
from task_manager.statuses.models import Statuses


User = get_user_model()


class SetUpMixin:
    """Миксин, создающий все необходимые сущности и наборы данных."""
    def setUp(self):
        self.user_1 = User.objects.create_user(
            username='1ONE',
            password='K3GauRS1'
        )
        self.user_2 = User.objects.create_user(
            username='DonUn',
            password='9o3rQaAc'
        )
        self.status_1 = Statuses.objects.create(name='Status1')
        self.status_2 = Statuses.objects.create(name='Status2')
        self.task = Tasks.objects.create(
            name="Task",
            description="Description",
            executor=self.user_2,
            status=self.status_1,
            author=self.user_1
        )
        self.create_form_data = [
            {
                "name": "Task1",
                "description": "Task_description1",
                "executor": self.user_2.id,
                "author": self.user_1.id,
                "status": self.status_1.id
            },
            {
                "name": "Task2",
                "description": "Task_description2",
                "executor": self.user_1.id,
                "author": self.user_1.id,
                "status": self.status_2.id
            },
            {
                "name": "Task3",
                "description": "Task_description3",
                "author": self.user_1.id,
                "status": self.status_1.id
            }
        ]
        self.update_form_data = [
            {
                "name": "New Task1",
                "description": "New Task_description1",
                "status": self.task.status.id,
                "executor": self.task.executor.id,
            },
            {
                "name": "New Task2",
                "description": "new_task_desc",
                "status": self.status_2.id,
                "executor": ''
            }
        ]