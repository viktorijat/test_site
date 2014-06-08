from django.shortcuts import render
from django.conf import settings
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
from django.views.decorators.csrf import csrf_exempt
from django.views import generic

from  django.utils.decorators import method_decorator
from account.models import Expense
from datetime import date, timedelta
from django.db import IntegrityError
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import Context, loader
from django.contrib.auth import authenticate, login
import types
from django.views.decorators.csrf import csrf_exempt

from django.utils.dateformat import DateFormat, TimeFormat
from django.template.response import TemplateResponse
from account.models import Expense
from account.serializers import ExpenseSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response




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

                response = {'success': True, 'name': request.POST["name"], 'password': request.POST["password"],
                            'note': "logged in"}

            except:

                response = {'success': False, 'name': request.POST["name"], 'password': request.POST["password"],
                            'note': "password is bad"}
                #return HttpResponseRedirect('/home/')

    #return HttpResponseRedirect('profile', response)
    return HttpResponse(simplejson.dumps(response), mimetype='application/json')


def register_form_event(request):
    response = {'success': False}

    try:

        user = User.objects.get(username=request.POST["name"])
        response = {'success': False, 'name': request.POST["name"], 'password': request.POST["password"],
                    'note': "this user exists"}

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

                response = {'success': True, 'name': request.POST["name"], 'password': request.POST["password"],
                            'note': "user is created"}
                #return render_to_response(response, 'add_new_expense.html')
                #return HttpResponseRedirect(reverse('profile'), response)
                return render(request, 'add_new_expense.html', response)

            else:

                response = {'success': False, 'name': request.POST["name"], 'password': request.POST["password"],
                            'note': "the two passwords dont match"}

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


@csrf_exempt
def profile(request):
    return render_to_response('profile.html', locals(),
                              context_instance=RequestContext(request))


@csrf_exempt
def add_new_expense_url(request):
    response = {'success': True, 'note': "add expense"}
    return HttpResponse(simplejson.dumps(response), mimetype='application/json')


@csrf_exempt
def add_new_expense(request):
    return render_to_response('add_new_expense.html', locals(),
                              context_instance=RequestContext(request))


@csrf_exempt
def go_back_url(request):
    response = {'success': True, 'note': "add expense"}
    return HttpResponse(simplejson.dumps(response), mimetype='application/json')


@csrf_exempt
def logout_user(request):

    response = {'success': False}
    if request.user.is_authenticated():
        logout(request)
        response = {'success': True, 'note': "user is logged out"}
    else:
        response = {'success': False, 'note': "user isnt logged out"}

    return HttpResponse(simplejson.dumps(response), mimetype='application/json')


@csrf_exempt
def details(request):
    response = {'success': False, 'note': "user is not authenticated"}
    if request.user.is_authenticated():
        response = {'success': True, 'note': "user is authenticated"}

    return HttpResponse(simplejson.dumps(response), mimetype='application/json')


@csrf_exempt
def detail_view(request):
    current_user = request.user
    current_user_id = current_user.id
    template = loader.get_template("detail_view.html")
    exp_list = ((Expense.objects.filter(user=current_user_id)).order_by('-date')).order_by('-time')
    response = {'success': True, 'exp_list': exp_list}
    return render_to_response('detail_view.html', locals(),
                              context_instance=RequestContext(request))



@csrf_exempt
def filter_all_func(request):

    current_user = request.user
    current_user_id = current_user.id

    submitted_date_one = request.POST.get('date_one', False)
    submitted_date_two = request.POST.get('date_two', False)

    first = request.POST.get('first_amount', False)
    second = request.POST.get('second_amount', False)
    submitted_name = request.POST.get('name_received', False)
    submitted_desc = request.POST.get('desc_received', False)
    submitted_comm = request.POST.get('comm_received', False)

    kwargs = {}
    if submitted_date_one is not "":
        year_first = int(str((submitted_date_one.split("-")[0])).zfill(4))
        month_first = int(str((submitted_date_one.split("-")[1])).zfill(2))
        day_first = int(str((submitted_date_one.split("-")[2])).zfill(2))
        kwargs['date_gte'] = datetime.date(year_first, month_first, day_first)

    if submitted_date_two is not "":
        year_second = int(str((submitted_date_two.split("-")[0])).zfill(4))
        month_second = int(str((submitted_date_two.split("-")[1])).zfill(2))
        day_second = int(str((submitted_date_two.split("-")[2])).zfill(2))
        kwargs['date_lte'] = datetime.date(year_second, month_second, day_second)

    if first is not "":
        kwargs['amount_gte'] = first

    if second is not "":
        kwargs['amount_lte'] = second

    if submitted_name is not "":
        kwargs['expense_name__contains'] = submitted_name

    if submitted_desc is not "":
        kwargs['description__contains'] = submitted_desc

    if submitted_comm is not "":
        kwargs['comment__contains'] = submitted_comm

    print(kwargs)

    res = Expense.objects.filter(**kwargs)


    if res:

        all_list = []
        for obj in res:

            id = str(obj.id)
            name = str(obj.expense_name)
            amount = str(obj.amount)
            description = str(obj.description)
            date = str(obj.date)
            time = str(obj.time)
            comment = str(obj.comment)
            item = {'id': id, 'name': name, 'amount': amount, 'description': description, 'date': date, 'time': time, 'comment': comment}
            all_list.append(item)

        response = {'success': True, 'all_list': all_list, 'note': "expense result"}

    else:
        response = {'success': False, 'note': "no such expense"}

    return HttpResponse(simplejson.dumps(response), mimetype='application/json')

'''
class DetailView(generic.ListView):

    model = Expense
    template_name = "detail_view.html"
    context_object_name = 'exp_list'

    @csrf_exempt
    def get_queryset(self):

        current_user = self.request.user
        current_user_id = current_user.id

        exp_list = ((Expense.objects.filter(user=current_user_id)).order_by('-date')).order_by('-time')
        return exp_list
        #response = {"exp_list": exp_list}
        #return render(self.request, "detail_view.html", exp_list)
        #response = {'success': True, 'exp_list': exp_list, 'note': "user is authenticated"}

        #return TemplateResponse(self.request, "detail_view.html", response)
        #response = {'success': False, 'exp_list': exp_list, 'note': "no such expense"}
        #return HttpResponse(simplejson.dumps(response), mimetype='application/json')


'''


class DetailView(APIView):

    model = Expense
    template_name = "detail_view.html"
    context_object_name = 'exp_list'

    @csrf_exempt
    def get_queryset(self):

        current_user = self.request.user
        current_user_id = current_user.id
        expenses = ((Expense.objects.filter(user=current_user_id)).order_by('-date')).order_by('-time')
        exp_list = ExpenseSerializer(expenses, many=True)
        return Response(exp_list)






def delete_expense(request):
    response = {'success': False, 'note': "field is blank"}
    current_user = request.user
    current_user_id = current_user.id

    exp_id = request.POST['exp_id']
    e = (Expense.objects.get(id=exp_id, user=current_user_id))
    if e is not None:
        e.delete()
        response = {'success': True, 'note': "expense deleted"}
    else:
        response = {'success': False, 'note': "no such expense"}

    return HttpResponse(simplejson.dumps(response), mimetype='application/json')




def edit_expense(request):
    response = {'success': False, 'note': "field is blank"}
    current_user = request.user
    current_user_id = current_user.id
    now = datetime.datetime.now()
    date = '-'.join([str(now.year).zfill(4), str(now.month).zfill(2), str(now.day).zfill(2)])
    time = ':'.join([str(now.hour).zfill(2), str(now.minute).zfill(2), str(now.second).zfill(2)])

    exp_id = request.POST['exp_id']
    e = (Expense.objects.get(id=exp_id, user=current_user_id))
    if e:
        e.expense_name = request.POST['exp_name']
        e.amount = request.POST['exp_amount']
        e.description = request.POST['exp_descr']
        e.comment = request.POST['exp_comment']
        e.date = date
        e.time = time
        e.save()
        response = {'success': True, 'exp_id': exp_id, 'expense_name': request.POST['exp_name'],
                    'amount': request.POST['exp_amount'],
                    'description': request.POST['exp_descr'], 'comment': request.POST['exp_comment'],
                    'date': date, 'time': time, 'note': "expense edited"}
    else:
        response = {'success': False, 'note': "no such expense"}

    return HttpResponse(simplejson.dumps(response), mimetype='application/json')


@csrf_exempt
def calculate_day(request):
    avg = 0
    response = {'success': False, 'avg': avg, 'note': "no entries"}
    current_user = request.user
    current_user_id = current_user.id


    e = list(Expense.objects.filter(user=current_user_id))
    if e:
        days = []
        for enrty in e:
            this_date = enrty.date
            if this_date not in days:
                days.append(this_date)

        amounts = []
        for day in days:
            a = list(Expense.objects.filter(user=current_user_id, date=day))
            suma = 0
            if a:
                for entry2 in a:
                    suma += entry2.amount
            amounts.append(suma)

        sum3 = 0
        for s3 in amounts:
            sum3 += s3

        avg = sum3 / len(amounts)
        response = {'success': True, 'avg': avg, 'note': "avg calculated"}

    else:
        response = {'success': False, 'avg': avg, 'note': "no entries"}

    return HttpResponse(simplejson.dumps(response), mimetype='application/json')


@csrf_exempt
def calculate_this_week(request):

    now = datetime.datetime.now()

    date = '-'.join([str(now.year).zfill(4), str(now.month).zfill(2), str(now.day).zfill(2)])
    time = ':'.join([str(now.hour).zfill(2), str(now.minute).zfill(2), str(now.second).zfill(2)])


    today = datetime.datetime.today().weekday() + 1
    first_week_day = now - datetime.timedelta(days=today - 1)
    print(first_week_day)

    first_date = '-'.join(
        [str(first_week_day.year).zfill(4), str(first_week_day.month).zfill(2), str(first_week_day.day).zfill(2)])
    rest = 7 - today
    last_week_day = now + datetime.timedelta(days=rest)
    print(last_week_day)

    last_date = '-'.join(
        [str(last_week_day.year).zfill(4), str(last_week_day.month).zfill(2), str(last_week_day.day).zfill(2)])
    e = list(Expense.objects.filter(date__range=(first_date, last_date)))
    total = 0
    if e:
        for entry in e:
            total += entry.amount
        response = {'success': True, 'total': total, 'note': "total for this week calculated"}
    else:
        response = {'success': False, 'total': total, 'note': "no entries"}

    return HttpResponse(simplejson.dumps(response), mimetype='application/json')



