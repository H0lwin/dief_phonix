from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('persons', '0004_populate_created_by'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='salesinvoice',
            name='service',
        ),
        migrations.RemoveField(
            model_name='salesinvoice',
            name='service_category',
        ),
        migrations.RemoveField(
            model_name='purchaseinvoice',
            name='service',
        ),
        migrations.RemoveField(
            model_name='purchaseinvoice',
            name='service_category',
        ),
        migrations.AddField(
            model_name='salesinvoice',
            name='service_category',
            field=models.CharField(
                choices=[
                    ('commercial', 'خدمات بازرگانی'),
                    ('registration', 'خدمات ثبت'),
                    ('legal', 'خدمات حقوقی'),
                    ('leasing', 'خدمات لیزینگ'),
                    ('loan', 'خدمات وام'),
                ],
                max_length=20,
                verbose_name='دسته‌بندی خدمت',
                default='commercial'
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='salesinvoice',
            name='service_id',
            field=models.PositiveIntegerField(
                blank=True,
                null=True,
                verbose_name='خدمت'
            ),
        ),
        migrations.AddField(
            model_name='purchaseinvoice',
            name='service_category',
            field=models.CharField(
                choices=[
                    ('commercial', 'خدمات بازرگانی'),
                    ('registration', 'خدمات ثبت'),
                    ('legal', 'خدمات حقوقی'),
                    ('leasing', 'خدمات لیزینگ'),
                    ('loan', 'خدمات وام'),
                ],
                max_length=20,
                verbose_name='دسته‌بندی خدمت',
                default='commercial'
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='purchaseinvoice',
            name='service_id',
            field=models.PositiveIntegerField(
                blank=True,
                null=True,
                verbose_name='خدمت'
            ),
        ),
        migrations.DeleteModel(
            name='Service',
        ),
        migrations.DeleteModel(
            name='ServiceCategory',
        ),
    ]
