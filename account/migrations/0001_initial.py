# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Expense'
        db.create_table('account_expense', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('amount', self.gf('django.db.models.fields.IntegerField')(max_length=25)),
            ('description', self.gf('django.db.models.fields.TextField')(max_length=500)),
            ('date', self.gf('django.db.models.fields.DateField')(max_length=300)),
            ('time', self.gf('django.db.models.fields.TimeField')(max_length=300)),
            ('comment', self.gf('django.db.models.fields.TextField')(max_length=500)),
        ))
        db.send_create_signal('account', ['Expense'])


    def backwards(self, orm):
        # Deleting model 'Expense'
        db.delete_table('account_expense')


    models = {
        'account.expense': {
            'Meta': {'object_name': 'Expense'},
            'amount': ('django.db.models.fields.IntegerField', [], {'max_length': '25'}),
            'comment': ('django.db.models.fields.TextField', [], {'max_length': '500'}),
            'date': ('django.db.models.fields.DateField', [], {'max_length': '300'}),
            'description': ('django.db.models.fields.TextField', [], {'max_length': '500'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'time': ('django.db.models.fields.TimeField', [], {'max_length': '300'})
        }
    }

    complete_apps = ['account']