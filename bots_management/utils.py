import string
import random
from typing import Any, Union

from django.utils.text import slugify


def random_string_generator(size: int) -> str:
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(size))


def unique_slug_generator(instance: Any, new_slug: Union[str, None]=None) -> str:
    """
    This is for a Django project and it assumes your instance
    has a model with a slug field and a title character (char) field.
    """
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(str(instance))

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=slug).exists()
    if qs_exists:
        new_slug = "{slug}-{randstr}".format(
            slug=slug,
            randstr=random_string_generator(size=4)
        )
        return unique_slug_generator(instance, new_slug=new_slug)
    return slug
