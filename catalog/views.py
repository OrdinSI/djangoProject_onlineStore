from django.shortcuts import render


# Create your views here.

def home(request):
    """ Renders the home page"""
    return render(request, 'catalog/home.html')


def contacts(request):
    """ Renders the contacts page """
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        print(f"Name: {name}, Phone: {phone}, Message: {message}")
    return render(request, 'catalog/contacts.html')
