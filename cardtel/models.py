from django.db import models

class TestModel(models.Model):

    class Meta:
        db_table = 'test_model'
        app_label = 'cardtel'