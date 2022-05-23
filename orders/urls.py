from django.urls import path

from orders.views import (
    OrderListView, decline_order, accept_order,
)

app_name = "orders"

urlpatterns = [
    path(
        "orders/",
        OrderListView.as_view(),
        name="order-list"
    ),
    path(
        "orders/<int:order_id>/accept/",
        accept_order,
        name="order-decline"
    ),
    path(
        "orders/<int:order_id>/decline/",
        decline_order,
        name="order-accept"
    ),
]
