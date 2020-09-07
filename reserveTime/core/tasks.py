from celery.decorators import task
from restaurant.models import Table,TableDate,Time
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMessage, send_mail
from celery import shared_task
from restaurant.models import Company

@task(name="complete_reserve")
def complete_reserve(time, date, table_id):

    reserve_date = TableDate.objects.filter(date=date)
    table = Table.objects.filter(id = table_id, dates_in=reserve_date)
    print(table.first().times.filter(free_time=time))
    times = table.first().times.filter(free_time=time).update(reserved=False)
    

@shared_task
def give_feedback(company_id, user_email):
    company_name = Company.objects.filter(id=company_id).first().company_name
    template_name = 'feedback-email.html'
    subject  = 'Please give your feedback'
    context = {
        'site_address': settings.SITE_ADDRESS,
		'company_id': company_id,
        'company_name' : company_name
    }
    msg = render_to_string(template_name, context)
    message = EmailMessage(subject=subject, body=msg, from_email=settings.EMAIL_HOST_USER, to = (user_email,) )
    message.content_subtype = 'html'
    message.send()
