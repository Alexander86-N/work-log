from django.db import models

class Item(models.Model):
    """ Элемент списка Рабочего журнала """
    text = models.TextField(default='')
