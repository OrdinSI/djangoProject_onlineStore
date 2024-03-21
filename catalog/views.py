from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.forms import inlineformset_factory
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView, DeleteView

from catalog.forms import ProductForm, VersionForm, VersionFormSet
from catalog.models import Product, Version


class ProductListView(ListView):
    model = Product

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data['title'] = "Продукты"
        products = context_data['object_list']

        for product in products:
            active_version = product.versions.filter(is_active=True).first()
            product.active_version = active_version
        return context_data


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    login_url = 'users:login'


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:product_list')
    login_url = 'users:login'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        VersionFormset = inlineformset_factory(Product, Version, form=VersionForm, formset=VersionFormSet, extra=1)
        if self.request.method == 'POST':
            context_data['formset'] = VersionFormset(self.request.POST)
        else:
            context_data['formset'] = VersionFormset()

        return context_data

    def form_valid(self, form):
        formset = self.get_context_data()['formset']
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()

        if formset.is_valid():
            formset.instance = self.object
            formset.save()
            return super().form_valid(form)
        else:
            return self.form_invalid(form)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    login_url = 'users:login'

    def get_success_url(self):
        return reverse('catalog:product_update', args=[self.kwargs.get('pk')])

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        VersionFormset = inlineformset_factory(Product, Version, form=VersionForm, formset=VersionFormSet, extra=1)
        if self.request.method == 'POST':
            context_data['formset'] = VersionFormset(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = VersionFormset(instance=self.object)

        return context_data

    def form_valid(self, form):
        formset = self.get_context_data()['formset']
        self.object = form.save()

        if formset.is_valid():
            formset.instance = self.object
            formset.save()
            return super().form_valid(form)
        else:
            return self.form_invalid(form)


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    success_url = reverse_lazy('catalog:product_list')
    login_url = 'users:login'



class ContactsView(TemplateView):
    template_name = 'catalog/contacts.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Контакты"
        return context

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        print(f"Name: {name}, Phone: {phone}, Message: {message}")
        return super().get(request, *args, **kwargs)
