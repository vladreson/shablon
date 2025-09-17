from django import forms
from .models import Product

FORBIDDEN_WORDS = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево',
                   'бесплатно', 'обман', 'полиция', 'радар']


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

    def clean_name(self):
        name = self.cleaned_data['name'].lower()
        for word in FORBIDDEN_WORDS:
            if word in name:
                raise forms.ValidationError(f'Название содержит запрещенное слово: "{word}"')
        return self.cleaned_data['name']

    def clean_description(self):
        description = self.cleaned_data['description'].lower()
        for word in FORBIDDEN_WORDS:
            if word in description:
                raise forms.ValidationError(f'Описание содержит запрещенное слово: "{word}"')
        return self.cleaned_data['description']

    def clean_price(self):
        price = self.cleaned_data['price']
        if price < 0:
            raise forms.ValidationError('Цена не может быть отрицательной')
        return price

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            if field_name == 'is_published':
                field.widget.attrs['class'] = 'form-check-input'
            elif field_name == 'description':
                field.widget.attrs['rows'] = 4