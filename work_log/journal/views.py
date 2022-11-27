from django.shortcuts import render
from django.http import HttpResponse


def home_page(request):
    """ Домашняя страница. """
    return render(request, 'index.html', {
        "new_item_text": request.POST.get('item_text', )
    })
