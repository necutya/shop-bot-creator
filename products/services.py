from sqlite3 import IntegrityError

from django.core.exceptions import ValidationError
from django.utils.text import slugify
from pyexcel_xls import get_data as xls_get
from pyexcel_xlsx import get_data as xlsx_get


from products.exceptions import NonPositiveError, CategoryError
from products.models import Category, ProductPhoto, Product


def parse_import_file(import_file, bot):
    data = None
    if str(import_file).split('.')[-1] == 'xls':
        data = xls_get(import_file)
    elif str(import_file).split('.')[-1] == "xlsx":
        data = xlsx_get(import_file, column_limit=4)

    if not data:
        raise ValidationError(
            'Дозволені лише файли формату .xls и .xlsx',
            code='invalid'
        )

    for row in data['products'][1:]:
        if not row[0] or not row[3]:
            raise IntegrityError
        if int(row[2]) < 0 or float(row[4]) < 0.01 or (row[5] and row[5] < 0):
            raise NonPositiveError

        categories = []
        for category in row[7].split(', '):
            q = Category.objects.filter(name=category, bot__slug=bot.slug).first()
            if not q:
                raise CategoryError
            categories.append(q)

        product = Product(
            name=row[0],
            slug=slugify(row[0]),
            description=row[1],
            amount=row[2],
            article=row[3],
            price=row[4],
            discount=row[5],
            visible=row[6],
            url=row[9],
            bot=bot,
        )
        product.save()

        photo = ProductPhoto(product_id=product.id, is_main=True)
        if row[8]:
            photo.image_url = row[8]
        else:
            photo.image_url = "https://www.freeiconspng.com/thumbs/no-image-icon/no-image-icon-6.png"
        photo.save()

        product.categories.add(*categories)
        product.save()
