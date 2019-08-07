# Generated by Django 2.2 on 2019-08-07 17:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField(default='add some detail')),
                ('image_url', models.CharField(default='https://lar-mo.com/images/lazy_placeholder.gif', max_length=200)),
                ('replacement_cost', models.DecimalField(decimal_places=2, max_digits=6)),
            ],
        ),
        migrations.CreateModel(
            name='UserItemCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='UserItemCondition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='UserItemStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='UserItemCheckout',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('request_date', models.DateTimeField()),
                ('checkout_date', models.DateTimeField(blank=True, default=None, null=True)),
                ('checkin_date', models.DateTimeField(blank=True, default=None, null=True)),
                ('due_date', models.DateTimeField(blank=True, default=None, null=True)),
                ('borrower', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('item_status', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='lendingLibrary.UserItemStatus')),
                ('user_item', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='lendingLibrary.UserItem')),
            ],
        ),
        migrations.AddField(
            model_name='useritem',
            name='condition',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='lendingLibrary.UserItemCondition'),
        ),
        migrations.AddField(
            model_name='useritem',
            name='item_status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='lendingLibrary.UserItemStatus'),
        ),
        migrations.AddField(
            model_name='useritem',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='useritem',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='lendingLibrary.UserItemCategory'),
        ),
    ]
