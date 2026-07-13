from django.shortcuts import render,redirect,get_object_or_404
from .models import Note
from .forms import NoteForm
from django.views.generic import  CreateView, UpdateView, DeleteView, ListView
from django.urls import reverse_lazy


# Create your views here.
class NoteListView(ListView):
    model=Note
    template_name='notes/list.html'
    context_object_name='notes'

class NoteCreateView(CreateView):
    model=Note
    form_class=NoteForm
    template_name='notes/create.html'
    success_url=reverse_lazy('note_list')

class NoteUpdateView(UpdateView):
    model=Note
    form_class=NoteForm
    template_name='notes/update.html'
    success_url=reverse_lazy('note_list')

class NoteDeleteView(DeleteView):
    model=Note
    template_name='notes/note_confirm_delete.html'
    success_url=reverse_lazy('note_list')
