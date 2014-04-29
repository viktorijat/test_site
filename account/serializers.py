from account.models import Expense
from rest_framework import serializers


class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = (
            'id',
            'expense_name',
            'amount',
            'description',
            'date',
            'time',
            'comment',
            'user'
        )
