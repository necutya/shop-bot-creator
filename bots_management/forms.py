from django import forms
from django.contrib.auth import get_user_model
from django.utils.text import slugify

from bots_management.models import Bot
from administration.models import Country, DeliveryType, PaymentType, Currency
from bots_management.utils import unique_slug_generator


class BotForm(forms.ModelForm):
    name = forms.CharField(
        label='Назва бота',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        help_text="Назва бота лише для відображення на сайті",
        error_messages={'unique': 'Бот с такою назвою вже існує'}
    )

    token = forms.CharField(
        label='Телеграм токен',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        help_text="Токен має бути унікальним для кожного бота",
        error_messages={'unique': 'Бот с таким токеном вже існує'}
    )

    description = forms.CharField(
        label='Опис',
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control modal__field',
            'id': 'i_description'
        }),
        help_text="Опис бота лише для відображення на сайті"
    )

    telegram_operator = forms.CharField(
        label='Модератори',
        widget=forms.TextInput(attrs={'class': 'form-control modal__field',
                                      'id': 'i_title'}, ),
        help_text="Нікнейм модератора в телеграмі без символа @. Якщо не бажаєте додавати модераторів, то залиште це поле пустим.",
        required=True,
    )

    available_countries = forms.ModelMultipleChoiceField(
        label='Доступні країни',
        widget=forms.SelectMultiple(attrs={'class': 'form-control select2-search js-example-basic-multiple'}),
        required=True,
        queryset=Country.objects
    )

    available_delivery_type = forms.ModelMultipleChoiceField(
        label='Доступні способи доставки',
        widget=forms.SelectMultiple(attrs={'class': 'form-control select2-search js-example-basic-multiple'}),
        required=True,
        queryset=DeliveryType.objects.filter(is_active=True)
    )

    available_payment_types = forms.ModelMultipleChoiceField(
        label='Доступні способи оплати',
        widget=forms.SelectMultiple(attrs={'class': 'form-control select2-search js-example-basic-multiple'}),
        required=True,
        queryset=PaymentType.objects
    )

    currency = forms.ModelChoiceField(
        label='Валюта',
        widget=forms.Select(attrs={'class': 'form-control select2-search js-example-basic-single'}),
        required=True,
        queryset=Currency.objects
    )

    welcome_text = forms.CharField(
        label='Вітальне повідомлення',
        widget=forms.Textarea(attrs={'rows': '3', 'cols': '25', 'class': 'form-control modal__field',}),
        required=False,
    )

    terms_of_agreement = forms.BooleanField(
        label="Користувацька угода",
        widget=forms.CheckboxInput(attrs={'class': 'form-control', 'style': 'width:20px;height:20px; margin: 0 0 1em'}),
        required=True
    )

    class Meta:
        model = Bot
        fields = (
            'name',
            'token',
            'description',
            'telegram_operator',
            'available_countries',
            'available_delivery_type',
            'available_payment_types',
            'currency',
            'welcome_text',
            'terms_of_agreement',
        )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        """
        Automatically saves user, who's created a channel as a moder, and try to set webhook
        """
        bot = super().save(commit=False)
        bot.slug = unique_slug_generator(bot)
        bot.owner = self.user

        if commit:
            bot.save()
            self.save_m2m()

        return bot
