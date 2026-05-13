# Generated manually on 2026-05-13

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_lf_itse', '0002_agregar_dias_atencion_y_numero_folios_licencia'),
    ]

    operations = [
        migrations.AddField(
            model_name='tipoprocedimientotupa',
            name='monto',
            field=models.DecimalField(
                decimal_places=2,
                default=0,
                max_digits=10,
                validators=[django.core.validators.MinValueValidator(0)],
            ),
        ),
    ]
