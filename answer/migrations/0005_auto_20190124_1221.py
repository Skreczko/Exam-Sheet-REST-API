# Generated by Django 2.1.5 on 2019-01-24 11:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('answer', '0004_auto_20190123_2207'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='related_answer', to='question.Question', verbose_name='question_id'),
        ),
    ]
