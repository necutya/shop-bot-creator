import os

from django import forms
from django.core.exceptions import ValidationError

from bots_management.services import get_bot_by_slug
from products.models import Category, Product, ProductPhoto


class CsvFileField(forms.FileField):
    def validate(self, value):
        # First run the parent class' validation routine
        super().validate(value)
        # Run our own file extension check
        file_extension = os.path.splitext(value.name)[1]
        if file_extension != '.xls' and file_extension != '.xlsx':
            raise ValidationError(
                'Дозволені лише файли формату .xls и .xlsx',
                code='invalid'
            )


class ProductForm(forms.ModelForm):
    """
    Form to create a Post model object
    """
    name = forms.CharField(
        label='Назва',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )

    description = forms.CharField(
        label='Опис',
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': '5', 'cols': '25'
        }),
    )

    amount = forms.IntegerField(
        label='Кількість',
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
        }),
    )

    price = forms.DecimalField(
        label='Ціна',
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': "0.01"
        }),
    )

    discount = forms.DecimalField(
        label='Знижки %',
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': "0.01"
        }),
    )

    article = forms.CharField(
        label='Артикул',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )

    visible = forms.BooleanField(
        label='Видимий товар',
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-control',
            'style': 'width:20px;height:20px;display:inline;'
        }),
    )

    categories = forms.ModelMultipleChoiceField(
        label='Категорії',
        widget=forms.SelectMultiple(attrs={'class': 'form-control select2-search js-example-basic-multiple'}),
        queryset=Category.objects
    )

    url = forms.CharField(
        label='Посилання на продукт в інтернет магазині',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )

    main_photo = forms.ImageField(
        label="Головне зображення",
        required=False,
        widget=forms.FileInput(
            attrs={
                'class': "form-control",
            }
        )
    )

    # other_photos = forms.FileField(
    #     label="Інші зображення",
    #     widget=forms.ClearableFileInput(
    #         attrs={
    #             'class': "form-control",
    #         }
    #     )
    # )

    def __init__(self, *args, **kwargs):
        self.bot_slug = kwargs.pop('bot_slug')
        super().__init__(*args, **kwargs)
        self.fields['categories'].queryset = Category.objects.filter(bot__slug=self.bot_slug)

    def save(self, commit=True):
        product = super().save(commit=False)
        product.bot = get_bot_by_slug(self.bot_slug)
        if commit:
            product.save()
            if self.cleaned_data["main_photo"]:
                product.photos.add(ProductPhoto(image=self.cleaned_data["main_photo"], is_main=True), bulk=False)
            else:
                product.photos.add(ProductPhoto(is_main=True), bulk=False)
            self.save_m2m()

        return product

    class Meta:
        fields = (
            'name',
            'description',
            'amount',
            'price',
            'discount',
            'visible',
            'categories',
            'url',
            'article',
        )
        model = Product


class CategoryForm(forms.ModelForm):
    name = forms.CharField(
        label='Назва',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )

    description = forms.CharField(
        label='Опис',
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': '5', 'cols': '25'
        }),
    )

    def __init__(self, *args, **kwargs):
        self.bot_slug = kwargs.pop('bot_slug')
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        category = super().save(commit=False)
        category.bot = get_bot_by_slug(self.bot_slug)
        if commit:
            category.save()
            self.save_m2m()

        return category

    class Meta:
        fields = (
            'name',
            'description',
        )
        model = Category


class UploadFileForm(forms.Form):
    file = CsvFileField(
        label='Файл со списком товаров',
        widget=forms.FileInput(attrs={'class': 'custom-file-input', 'type': 'file', "id": "customFile"}),
        required=True,
    )
