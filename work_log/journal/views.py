from django.shortcuts import render, redirect
from work_log.journal.models import Item


def home_page(request):
    """ Домашняя страница. """
    if request.method == "POST":
        Item.objects.create(text=request.POST['item_text'])
        return redirect("/lists/new_url")
    return render(request, 'index.html')

def view_list(request):
    """ Представление списка. """
    items = Item.objects.all()
    return render(request, 'list.html', {'items': items})
