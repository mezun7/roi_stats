# Generated by Django 5.0.4 on 2024-04-07 11:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('roi', '0003_regionalias'),
    ]

    operations = [
        migrations.RenameField(
            model_name='student',
            old_name='first_name',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='student',
            old_name='father_name',
            new_name='patranomic',
        ),
        migrations.RenameField(
            model_name='student',
            old_name='last_name',
            new_name='surname',
        ),
        migrations.AlterField(
            model_name='task',
            name='alias',
            field=models.CharField(max_length=100, verbose_name='Короткое название'),
        ),
        migrations.AlterField(
            model_name='task',
            name='name',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Название'),
        ),
    ]