from django.shortcuts import render
from django.http import HttpResponse
import json as simplejson
from django.shortcuts import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
import datetime
import pytz
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from django.views import generic


from account.models import Expense

from django.db import IntegrityError
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import Context, loader
from django.contrib.auth import authenticate, login

from django.views.decorators.csrf import csrf_exempt

from django.utils.dateformat import DateFormat, TimeFormat

def home(request):
    return render_to_response('index.html', locals(),
                              context_instance=RequestContext(request))


def log_in_form_event(request):

    response = {'success': False}
    user = authenticate(username=request.POST["name"], password=request.POST["password"])

    if request.method == "POST":
        try:
            at = User.objects.get(username=request.POST["name"])
        except:

            at = False

        if at == False:

            response = {'success': False, 'name': request.POST["name"], 'password': request.POST["password"],
                        'note': "this username does not exist"}

        else:

            try:

                login(request, user)

                response = {'success': True, 'name': request.POST["name"], 'password': request.POST["password"], 'note': "logged in"}

            except:

                response = {'success': False, 'name': request.POST["name"], 'password': request.POST["password"], 'note': "password is bad"}
                #return HttpResponseRedirect('/home/')

    #return HttpResponseRedirect('profile', response)
    return HttpResponse(simplejson.dumps(response), mimetype='application/json')


def register_form_event(request):


    response = {'success': False}

    try:

        user = User.objects.get(username=request.POST["name"])
        response = {'success': False, 'name': request.POST["name"], 'password': request.POST["password"], 'note': "this user exists"}

    except User.DoesNotExist:

        if request.method == "POST":
            dd = str(datetime.datetime.now(pytz.timezone('US/Pacific'))).split(" ")[0]
            if request.POST['password'] == request.POST['password1']:

                new_user = User.objects.create_user(
                    username=request.POST['name'],
                    email=request.POST['email'],
                    password=request.POST['password'],
                )
                try:
                    new_user.full_clean()
                    new_user.save()
                    user = authenticate(username=request.POST['name'], password=request.POST['password'])
                    login(request, user)

                except IntegrityError:
                    print("ima coek")

                response = {'success': True, 'name': request.POST["name"], 'password': request.POST["password"], 'note': "user is created"}
                #return render_to_response(response, 'profile.html')
                #return HttpResponseRedirect(reverse('profile'), response)
                return render(request, 'profile.html', response)

            else:

                response = {'success': False, 'name': request.POST["name"], 'password': request.POST["password"], 'note': "the two passwords dont match"}

    return HttpResponse(simplejson.dumps(response), mimetype='application/json')


@csrf_exempt
def expense_added(request):

    submitted_amount = float(request.POST["amount"])
    now = datetime.datetime.now()
    date = '-'.join([str(now.year).zfill(4), str(now.month).zfill(2), str(now.day).zfill(2)])
    time = ':'.join([str(now.hour).zfill(2), str(now.minute).zfill(2), str(now.second).zfill(2)])
    current_user = request.user
    print("current user")
    print(current_user)
    current_user_id = current_user.id

    if submitted_amount > 0.0:

        exp = Expense(expense_name=request.POST["expense_name"],
                      amount=request.POST["amount"],
                      description=request.POST["description"],
                      date=date,
                      time=time,
                      comment=request.POST["comment"],
                      user=User.objects.get(username=current_user))

        exp.save()
        response = {'success': True, 'note': "you just added an expense"}

    else:

        response = {'success': False, 'note': "you entered a negative number"}

    return HttpResponse(simplejson.dumps(response), mimetype='application/json')


def profile(request):

    return render_to_response('profile.html', locals(),
                              context_instance=RequestContext(request))
    '''
    def get_queryset(self):
        """Return the last five published questions."""
        return Expense.objects.all()
        #.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]
    '''


@csrf_exempt
def logout_user(request):

    response = {'success': False}
    if request.user.is_authenticated():
        logout(request)
        #return HttpResponseRedirect(reverse('home'), request)
        response = {'success': True, 'name': request.POST["name"], 'password': request.POST["password"], 'note': "user is logged out"}
        return HttpResponseRedirect('home')
    else:
        response = {'success': False, 'name': request.POST["name"], 'password': request.POST["password"], 'note': "user isnt logged out"}
        return HttpResponse(simplejson.dumps(response), mimetype='application/json')


def details(request):

    response = {'success': False, 'note': "user is not authenticated"}
    if request.user.is_authenticated():
        response = {'success': True, 'note': "user is authenticated"}

    return HttpResponse(simplejson.dumps(response), mimetype='application/json')



def detail_view(request):

    return render_to_response('detail_view.html', locals(),
                              context_instance=RequestContext(request))

    '''
    current_user = request.user

    expense_name = Expense.expense_name
    amount = Expense.amount
    description = Expense.description
    date = Expense.date
    time = Expense.time
    comment = Expense.comment
    user = Expense.user
    '''