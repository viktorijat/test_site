from account.models import Expense
from account.serializers import ExpenseSerializer
from django.http import Http404
from django.views.generic import APIView
from rest_framework.views import APIView
from rest_framework.response import Response


class ExpenseDetail(APIView):

    def get_queryset(self):

        current_user = self.request.user
        current_user_id = current_user.id
        expenses = ((Expense.objects.filter(user=current_user_id)).order_by('-date')).order_by('-time')
        serialized_expenses = ExpenseSerializer(expenses, many=True)
        return Response(serialized_expenses)




