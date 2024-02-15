from django.shortcuts import render
from django.http import JsonResponse
import json
from django.middleware import csrf
from django.db import connection
import jwt
import datetime


def mobile_login(request):
    if request.method == 'POST':
        received_data = json.loads(request.body)
        print(received_data)
        try:
            login = received_data['login']
            password_receive = received_data['password']
            logged_in_user = login
            with connection.cursor() as cursor:
                cursor.execute(f"SELECT password FROM auth_user WHERE username = %s", [logged_in_user])
                password = [row[0] for row in cursor.fetchall()]
            if password:
                password = password[0].split('$')[3]
                if password == password_receive:
                    with connection.cursor() as cursor:
                        cursor.execute(f"SELECT id FROM auth_user WHERE username = '{logged_in_user}'")
                        id_user = [row[0] for row in cursor.fetchall()]
                    if id_user:
                        id_user = id_user[0]
                        with connection.cursor() as cursor:
                            cursor.execute(f"SELECT secret_key FROM jwt_tokens WHERE id_user = %s", [id_user])
                            secret_key = [row[0] for row in cursor.fetchall()][0]

                        expiration_time = datetime.datetime.utcnow() + datetime.timedelta(hours=96)

                        payload = {'user': login, 'password': password, 'id': id_user, 'exp': expiration_time}
                        jwt_token = jwt.encode(payload, secret_key, algorithm='HS256')
                        return JsonResponse({'message': True, 'jwt_token': jwt_token, 'id_user': id_user})
                    else:
                        return JsonResponse({'error': 'Введенного логина не существует или неправильынй пароль'})
                else:
                    return JsonResponse({'message': False})
            else:
                return JsonResponse({'error': 'Введенного логина не существует или неправильынй пароль'})
        except:
            return JsonResponse({'error': 'Ошибка на сервере'})
    else:
        # Если файл не был загружен
        return JsonResponse({'error': 'Ошибка на сервере'}, status=400)


def get_csrf_token(request):
    # Получаем CSRF-токен из cookies
    csrf_token = csrf.get_token(request)
    return JsonResponse({'csrf_token': csrf_token})


def get_salt(request):
    if request.method == 'POST':
        received_data = json.loads(request.body)
        try:
            login = received_data['login']
            print(login)
            logged_in_user = login
            with connection.cursor() as cursor:
                cursor.execute(f"SELECT password FROM auth_user WHERE username = %s", [logged_in_user])
                salt = [row[0] for row in cursor.fetchall()]
            if salt:
                salt = salt[0].split('$')[2]
                print(salt)
                return JsonResponse({'salt': salt})
            else:
                return JsonResponse({'error': 'Введенного логина не существует или неправильынй пароль'})
        except:
            return JsonResponse({'error': 'Ошибка на сервере'})
    else:
        return JsonResponse({'error': 'Ошибка на сервере'}, status=400)


def get_data(request):
    if request.method == 'POST':
        received_data = json.loads(request.body)
        print(received_data)
        try:
            login = received_data['login']
            print(login)
            jwt_token_receive = received_data['jwt_token']
            print(jwt_token_receive)

            with connection.cursor() as cursor:
                cursor.execute(f"SELECT id FROM auth_user WHERE username = %s", [login])
                id_user = [row[0] for row in cursor.fetchall()]
            if id_user:
                id_user = id_user[0]
                with connection.cursor() as cursor:
                    cursor.execute(f"SELECT secret_key FROM jwt_tokens WHERE id_user = %s", [id_user])
                    secret_key = [row[0] for row in cursor.fetchall()][0]
                try:
                    decoded_payload = jwt.decode(jwt_token_receive, secret_key, algorithms=['HS256'])
                    print(decoded_payload)
                    if decoded_payload['user'] == login:
                        table_user = f"notes_{login}"
                        with connection.cursor() as cursor:
                            cursor.execute(f"SELECT * FROM {table_user}")
                            data = [row for row in cursor.fetchall()]
                        print(data)
                        return JsonResponse({'data': data})
                    else:
                        return JsonResponse({'error': 'Данные были изменены'})
                except jwt.InvalidTokenError:
                    return JsonResponse({'error': 'Неправильный jwt_token!'})
            else:
                return JsonResponse({'error': 'Введенного логина не существует или неправильынй пароль'})
        except:
            return JsonResponse({'error': 'Ошибка на сервере'})
    else:
        return JsonResponse({'error': 'Ошибка на сервере'}, status=400)


def is_number(string):
    return string.isdigit()


def save_cloud_note(request):
    if request.method == 'POST':
        received_data = json.loads(request.body)
        print(received_data)
        try:
            login = received_data['login']
            jwt_token_receive = received_data['jwt_token']

            with connection.cursor() as cursor:
                cursor.execute(f"SELECT id FROM auth_user WHERE username = %s", [login])
                id_user = [row[0] for row in cursor.fetchall()]
            if id_user:
                id_user = id_user[0]
                with connection.cursor() as cursor:
                    cursor.execute(f"SELECT secret_key FROM jwt_tokens WHERE id_user = %s", [id_user])
                    secret_key = [row[0] for row in cursor.fetchall()][0]
                try:
                    decoded_payload = jwt.decode(jwt_token_receive, secret_key, algorithms=['HS256'])
                    print(decoded_payload)
                    if decoded_payload['user'] == login:
                        table_user = f"notes_{login}"
                        with connection.cursor() as cursor:
                            cursor.execute(f"SELECT title FROM {table_user}")
                            titles = [row[0] for row in cursor.fetchall()]
                        data = received_data['data'][0]
                        title = data['note']
                        if titles.count(title) != 0:
                            title = data['note']
                            user_id_received = decoded_payload['id']
                            with connection.cursor() as cursor:
                                cursor.execute(f"SELECT id FROM {table_user} WHERE title = %s", [title])
                                id_title = [row[0] for row in cursor.fetchall()][0]
                            with connection.cursor() as cursor:
                                cursor.execute(
                                    f"SELECT user1_id, user2_id, user3_id FROM {table_user} WHERE id = %s",
                                    [id_title])
                                users_id = []
                                for row in cursor.fetchall():
                                    users_id.append(str(row[0]))
                                    users_id.append(str(row[1]))
                                    users_id.append(str(row[2]))
                            with connection.cursor() as cursor:
                                cursor.execute(f"SELECT user_id FROM {table_user} WHERE id = %s", [id_title])
                                user_id_author = [row[0] for row in cursor.fetchall()][0]
                            if str(user_id_author) == str(user_id_received):
                                data_author = data['content']
                                for user_id in users_id:
                                    if is_number(user_id):
                                        with connection.cursor() as cursor:
                                            cursor.execute(f"SELECT username FROM auth_user WHERE id = %s",
                                                           [int(user_id)])
                                            username = [row[0] for row in cursor.fetchall()][0]
                                            table_name_user = f"notes_{username}"
                                        with connection.cursor() as cursor:
                                            cursor.execute(f"SELECT id FROM {table_name_user} WHERE title = %s",
                                                           [title])
                                            id_title_user = [row[0] for row in cursor.fetchall()][0]
                                        with connection.cursor() as cursor:
                                            cursor.execute(
                                                f"UPDATE {table_name_user} SET content_author = %s WHERE id = %s",
                                                [data_author, id_title_user])
                                with connection.cursor() as cursor:
                                    cursor.execute(f"SELECT id FROM {table_user} WHERE title = %s", [title])
                                    id_title = [row[0] for row in cursor.fetchall()][0]
                                with connection.cursor() as cursor:
                                    cursor.execute(f"UPDATE {table_user} SET content_author = %s WHERE id = %s",
                                                   [data_author, id_title])
                            else:
                                if str(users_id[0]) == str(user_id_received):
                                    data_user = data['content_user1']
                                    for user_id in users_id:
                                        if is_number(user_id):
                                            with connection.cursor() as cursor:
                                                cursor.execute(f"SELECT username FROM auth_user WHERE id = %s",
                                                               [int(user_id)])
                                                username = [row[0] for row in cursor.fetchall()][0]
                                                table_name_user = f"notes_{username}"
                                            with connection.cursor() as cursor:
                                                cursor.execute(f"SELECT id FROM {table_name_user} WHERE title = %s",
                                                               [title])
                                                id_title_user = [row[0] for row in cursor.fetchall()][0]
                                            with connection.cursor() as cursor:
                                                cursor.execute(
                                                    f"UPDATE {table_name_user} SET content_user1 = %s WHERE id = %s",
                                                    [data_user, id_title_user])
                                    with connection.cursor() as cursor:
                                        cursor.execute(f"SELECT username FROM auth_user WHERE id = %s",
                                                       [int(user_id_author)])
                                        username = [row[0] for row in cursor.fetchall()][0]
                                        table_name_author = f"notes_{username}"
                                    with connection.cursor() as cursor:
                                        cursor.execute(f"SELECT id FROM {table_name_author} WHERE title = %s",
                                                       [title])
                                        id_title_author = [row[0] for row in cursor.fetchall()][0]
                                    with connection.cursor() as cursor:
                                        cursor.execute(
                                            f"UPDATE {table_name_author} SET content_user1 = %s WHERE id = %s",
                                            [data_user, id_title_author])

                                elif str(users_id[1]) == str(user_id_received):
                                    data_user = data['content_user2']
                                    for user_id in users_id:
                                        if is_number(user_id):
                                            with connection.cursor() as cursor:
                                                cursor.execute(f"SELECT username FROM auth_user WHERE id = %s",
                                                               [int(user_id)])
                                                username = [row[0] for row in cursor.fetchall()][0]
                                                table_name_user = f"notes_{username}"
                                            with connection.cursor() as cursor:
                                                cursor.execute(f"SELECT id FROM {table_name_user} WHERE title = %s",
                                                               [title])
                                                id_title_user = [row[0] for row in cursor.fetchall()][0]
                                            with connection.cursor() as cursor:
                                                cursor.execute(
                                                    f"UPDATE {table_name_user} SET content_user2 = %s WHERE id = %s",
                                                    [data_user, id_title_user])
                                    with connection.cursor() as cursor:
                                        cursor.execute(f"SELECT username FROM auth_user WHERE id = %s",
                                                       [int(user_id_author)])
                                        username = [row[0] for row in cursor.fetchall()][0]
                                        table_name_author = f"notes_{username}"
                                    with connection.cursor() as cursor:
                                        cursor.execute(f"SELECT id FROM {table_name_author} WHERE title = %s",
                                                       [title])
                                        id_title_author = [row[0] for row in cursor.fetchall()][0]
                                    with connection.cursor() as cursor:
                                        cursor.execute(
                                            f"UPDATE {table_name_author} SET content_user2 = %s WHERE id = %s",
                                            [data_user, id_title_author])

                                elif str(users_id[2]) == str(user_id_received):
                                    data_user = data['content_user3']
                                    for user_id in users_id:
                                        if is_number(user_id):
                                            with connection.cursor() as cursor:
                                                cursor.execute(f"SELECT username FROM auth_user WHERE id = %s",
                                                               [int(user_id)])
                                                username = [row[0] for row in cursor.fetchall()][0]
                                                table_name_user = f"notes_{username}"
                                            with connection.cursor() as cursor:
                                                cursor.execute(f"SELECT id FROM {table_name_user} WHERE title = %s",
                                                               [title])
                                                id_title_user = [row[0] for row in cursor.fetchall()][0]
                                            with connection.cursor() as cursor:
                                                cursor.execute(
                                                    f"UPDATE {table_name_user} SET content_user3 = %s WHERE id = %s",
                                                    [data_user, id_title_user])
                                    with connection.cursor() as cursor:
                                        cursor.execute(f"SELECT username FROM auth_user WHERE id = %s",
                                                       [int(user_id_author)])
                                        username = [row[0] for row in cursor.fetchall()][0]
                                        table_name_author = f"notes_{username}"
                                    with connection.cursor() as cursor:
                                        cursor.execute(f"SELECT id FROM {table_name_author} WHERE title = %s",
                                                       [title])
                                        id_title_author = [row[0] for row in cursor.fetchall()][0]
                                    with connection.cursor() as cursor:
                                        cursor.execute(
                                            f"UPDATE {table_name_author} SET content_user3 = %s WHERE id = %s",
                                            [data_user, id_title_author])
                        else:
                            title = data['note']
                            user_id = decoded_payload['id']
                            content_author = data['content']
                            login = decoded_payload['user']
                            with connection.cursor() as cursor:
                                cursor.execute(f"SELECT id FROM auth_user WHERE username = '{login}'")
                                id_user = [row[0] for row in cursor.fetchall()][0]
                            if str(id_user) == str(user_id):
                                with connection.cursor() as cursor:
                                    cursor.execute(
                                        f"INSERT INTO {table_user} (user_id, title, content_author, user1_id, content_user1, "
                                        f"user2_id, content_user2, user3_id, content_user3) VALUES "
                                        f"({id_user}, %s, %s, NULL, NULL, NULL, NULL, NULL, NULL)", [title, content_author])
                            else:
                                for i in range(1, 4):
                                    if id_user == data[f'user{i}_id']:
                                        content_user = data[f'content_user{i}']
                                        with connection.cursor() as cursor:
                                            cursor.execute(
                                                f"INSERT INTO {table_user} (user_id, title, content_author, user1_id, content_user1, "
                                                f"user2_id, content_user2, user3_id, content_user3) VALUES "
                                                f"({id_user}, %s, %s, NULL, NULL, NULL, NULL, NULL, NULL)", [title, content_user])

                        return JsonResponse({'message': 'данные были обработаны'})
                    else:
                        return JsonResponse({'error': 'Данные были изменены'})
                except jwt.InvalidTokenError:
                    return JsonResponse({'error': 'Неправильный jwt_token!'})
            else:
                return JsonResponse({'error': 'Введенного логина не существует или неправильынй пароль'})
        except:
            return JsonResponse({'error': 'Ошибка на сервере'})
    else:
        return JsonResponse({'error': 'Ошибка на сервере'}, status=400)
