from django.db import models

class TaskCategory(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Task(models.Model):
    category = models.ForeignKey(TaskCategory, on_delete=models.CASCADE, related_name="tasks")
    difficulty = models.CharField(max_length=50, choices=[('easy', 'Легкая'), ('medium', 'Средняя'), ('hard', 'Сложная')])
    description = models.TextField()

    def __str__(self):
        return f"{self.difficulty} - {self.description[:30]}..."

