from django.shortcuts import render,redirect,get_object_or_404
from .models import Note
from .forms import NoteForm
from django.views.generic import  CreateView, UpdateView, DeleteView, ListView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

#create your views here
class NoteListView(LoginRequiredMixin, ListView):
    model=Note
    template_name='notes/list.html'
    context_object_name='notes'
    #Restricting views to logged in users
    def get_queryset(self):
        return Note.objects.filter(user=self.request.user)

class NoteCreateView(LoginRequiredMixin, CreateView):
    model=Note
    form_class=NoteForm
    template_name='notes/create.html'
    success_url=reverse_lazy('note_list')

    #When the user signs in, we need to auto assign this note to the specific user
    def form_valid(self, form):
        form.instance.user= self.request.user
        return super().form_valid(form)

class NoteUpdateView(UpdateView):
    model=Note
    form_class=NoteForm
    template_name='notes/update.html'
    success_url=reverse_lazy('note_list')

class NoteDeleteView(DeleteView):
    model=Note
    template_name='notes/note_confirm_delete.html'
    success_url=reverse_lazy('note_list')
