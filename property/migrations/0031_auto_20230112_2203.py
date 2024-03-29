# Generated by Django 4.0.6 on 2023-01-12 20:03

from django.db import migrations
from property.models import Tenant, PropertyApplication

def create_approved_applications_for_teanats(apps, schema):
    tenants = Tenant.objects.filter(
        user__isnull=False
    )
    # make user property applications as approved
    for tenant in tenants:
        PropertyApplication.objects.get_or_create(
                    owner = tenant.property.user,
                    tenant = tenant.user,
                    state = "approved",
                )

class Migration(migrations.Migration):

    dependencies = [
        ('property', '0030_auto_20221229_2049'),
    ]

    operations = [
        migrations.RunPython(
            create_approved_applications_for_teanats
        )
    ]
