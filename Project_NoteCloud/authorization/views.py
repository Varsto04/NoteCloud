from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from .forms import SignUpForm
from .models import create_user_table
import jwt
import secrets
from django.db import connection


def registration(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            # получаем имя пользователя и пароль из формы
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            # выполняем аутентификацию
            user = authenticate(username=username, password=password)

            create_user_table(username)

            secret_key = secrets.token_urlsafe(64)

            with connection.cursor() as cursor:
                cursor.execute(f"SELECT id FROM auth_user WHERE username = '{username}'")
                id_user = [row[0] for row in cursor.fetchall()][0]
            with connection.cursor() as cursor:
                cursor.execute(
                    f"INSERT INTO jwt_tokens (id_user, secret_key) VALUES "
                    f"(%s, %s)", [id_user, secret_key])

            login(request, user)
            return redirect('/')
    else:
        form = SignUpForm()
    return render(request, 'authorization/signup.html', {'form': form})


def index(request):
    return redirect('/')
