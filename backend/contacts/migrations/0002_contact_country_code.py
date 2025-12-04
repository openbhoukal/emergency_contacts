# Generated manually for adding country_code field

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='country_code',
            field=models.CharField(blank=True, default='', help_text='Country code for mobile number (e.g., +91, +1)', max_length=5),
        ),
    ]

