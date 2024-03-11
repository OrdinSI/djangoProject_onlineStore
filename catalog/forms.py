from django import forms

from catalog.models import Product
from config import settings


class ProductForm(forms.ModelForm):
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
