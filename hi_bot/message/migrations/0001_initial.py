# Generated by Django 3.2 on 2023-07-26 10:46

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('role', models.CharField(blank=True, choices=[('anonymous', 'анон'), ('user', 'Пользователь'), ('moderator', 'Модератор'), ('admin', 'Админ')], default='user', max_length=30, verbose_name='Пользовательская роль')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'Пользователь',
                'verbose_name_plural': 'Пользователи',
                'ordering': ('id',),
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now=True, verbose_name='Время получения')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Описание')),
                ('title', models.TextField(blank=True, null=True, verbose_name='Заголовок')),
                ('pub_date', models.DateTimeField(blank=True, null=True, verbose_name='Время получения')),
                ('command_response', models.TextField(choices=[('Я бот который родился в процессе написания тестового задания. Расскажу интересные новости и скажу какая погода. Cписок рабочих команд ты увидешь заюзая команду: /help Надеюсь тебе понравится))', 'START'), ('/start: Скажу привет и расскажу кратко, что умею, \n/help: Расскажу какими командами ты можешь воспользоваться, \n/weather: расскажу какая погода в этом городе, \n/news: Интересные новости читать будем??!!1! ', 'HELP'), ('Я ща тебе такое расскажу, только сначала присядь ', 'NEWS'), ('Так а ты вообще знаешь че там по погоде? Ща буду рассказывать ', 'WEATHER')], verbose_name='Команда для бота')),
                ('link', models.URLField(blank=True, null=True, verbose_name='Ссылка на новость')),
                ('image', models.ImageField(blank=True, null=True, upload_to='message/', verbose_name='Картинка')),
                ('sunrise', models.DateTimeField(blank=True, null=True, verbose_name='Восход солнца')),
                ('humidity', models.FloatField(blank=True, null=True, verbose_name='Влажность воздуха')),
                ('city', models.CharField(blank=True, max_length=30, null=True, verbose_name='Влажность воздуха')),
                ('temp', models.FloatField(blank=True, null=True, verbose_name='Температура воздуха в С°')),
                ('recipient', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='recipient', to=settings.AUTH_USER_MODEL, verbose_name='Получатель сообщения')),
            ],
            options={
                'verbose_name': 'Ответ',
                'verbose_name_plural': 'Ответы',
                'ordering': ('-created',),
            },
        ),
    ]
