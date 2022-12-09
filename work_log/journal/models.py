from django.db import models


class List(models.Model):
    """ Модель списка """
    pass


class Item(models.Model):
    """ Элемент списка Рабочего журнала """
    text = models.TextField(default='')
    list = models.ForeignKey(List,
                             on_delete=models.CASCADE,
                             default=None)
