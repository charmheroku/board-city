import random

from django.shortcuts import render
from django import forms
from django.http import Http404
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, UpdateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.cache import cache
from django.contrib.postgres.search import SearchVector


from . import forms as main_forms, mixins


from main.models import (
    CarAdvert,
    ServicesAdvert,
    Subscriber,
    ThingsAdvert,
    Seller,
    Category,
)

from django.views.decorators.http import require_GET


@require_GET
def robots_txt(request):
    lines = [
        "User-Agent: *",
        "Disallow: catalog/things/add",
        "Disallow: catalog/cars/add",
        "Disallow: catalog/cars/add",
        "Disallow: catalog/services/add",
        "Disallow: accounts/profile/",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")


def main_page(request) -> HttpResponse:
    """Отображение главной страницы сайта"""
    # add.delay(50, 7)
    context = {}
    if not request.is_mobile:
        context["is_mobile"] = True

    return render(request, "main/index.html", context)


# @method_decorator(cache_page(60 * 5), name="dispatch")
class CarListView(ListView):
    """Отображение списка обьявлений - Авто"""

    model = CarAdvert
    context_object_name = "cars"
    template_name = "main/car_list.html"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tags = CarAdvert.objects.values_list("tags__name")
        tags = set(tags)
        context["tags"] = tags
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        tag = self.request.GET.get("tag")
        if tag:
            return CarAdvert.objects.filter(tags__name=tag)
        return queryset


class ServiceListView(ListView):
    """Отображение списка обьявлений - Услуги"""

    model = ServicesAdvert
    context_object_name = "services"
    template_name = "main/service_list.html"
    paginate_by = 1

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tags = ServicesAdvert.objects.values_list("tags__name")
        tags = set(tags)
        context["tags"] = tags
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        tag = self.request.GET.get("tag")
        if tag:
            return ServicesAdvert.objects.filter(tags__name=tag)
        return queryset


class ThingListView(ListView):
    """Отображение списка обьявлений - Вещи"""

    model = ThingsAdvert
    context_object_name = "things"
    template_name = "main/thing_list.html"
    paginate_by = 1

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tags = ThingsAdvert.objects.values_list("tags__name")
        tags = set(tags)
        context["tags"] = tags
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        tag = self.request.GET.get("tag")
        if tag:
            return ThingsAdvert.objects.filter(tags__name=tag)
        return queryset


# @method_decorator(cache_page(60 * 5), name="dispatch")
class CarDetailView(DetailView):
    """Отображение детальной обьявления - Авто"""

    model = CarAdvert
    context_object_name = "car"
    template_name = "main/car_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cid = kwargs["object"].id
        price = context["object"].price
        key_name = str(self.__class__.__name__) + str(cid)
        r = random.uniform(0.8, 1.2)
        new_price = cache.get_or_set(key_name, round((price * r), 2), 60)
        context["new_price"] = new_price
        return context


class ServiceDetailView(DetailView):
    """Отображение детальной обьявления - Услуги"""

    model = ServicesAdvert
    context_object_name = "service"
    template_name = "main/service_detail.html"


class ThingDetailView(DetailView):
    """Отображение детальной обьявления - Вещи"""

    model = ThingsAdvert
    context_object_name = "thing"
    template_name = "main/thing_detail.html"


class SellerEditView(LoginRequiredMixin, UpdateView):
    """Редактирование Seller"""

    model = Seller
    success_url = reverse_lazy("main:seller_edit")
    template_name = "account/seller_edit.html"
    fields = (
        "first_name",
        "last_name",
        "email",
        "kod_inn",
    )

    def get_object(self, queryset=None):
        user = self.request.user
        try:
            seller = Seller.objects.get(user_ptr=user)
            return seller
        except Seller.DoesNotExist:
            raise Http404()


class CreateCarAdvertView(mixins.BannedUsersGroup, LoginRequiredMixin, CreateView):
    """Создание обьявления - Авто"""

    model = CarAdvert
    template_name = "account/car_advert_add_edit.html"
    fields = (
        "title",
        "description",
        "price",
        "brand",
        "model",
        "year",
        "color",
        "category",
        "tags",
        "tags_array",
    )
    success_url = reverse_lazy("main:seller_edit")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["formset"] = main_forms.CarFormSet()
        return context

    def form_valid(self, form):
        form.instance.seller = self.request.user.seller
        advert_form = form.save(commit=False)
        formset = main_forms.CarFormSet(
            self.request.POST, self.request.FILES, instance=advert_form
        )
        if formset.is_valid():
            formset.instance = form.save()
            formset.save()
            return super(CreateCarAdvertView, self).form_valid(form)
        else:
            return self.render_to_response({"form": form, "formset": formset})


class CreateServiceAdvertView(mixins.BannedUsersGroup, LoginRequiredMixin, CreateView):
    """Создание обьявления - Услуги"""

    model = ServicesAdvert
    template_name = "account/service_advert_add_edit.html"
    fields = (
        "title",
        "description",
        "price",
        "full_adress",
        "category",
        "tags",
        "tags_array",
    )
    success_url = reverse_lazy("main:seller_edit")

    def form_valid(self, form):
        form.instance.seller = self.request.user.seller
        return super().form_valid(form)


class CreateThingAdvertView(mixins.BannedUsersGroup, LoginRequiredMixin, CreateView):
    """Создание обьявления - Вещи"""

    model = ThingsAdvert
    template_name = "account/thing_advert_add_edit.html"
    fields = (
        "title",
        "description",
        "price",
        "condition",
        "category",
        "tags",
        "tags_array",
    )
    success_url = reverse_lazy("main:seller_edit")

    def form_valid(self, form):
        form.instance.seller = self.request.user.seller
        return super().form_valid(form)


class EditCarAdvertView(LoginRequiredMixin, UpdateView):
    """Редактирование обьявления - Авто"""

    model = CarAdvert
    template_name = "account/car_advert_add_edit.html"
    fields = (
        "title",
        "description",
        "price",
        "brand",
        "model",
        "year",
        "color",
        "tags",
        "tags_array",
    )
    success_url = reverse_lazy("main:seller_edit")

    def get_object(self, queryset=None):
        caradvert = super().get_object(queryset=queryset)
        if caradvert.seller.pk != self.request.user.pk:
            raise Http404()
        return caradvert

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["formset"] = main_forms.CarFormSet(instance=self.get_object())
        return context

    def form_valid(self, form):
        advert_form = form.save(commit=False)
        formset = main_forms.CarFormSet(
            self.request.POST, self.request.FILES, instance=advert_form
        )
        if formset.is_valid():

            formset.instance = form.save()
            formset.save()
            return super(EditCarAdvertView, self).form_valid(form)
        else:
            return self.render_to_response({"form": form, "formset": formset})


class EditServiceAdvertView(LoginRequiredMixin, UpdateView):
    """Редактирование обьявления - Услуги"""

    model = ServicesAdvert
    template_name = "account/service_advert_add_edit.html"
    fields = ("title", "description", "price", "full_adress", "tags", "tags_array")
    success_url = reverse_lazy("main:seller_edit")

    def get_object(self, queryset=None):
        serviceadvert = super().get_object(queryset=queryset)
        if serviceadvert.seller.pk != self.request.user.pk:
            raise Http404()
        return serviceadvert


class EditThingAdvertView(LoginRequiredMixin, UpdateView):
    """Редактирование обьявления - Вещи"""

    model = ThingsAdvert
    template_name = "account/thing_advert_add_edit.html"
    fields = ("title", "description", "price", "condition", "tags", "tags_array")
    success_url = reverse_lazy("main:seller_edit")

    def get_object(self, queryset=None):
        thingadvert = super().get_object(queryset=queryset)
        if thingadvert.seller.pk != self.request.user.pk:
            raise Http404()
        return thingadvert


class UserProfileView(LoginRequiredMixin, UpdateView):
    """Редактирование профиля Юзера"""

    model = User
    template_name = "account/user_edit.html"
    success_url = reverse_lazy("main:user_edit")

    fields = ("email", "first_name", "last_name")

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        if "email" in form.changed_data:

            email = form.cleaned_data.get("email")
            user = self.request.user
            socialaccount = user.socialaccount_set.filter(user=user).first()
            if socialaccount is not None:
                if socialaccount.extra_data.get("email") != email:
                    messages.error(self.request, "Email не совпадают")
                    return self.form_invalid(form)

            messages.success(self.request, "Email успешно изменен")
            return super().form_valid(form)
        else:
            messages.success(self.request, "Профиль успешно изменен")
            return super().form_valid(form)


class SubscriberProfileView(LoginRequiredMixin, UpdateView):
    """Добавления подписки на рассылки"""

    model = Subscriber
    template_name = "account/subscribe_edit.html"
    success_url = reverse_lazy("main:user_edit")

    fields = ("сategory_subscribe",)

    def get_object(self, queryset=None):

        user = self.request.user
        try:
            subscriber = Subscriber.objects.get(user=user)
            return subscriber
        except Subscriber.DoesNotExist:
            raise Http404()

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        form.fields["сategory_subscribe"] = forms.ModelMultipleChoiceField(
            required=False,
            queryset=Category.objects.all(),
            widget=forms.CheckboxSelectMultiple,
        )

        return form


class Search(ListView):
    """Поиск объявлений"""

    paginate_by = 1
    context_object_name = "cars"
    template_name = "main/car_list.html"

    def get_queryset(self):
        q = self.request.GET.get("q", "")
        return CarAdvert.objects.annotate(
            search=SearchVector("title", "description")
        ).filter(search=q)
