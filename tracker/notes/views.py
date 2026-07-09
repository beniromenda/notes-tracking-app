from django.shortcuts import render,redirect
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