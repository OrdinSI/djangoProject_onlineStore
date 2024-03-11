from django import forms

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

    def clean_is_active(self):
        is_active = self.cleaned_data.get('is_active')

        if is_active:
            active_versions = Version.objects.filter(is_active=True).exclude(pk=self.instance.pk)
            if active_versions.exists():
                raise forms.ValidationError(f'Может быть активна только одна версия продукта"')
        return is_active
