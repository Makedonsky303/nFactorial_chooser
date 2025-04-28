from rest_framework import generics
from .models import Task
from .serializers import TaskSerializer
from rest_framework.response import Response

class TaskListView(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

class RandomTaskView(generics.GenericAPIView):
    def get(self, request):
        import random
        task = random.choice(Task.objects.all())
        serializer = TaskSerializer(task)
        return Response(serializer.data)
