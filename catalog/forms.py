from django import forms
from django.forms import BaseInlineFormSet

from catalog.models import Product, Version
from config import settings


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'


class ProductForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Product
        exclude = ('created_at', 'updated_at')

    def clean_name(self):
        name = self.cleaned_data.get('name')
        forbidden_words = settings.FORBIDDEN_WORDS

        for word in forbidden_words:
            if word.lower() in name.lower():
                raise forms.ValidationError(f'Название не должно содержать слово "{word}"')
        return name

    def clean_description(self):
        description = self.cleaned_data.get('description')
        forbidden_words = settings.FORBIDDEN_WORDS

        for word in forbidden_words:
            if word.lower() in description.lower():
                raise forms.ValidationError(f'Описание не должно содержать слово "{word}"')
        return description


class VersionForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Version
        fields = ('number', 'name', 'is_active')


class VersionFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()

        active_versions = [form.cleaned_data for form in self.forms if form.cleaned_data.get('is_active')
                           and not form.cleaned_data.get('DELETE', False)]

        if len(active_versions) > 1:
            raise forms.ValidationError('Может быть активна только одна версия продукта.')

        if self.has_changed():
            if len(active_versions) == 1:
                active_versions = active_versions[0]
                Version.objects.filter(product_id=self.instance.id, is_active=True).update(is_active=False)

        return active_versions
