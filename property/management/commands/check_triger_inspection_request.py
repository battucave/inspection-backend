from django.core.management.base import BaseCommand
from property.models import InspectionSchedule, Property, Tenant
from datetime import date, timedelta
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings

def send_inspection_email_tenants(property):
    tenants_emails = Tenant.objects.filter(
        property__id=property.id,
        user__isnull=False
    ).values_list('email',flat=True)

    emails = list(tenants_emails)     
    context ={
                     "property":property,     
                }
    title = f"Inspection360 Inspection Request"
    email_html_message = render_to_string('email/property_inspection_email.html', context)
    email_plaintext_message = render_to_string('email/property_inspection_email.html', context)
    from_email = settings.DEFAULT_FROM_EMAIL
    msg = EmailMultiAlternatives(
        # title:
        title,
        # message:
         email_plaintext_message,
        # from:
        from_email,
        # to:
        emails
        )
    msg.attach_alternative(email_html_message, "text/html")
    msg.send()

     
class Command(BaseCommand):

    def handle(self, *args, **options):
        try:
            today = date.today()
            for schedule in InspectionSchedule.objects.all():
                if schedule.period:
                    if timedelta(days=schedule.period) + schedule.last_triggered <= today:
                        #notify_tenants with inspection
                        send_inspection_email_tenants(schedule.property)
                        # reset last triggered date to be today
                        schedule.last_triggered = today
                        schedule.save()
        except Exception as message:
            self.stdout.write(f'error happended during  trigger inspection request: {message}')

