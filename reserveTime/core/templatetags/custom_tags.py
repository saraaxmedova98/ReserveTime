from restaurant.models import Notification, Reservation, Table
import datetime
from django import template

register = template.Library()


@register.simple_tag()
def notification(user):
    notification = Notification.objects.filter(reciever=user, read=False)
    
    return notification

@register.simple_tag()
def reservation(user):
    reservation = Reservation.objects.filter(user=user, accept=True, reserved_date__gt = datetime.datetime.today())
    
    return reservation

@register.simple_tag()
def get_party_size(table_id):
    size = Table.objects.filter(id=table_id).first().size
    
    return size