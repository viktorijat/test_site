from django.shortcuts import render
from django.http import HttpResponse
import json as simplejson
from django.shortcuts import *
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.models import User


def home(request):

    return render_to_response('index.html', locals(),
                         context_instance=RequestContext(request))


def test(request):

    response = {'success': False}
    if request.method == "POST":
        try:
            user = authenticate(username=request.POST["name"], password=request.POST["password"])

        except:

            new_user = User.objects.create_user(
                username=request.POST['name'],
                password=request.POST['password'],
            )
            new_user.full_clean()
            new_user.save()
            user = authenticate(username=request.POST["name"], password=request.POST["password"])
            print(new_user)

        print("hello")
        response = {'success': True, 'name': request.POST["name"], 'password': request.POST["password"]}
    return HttpResponse(simplejson.dumps(response), mimetype='application/json')

