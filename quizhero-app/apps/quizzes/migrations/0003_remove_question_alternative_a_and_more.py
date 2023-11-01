# Generated by Django 4.2.5 on 2023-10-29 18:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quizzes', '0002_question_correct_alternative'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='alternative_a',
        ),
        migrations.RemoveField(
            model_name='question',
            name='alternative_b',
        ),
        migrations.RemoveField(
            model_name='question',
            name='alternative_c',
        ),
        migrations.RemoveField(
            model_name='question',
            name='alternative_d',
        ),
        migrations.RemoveField(
            model_name='question',
            name='correct_alternative',
        ),
        migrations.CreateModel(
            name='QuestionAlternative',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=255)),
                ('is_correct', models.BooleanField(default=False)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quizzes.question')),
            ],
        ),
    ]