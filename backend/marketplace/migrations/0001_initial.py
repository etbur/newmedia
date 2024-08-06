# Generated by Django 5.0.7 on 2024-08-06 07:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Products',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('description', models.TextField()),
                ('image', models.ImageField(upload_to='products/')),
                ('seller_profile_name', models.CharField(max_length=255)),
                ('seller_profile_picture', models.ImageField(blank=True, null=True, upload_to='profiles/')),
                ('category', models.CharField(choices=[('electronics', 'Electronics'), ('fashion', 'Fashion'), ('home', 'Home'), ('beauty', 'Beauty'), ('sports', 'Sports'), ('other', 'Other')], default='other', max_length=50)),
                ('views', models.PositiveIntegerField(default=0)),
                ('rating', models.DecimalField(decimal_places=2, default=0, max_digits=3)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
            ],
        ),
    ]
