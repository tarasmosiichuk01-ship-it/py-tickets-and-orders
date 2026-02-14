from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from django.utils.dateparse import parse_datetime

from db.models import Order, Ticket, MovieSession


@transaction.atomic
def create_order(
        tickets: list[dict],
        username: str,
        date: str = None
) -> Order:
    user = get_user_model().objects.get(username=username)
    order_data = {"user": user}
    if date:
        order_data["created_at"] = parse_datetime(date)

    order = Order.objects.create(**order_data)

    for ticket in tickets:
        movie_session = MovieSession.objects.get(id=ticket["movie_session"])
        Ticket.objects.create(
            movie_session=movie_session,
            order=order,
            row=ticket["row"],
            seat=ticket["seat"]
        )
    return order


def get_orders(username: str = None) -> QuerySet[Order]:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
