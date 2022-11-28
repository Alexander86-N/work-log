from django.shortcuts import render, redirect
from work_log.journal.models import Item


def home_page(request):
    """ Домашняя страница. """
    if request.method == "POST":
        Item.objects.create(text=request.POST['item_text'])
        return redirect("/")
    return render(request, 'index.html')
