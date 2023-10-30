from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt

from .models import NotepadForm, NotepadModel, BotQueue
import json

# XSS POLICE!
def sanitize(text):
    cleaned = text
    ind_list = []

    try:
        for i in range(len(cleaned)):
            if cleaned[i] == '<':
                ind_list.append(i)
            elif cleaned[i] == '>':
                if(len(ind_list) > 0):
                    cleaned = cleaned[:ind_list.pop()] + cleaned[i+1:]
    except:
        pass

    return cleaned

def note(request, **kwargs):
    if request.method == 'GET':
        noteid = kwargs["noteid"]
        text = NotepadModel.objects.get(id=noteid).text
        return render(request, 'submission.html', {'text': json.dumps(text), 'uuid': json.dumps(str(noteid))})
    return redirect("/")

# Create your views here.
def index(request):

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NotepadForm(request.POST)
        # check whether it's valid:
        if form.is_valid():

            # Save the data to db
            text = sanitize(form.cleaned_data['text'])
            form.instance.text = text
            form.save()

            return redirect("note/" + str(form.instance.id))
            

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NotepadForm()

    return render(request, 'home.html', {'form': form})

@csrf_exempt
def sendToGalih(request):

    if request.method == 'POST':

        request_data = json.loads(request.body)
        model = BotQueue(id_queue = request_data['uuid'])
        model.save()
        
    return redirect("/")

def superSecretGalih(request):

    data = BotQueue.objects.all().first()
    BotQueue.objects.all().first().delete()

    return redirect("note/" + data.id_queue)