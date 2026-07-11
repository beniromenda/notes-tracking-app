from django.shortcuts import render,redirect,get_object_or_404
from .models import Note
from .forms import NoteForm

# Create your views here.
def note_list(request):
    notes=Note.objects.all()
    return render(request, 'notes/list.html',{'notes': notes})

def note_create(request):
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('note_list')
    else:
        form = NoteForm()

    return render(request, 'notes/create.html', {'form': form})

def note_update(request, pk):
    note=get_object_or_404(Note, pk=pk)

    if request.method=="POST":
        form=NoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            return redirect('note_list')
    else:
        form=NoteForm(instance=note)
    
    return render (request, 'notes/update.html',{'form':form, 'note':note})

def note_delete(request,pk):
    note=get_object_or_404(Note, pk=pk)
    note.delete()
    return redirect ('note_list')
