from django.shortcuts import render

from catalog.models import Product


# Create your views here.

def home(request):
    """ Renders the home page"""

    context = {
        'object_list': Product.objects.all(),
        'title': 'Главная'
    }
    return render(request, 'catalog/home.html', context)


def contacts(request):
    """ Renders the contacts page """
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        print(f"Name: {name}, Phone: {phone}, Message: {message}")

    context = {
        'title': "Контакты"
    }
    return render(request, 'catalog/contacts.html', context)


def product_detail(request, pk):
    """ Renders the product page """
    context = {
        'object': Product.objects.get(pk=pk)

    }
    return render(request, 'catalog/product_detail.html', context)

