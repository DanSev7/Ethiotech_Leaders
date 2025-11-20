from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0026_add_tracking_fields'),
    ]

    operations = [
        migrations.AddField(
            model_name='cardblock',
            name='payload',
            field=models.JSONField(blank=True, default=dict, help_text='Type-specific data for dynamic card layouts'),
        ),
    ]

