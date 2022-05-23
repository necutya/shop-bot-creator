from django.db import models
from django.urls import reverse

from bots_management.models import Bot


class Category(models.Model):
    name = models.CharField("Назва категорії", max_length=50)
    bot = models.ForeignKey(
        Bot,
        verbose_name="Бот",
        on_delete=models.CASCADE,
        related_name="categories",
        blank=True,
    )
    description = models.TextField("Опис", max_length=255, null=True, blank=True)

    def __str__(self) -> str:
        return self.name.title()

    def get_update_url(self):
        return reverse(
            "bots-management:products:category-update",
            kwargs={"slug": self.bot.slug,
                    "pk": self.pk})

    def get_delete_url(self):
        return reverse(
            "bots-management:products:category-delete",
            kwargs={"slug": self.bot.slug,
                    "pk": self.pk})


class Product(models.Model):
    name = models.CharField("Назва", max_length=50)
    slug = models.SlugField(blank=True)
    description = models.TextField("Опис", max_length=255)
    amount = models.IntegerField("Кількість", default=0)
    article = models.CharField("Артикул", max_length=255, null=True, blank=True)
    price = models.DecimalField("Ціна", max_digits=6, decimal_places=2)
    discount = models.DecimalField("Відсоток знижки", null=True, blank=True, max_digits=6, decimal_places=2)
    visible = models.BooleanField("Видимий товар", default=True)
    bot = models.ForeignKey(
        Bot,
        verbose_name="Бот",
        on_delete=models.CASCADE,
        related_name="products",
        blank=True,
    )
    categories = models.ManyToManyField(
        Category,
        verbose_name="Категорії",
        related_name="products",
        blank=True
    )
    url = models.URLField(
        "Посилання на продукт в інтернет магазині",
        blank=True,
        null=True
    )
    likes = models.IntegerField(
        "Кількість лайків",
        default=0,
        blank=True
    )
    views_count = models.IntegerField(
        "Кількіть переглядів",
        default=0,
        blank=True
    )
    add_to_basket_count = models.IntegerField(
        "Кількість додавань до корзини",
        default=0,
        blank=True
    )
    acquired_count = models.IntegerField(
        "Кількість покупок",
        default=0,
        blank=True
    )

    def get_absolute_url(self):
        return reverse(
            "bots-management:products:product-detailed",
            kwargs={"slug": self.bot.slug,
                    "pk": self.pk})

    def get_update_url(self):
        return reverse(
            "bots-management:products:product-update",
            kwargs={"slug": self.bot.slug,
                    "pk": self.pk})

    def get_delete_url(self):
        return reverse(
            "bots-management:products:product-delete",
            kwargs={"slug": self.bot.slug,
                    "pk": self.pk})

    @property
    def final_price(self):
        if self.discount:
            return round(self.price - (self.price / self.discount), 2)

        return self.price

    def __str__(self) -> str:
        return self.name.title()


class ProductPhoto(models.Model):
    product = models.ForeignKey(
        Product,
        verbose_name="Продукт",
        on_delete=models.CASCADE,
        related_name="photos",
    )
    image = models.ImageField(
        "Фото товару", upload_to='bots/images/', blank=True
    )
    is_main = models.BooleanField(
        "Головне зображення", default=False
    )
    image_url = models.URLField(
        "Посилання на фото товару", blank=True,
        default="https://www.freeiconspng.com/thumbs/no-image-icon/no-image-icon-6.png"
    )

    def __str__(self) -> str:
        return self.image.url
