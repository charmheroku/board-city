from django.urls import path

from main import views

app_name = "main"

urlpatterns = [
    path("", views.main_page, name="main_page"),
    path("cars/", views.CarListView.as_view(), name="car_list"),
    path("services/", views.ServiceListView.as_view(), name="services_list"),
    path("things/", views.ThingListView.as_view(), name="things_list"),
    path("cars/<int:pk>", views.CarDetailView.as_view(), name="car_detail"),
    path("services/<int:pk>", views.ServiceDetailView.as_view(), name="service_detail"),
    path("things/<int:pk>", views.ThingDetailView.as_view(), name="thing_detail"),
    path("cars/add", views.CreateCarAdvertView.as_view(), name="car_add"),
    path("services/add", views.CreateServiceAdvertView.as_view(), name="service_add"),
    path("things/add", views.CreateThingAdvertView.as_view(), name="thing_add"),
    path("cars/<int:pk>/edit", views.EditCarAdvertView.as_view(), name="car_edit"),
    path(
        "services/<int:pk>/edit",
        views.EditServiceAdvertView.as_view(),
        name="services_edit",
    ),
    path(
        "things/<int:pk>/edit", views.EditThingAdvertView.as_view(), name="thing_edit"
    ),
    path("accounts/seller/", views.SellerEditView.as_view(), name="seller_edit"),
    path("accounts/profile/", views.UserProfileView.as_view(), name="user_edit"),
    path(
        "accounts/subscribe/",
        views.SubscriberProfileView.as_view(),
        name="subscribe_edit",
    ),
    path("search/", views.Search.as_view(), name='search'),

]
