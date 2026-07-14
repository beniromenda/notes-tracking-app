from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'),name='login'),
    path('logout/',auth_views.LogoutView.as_view(),name='logout'),
    path('', views.NoteListView.as_view(), name='note_list'),
    path('note_create/', views.NoteCreateView.as_view(), name='note_create'),
    path('<int:pk>/update/',views.NoteUpdateView.as_view(),name='note_update'),
    path('<int:pk>/delete/', views.NoteDeleteView.as_view(), name='note_delete')
]