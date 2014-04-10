# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Expence'
        db.create_table('expence_expence', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('note', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('value', self.gf('django.db.models.fields.IntegerField')(max_length=25)),
        ))
        db.send_create_signal('expence', ['Expence'])


    def backwards(self, orm):
        # Deleting model 'Expence'
        db.delete_table('expence_expence')


    models = {
        'expence.expence': {
            'Meta': {'object_name': 'Expence'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'note': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'value': ('django.db.models.fields.IntegerField', [], {'max_length': '25'})
        }
    }

    complete_apps = ['expence']