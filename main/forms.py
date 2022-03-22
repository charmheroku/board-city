from django import forms

from main.models import CarAdvert, Picture

"""Вложенная Inline форма для фото объявлений"""
CarFormSet = forms.inlineformset_factory(
    CarAdvert,
    Picture,
    fields=(
        "caption",
        "file",
    ),
    max_num=1,
)
