from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_lf_itse', '0003_itse_informe'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.AlterField(
                    model_name='licenciafuncionamiento',
                    name='hora_desde',
                    field=models.TimeField(blank=True, null=True),
                ),
                migrations.AlterField(
                    model_name='licenciafuncionamiento',
                    name='hora_hasta',
                    field=models.TimeField(blank=True, null=True),
                ),
            ],
            database_operations=[],
        ),
    ]
