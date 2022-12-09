from django.shortcuts import render, redirect
from work_log.journal.models import Item


def home_page(request):
    """ Домашняя страница. """
    return render(request, 'index.html')

def view_list(request):
    """ Представление списка. """
    items = Item.objects.all()
    return render(request, 'list.html', {'items': items})

def new_list(request):
    """ Новый список. """
    Item.objects.create(text=request.POST['item_text'])
    return redirect("/lists/new_url/")
