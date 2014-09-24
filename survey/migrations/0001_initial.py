# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Survey'
        db.create_table(u'survey_survey', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(db_index=True)),
        ))
        db.send_create_signal(u'survey', ['Survey'])

        # Adding model 'Page'
        db.create_table(u'survey_page', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('page_num', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('survey', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['survey.Survey'])),
        ))
        db.send_create_signal(u'survey', ['Page'])

        # Adding unique constraint on 'Page', fields ['page_num', 'survey']
        db.create_unique(u'survey_page', ['page_num', 'survey_id'])

        # Adding model 'Question'
        db.create_table(u'survey_question', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('page', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['survey.Page'])),
            ('question_text', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('position', self.gf('django.db.models.fields.IntegerField')()),
            ('type', self.gf('django.db.models.fields.CharField')(default='checkbox', max_length=20)),
        ))
        db.send_create_signal(u'survey', ['Question'])

        # Adding model 'Answer'
        db.create_table(u'survey_answer', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['survey.Question'])),
            ('answer_text', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('score', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'survey', ['Answer'])

        # Adding model 'Result'
        db.create_table(u'survey_result', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('survey', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['survey.Survey'])),
            ('summary', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('min_score', self.gf('django.db.models.fields.IntegerField')()),
            ('max_score', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'survey', ['Result'])


    def backwards(self, orm):
        # Removing unique constraint on 'Page', fields ['page_num', 'survey']
        db.delete_unique(u'survey_page', ['page_num', 'survey_id'])

        # Deleting model 'Survey'
        db.delete_table(u'survey_survey')

        # Deleting model 'Page'
        db.delete_table(u'survey_page')

        # Deleting model 'Question'
        db.delete_table(u'survey_question')

        # Deleting model 'Answer'
        db.delete_table(u'survey_answer')

        # Deleting model 'Result'
        db.delete_table(u'survey_result')


    models = {
        u'survey.answer': {
            'Meta': {'object_name': 'Answer'},
            'answer_text': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['survey.Question']"}),
            'score': ('django.db.models.fields.IntegerField', [], {})
        },
        u'survey.page': {
            'Meta': {'unique_together': "(('page_num', 'survey'),)", 'object_name': 'Page'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'page_num': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'survey': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['survey.Survey']"})
        },
        u'survey.question': {
            'Meta': {'ordering': "['position']", 'object_name': 'Question'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'page': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['survey.Page']"}),
            'position': ('django.db.models.fields.IntegerField', [], {}),
            'question_text': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'type': ('django.db.models.fields.CharField', [], {'default': "'checkbox'", 'max_length': '20'})
        },
        u'survey.result': {
            'Meta': {'object_name': 'Result'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'max_score': ('django.db.models.fields.IntegerField', [], {}),
            'min_score': ('django.db.models.fields.IntegerField', [], {}),
            'summary': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'survey': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['survey.Survey']"})
        },
        u'survey.survey': {
            'Meta': {'ordering': "['-created_at']", 'object_name': 'Survey'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '150'})
        }
    }

    complete_apps = ['survey']