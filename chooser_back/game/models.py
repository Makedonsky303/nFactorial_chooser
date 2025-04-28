from django.db import models
    
class Participant(models.Model):
    color = models.CharField(max_length=20)
    x = models.FloatField(default=0)
    y = models.FloatField(default=0)
    is_active = models.BooleanField(default=True)
    has_completed_task = models.BooleanField(default=False)

    def __str__(self):
        return self.color

class Game(models.Model):
    participants = models.ManyToManyField(Participant, related_name='games_participated')
    winner = models.ForeignKey(Participant, null=True, blank=True, on_delete=models.SET_NULL, related_name='games_won')

    game_mode = models.CharField(max_length=20, choices=[('simple', 'Simple'), ('withTasks', 'With Tasks')], default='withTasks')
    elimination_mode = models.BooleanField(default=True)
    task_difficulty = models.CharField(max_length=10, choices=[('easy', 'Easy'), ('medium', 'Medium'), ('hard', 'Hard')], default='easy')
    time_limit_seconds = models.IntegerField(default=5)

    def __str__(self):
        return f"Game {self.id}"
    


