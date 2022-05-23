import mimetypes
import os

from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils.datastructures import MultiValueDictKeyError
from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView
import django_excel as excel

from bots_management.mixins import OwnerRequiredMixin
from bots_management.models import Bot
from bots_management.services import get_bot_by_slug
from products.exceptions import CategoryError, NonPositiveError
from products.forms import ProductForm, CategoryForm, UploadFileForm
from products.models import Product, Category, ProductPhoto
from products.services import parse_import_file


class CategoryCreateView(OwnerRequiredMixin, CreateView):
    template_name = "products/category_create.html"
    form_class = CategoryForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['bot_slug'] = self.kwargs.get('slug')
        return kwargs

    def get_success_url(self):
        # if message is planned send to
        return reverse_lazy(
            "bots-management:products:category-list",
            kwargs={
                "slug": self.kwargs.get('slug')
            }
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        bot = get_bot_by_slug(self.kwargs.get('slug'))
        context['bot'] = bot
        return context


class CategoryListView(OwnerRequiredMixin, ListView):
    template_name = "products/category_list.html"
    context_object_name = 'categories'

    def get_queryset(self):
        bot = get_bot_by_slug(self.kwargs['slug'])
        return Category.objects.filter(bot=bot)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['bot'] = get_bot_by_slug(self.kwargs['slug'])
        return context


class CategoryDeleteView(OwnerRequiredMixin, DeleteView):
    model = Category
    template_name = "products/category_delete.html"
    context_object_name = "category"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['bot'] = get_bot_by_slug(self.kwargs['slug'])
        return context

    def get_success_url(self):
        return reverse_lazy("bots-management:products:category-list", kwargs={
            "slug": self.kwargs.get('slug')
        })


class CategoryUpdateView(OwnerRequiredMixin, UpdateView):
    model = Category
    template_name = "products/category_update.html"
    context_object_name = "category"
    form_class = CategoryForm

    def get_success_url(self):
        return reverse_lazy("bots-management:products:category-list", kwargs={
            "slug": self.kwargs.get('slug')
        })

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['bot_slug'] = self.kwargs.get('slug')
        return kwargs

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['bot'] = get_bot_by_slug(self.kwargs['slug'])
        return context


class ProductCreateView(OwnerRequiredMixin, CreateView):
    template_name = "products/product_create.html"
    form_class = ProductForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['bot_slug'] = self.kwargs.get('slug')
        return kwargs

    def get_success_url(self):
        # if message is planned send to
        return reverse_lazy(
            "bots-management:products:product-list",
            kwargs={
                "slug": self.kwargs.get('slug')
            }
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        bot = get_bot_by_slug(self.kwargs.get('slug'))
        context['bot'] = bot
        return context


class ProductListView(OwnerRequiredMixin, ListView):
    template_name = "products/product_list.html"
    context_object_name = 'products'

    def get_queryset(self):
        bot = get_bot_by_slug(self.kwargs['slug'])
        return Product.objects.filter(bot=bot)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['bot'] = get_bot_by_slug(self.kwargs['slug'])
        return context


class ProductDetailView(OwnerRequiredMixin, DetailView):
    """
    Get info can only moderator or superuser.
    """
    model = Product
    template_name = "products/product_details.html"
    context_object_name = "product"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['bot'] = get_bot_by_slug(self.kwargs['slug'])
        return context


class ProductDeleteView(OwnerRequiredMixin, DeleteView):
    model = Product
    template_name = "products/product_delete.html"
    context_object_name = "product"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['bot'] = get_bot_by_slug(self.kwargs['slug'])
        return context

    def get_success_url(self):
        return reverse_lazy("bots-management:products:product-list", kwargs={
            "slug": self.kwargs.get('slug')
        })


class ProductUpdateView(OwnerRequiredMixin, UpdateView):
    model = Product
    template_name = "products/product_update.html"
    context_object_name = "product"
    form_class = ProductForm

    def get_success_url(self):
        return reverse_lazy("bots-management:products:product-list", kwargs={
            "slug": self.kwargs.get('slug')
        })

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['bot_slug'] = self.kwargs.get('slug')
        return kwargs

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['bot'] = get_bot_by_slug(self.kwargs['slug'])
        return context


def product_bulk_creation(request, slug: str):
    error_msg = None
    bot = get_object_or_404(Bot, slug=slug)

    if request.method == "POST":
        form = UploadFileForm(request.POST,
                              request.FILES)
        if form.is_valid():
            try:
                import_file = request.FILES['file']
                parse_import_file(import_file, bot)
            except IntegrityError as e:
                print(e)
                error_msg = "Одне із необхідних полів незаповнене. Назви колонок потрібних полів будуть виділені " \
                            "жирним шрифотом. "
            except NonPositiveError as e:
                print(e)
                error_msg = "Поля суми і кількості не можуть бути меншими або дорівнюють нулю."
            except CategoryError as e:
                print(e)
                error_msg = "Ця категорія не існує. Створіть категорію товару або оберіть іншу."
            except ValidationError as e:
                print(e)
                error_msg = e.message
            except Exception as e:
                print(e)
                error_msg = "Назва колонок таблиці не співпадають із шаблонним прикладом. Будь ласка перевірте назву " \
                            "колонок і спробуйте ще раз. "

            else:
                return redirect('bots-management:products:product-list', slug)
    else:
        form = UploadFileForm()
    return render(request, 'products/product_bulk_add.html',
                  {'bot': bot, 'form': form, 'error_msg': error_msg})


def download_file(request, slug):
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = "template_files"
    file_name = 'product_bulk_creation.xls'
    full_file_path = os.path.join(base_path, file_path, file_name)

    try:
        with open(full_file_path, 'rb') as path:
            mime_type, _ = mimetypes.guess_type(full_file_path)

            response = HttpResponse(path, content_type=mime_type)
            response['Content-Disposition'] = "attachment; filename=%s" % file_name

            return response

    except Exception as e:
        print(e)
        form = UploadFileForm()
        bot = get_object_or_404(Bot, slug=slug)
        error_msg = "Щось пішло не так"

        return render(request, 'products/product_bulk_add.html',
                      {'bot': bot, 'form': form, 'error_msg': error_msg})
