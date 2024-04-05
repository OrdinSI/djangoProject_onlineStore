from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.forms import inlineformset_factory
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView, DeleteView

from catalog.forms import ProductForm, VersionForm, VersionFormSet, ModeratorProductForm
from catalog.models import Product, Version, Category
from catalog.services import get_model


class ProductListView(ListView):
    """Product list view"""
    model = Product

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.groups.filter(name='moderator').exists():
            return queryset
        else:
            return queryset.filter(is_published=True)

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data['show_create_button'] = not self.request.user.groups.filter(name='moderator').exists()
        context_data['title'] = "Продукты"
        products = context_data['object_list']

        for product in products:
            active_version = product.versions.filter(is_active=True).first()
            product.active_version = active_version
        return context_data


class ProductDetailView(LoginRequiredMixin, DetailView):
    """Product detail view"""
    model = Product
    login_url = 'users:login'

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['show_detail_button'] = self.request.user.groups.filter(name='moderator').exists()
        return context_data


class ProductCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    """Product create view"""
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:product_list')
    login_url = 'users:login'

    def test_func(self):
        return not self.request.user.groups.filter(name='moderator').exists()

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        VersionFormset = inlineformset_factory(Product, Version, form=VersionForm, formset=VersionFormSet, extra=1)
        if self.request.method == 'POST':
            context_data['formset'] = VersionFormset(self.request.POST)
        else:
            context_data['formset'] = VersionFormset()
        context_data['show_create_button'] = not self.request.user.groups.filter(name='moderator').exists()
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

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    """Product edit view."""
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
        context_data['request'] = self.request
        context_data['show_create_button'] = not self.request.user.groups.filter(name='moderator').exists()
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

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def get_form_class(self):
        if self.request.user.has_perm('catalog.set_published') and not self.request.user.is_superuser:
            return ModeratorProductForm
        else:
            return ProductForm


class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Product delete view."""
    model = Product
    success_url = reverse_lazy('catalog:product_list')
    login_url = 'users:login'

    def test_func(self):
        return not self.request.user.groups.filter(name='moderator').exists()


class ContactsView(TemplateView):
    """Contacts view."""
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


class CategoryListView(LoginRequiredMixin, ListView):
    """Category list view."""
    model = Category

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = get_model(Category, 'categories')
        context['categories'] = categories
        return context
