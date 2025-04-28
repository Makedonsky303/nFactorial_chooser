from django.urls import path
from .views import GameCreateView, PickParticipantView, ParticipantListView,ResetParticipantsView, AssignTaskView, RemoveParticipantView, CompleteTaskView, GameDeleteView

urlpatterns = [
    path('create/', GameCreateView.as_view(), name='create_game'),  
    path('pick/', PickParticipantView.as_view(), name='pick_participant'),  
    path('participants/', ParticipantListView.as_view() , name='get_participants'),
    path('reset/', ResetParticipantsView.as_view(), name='reset-participants'),
    path('assign_task/<int:participant_id>/', AssignTaskView.as_view(), name='assign-task'),
    path('eliminate/<int:participant_id>/', RemoveParticipantView.as_view(), name='remove-participant'),
    path('complete_task/<int:participant_id>/', CompleteTaskView.as_view(), name='complete-task'),
    path('api/game/<int:pk>/delete/', GameDeleteView.as_view(), name='game-delete'),
]
