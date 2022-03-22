from django import template

register = template.Library()


@register.filter
def invert_string(value):
    """Тэг инвертирования строки"""
    return value[::-1]


@register.simple_tag
def url_replace(request, field, value):
    """Тэг для пагинации фильтра по тэгам"""
    dict_ = request.GET.copy()
    dict_[field] = value
    return dict_.urlencode()
