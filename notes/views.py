from django.shortcuts import render, get_object_or_404
from notes.models import Note
from django.http import HttpResponseRedirect
from notes.forms import NoteForm
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required


@login_required(login_url='/')
def index_view(request):
	notes = Note.objects.filter(user=request.user).order_by('-timestamp')
	return render(request, 'notes/index.html', {'notes':notes})


@login_required(login_url='/')
def add_note(request):
	id = request.GET.get('id', None)
	if id is not None:
		note = get_object_or_404(Note, id=id)
	else:
		note = None
	if request.method == 'POST':
		if request.POST.get('control') == 'delete':
			note.delete()
			messages.add_message(request, messages.INFO, 'Note Deleted!')
			return HttpResponseRedirect(reverse('notes:index'))
		form = NoteForm(request.POST)
		if form.is_valid():
			current_user = request.user
			current_label = request.POST.get('label')
			current_body = request.POST.get('body')
			if id is not None:
				note.delete()
			Note.objects.create(user=current_user, label=current_label, body= current_body)
			messages.add_message(request, messages.INFO, 'Note Added!')
			return HttpResponseRedirect(reverse('notes:index'))
	else:
		form = NoteForm(instance=note)
	return render(request, 'notes/addnote.html', {'form': form, 'note': note})

