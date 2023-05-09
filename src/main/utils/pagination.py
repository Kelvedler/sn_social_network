import math
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError


class PageError(ValidationError):
    status_code = 400
    default_detail = _('Page out of bounds')
    default_code = 'page_error'


def fetch_list(queryset, page, order_by='-created_at', per_page=25):
    if type(order_by) == str:
        order = [order_by]
    elif type(order_by) in (list, tuple):
        order = order_by
    else:
        raise ValueError(f'Unknown type of order_by - "{type(order_by)}"')

    items_count = queryset.count()
    pages_count = math.ceil(items_count / per_page)

    if page > 0 and page >= pages_count:
        raise PageError()

    start = page * per_page
    end = start + per_page

    queryset = queryset.order_by(*order)

    items = queryset.all()[start:end]
    return items_count, pages_count, items
