# Generated by Django 5.1.5 on 2025-01-23 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('superset', '0007_remove_company_eligibility_criteria_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='opportunity_type',
            field=models.CharField(choices=[('Placement', 'Placement'), ('Internship', 'Internship'), ('I+P', 'Internship + Placement')], default='Placement', max_length=20),
        ),
    ]
