from django.shortcuts import render,redirect,get_object_or_404
from .models import Note

# Create your views here.
def note_list(request):
    notes=Note.objects.all()
    return render(request, 'notes/list.html',{'notes': notes})

def note_create(request):
    if request.method=='POST':
        Note.objects.create(title=request.POST['title'], content=request.POST['content']);
        return redirect('note_list')
    return render(request, 'notes/create.html')

def note_update(request, pk):
    note=get_object_or_404(Note, pk=pk)
    if request.method=="POST":
        note.title = request.POST['title']
        note.content = request.POST['content']
        note.save()
        return redirect('note_list')
    return render (request, 'notes/update.html',{'note':note})

def note_delete(request, pk):
    note=get_object_or_404(Note, pk=pk)
    note.delete()
    return redirect ('note_list')
