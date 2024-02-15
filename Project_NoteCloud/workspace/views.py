from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db import connection
from django.http import HttpResponse
from django.http import JsonResponse
import json
import codecs
from django.http import FileResponse
from io import BytesIO


@login_required(login_url='login')
def workspace(request):
    logged_in_user = request.user.username
    table_name = f"notes_{logged_in_user}"
    logged_in_user_id = request.user.id
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT title FROM {table_name}")
        titles = [row[0] for row in cursor.fetchall()]
    return render(request, 'workspace/workspace.html', {'titles': titles, 'id_user': logged_in_user_id})


def login(request):
    return redirect('authorization:login')


def logout(request):
    return redirect('authorization:logout')


def is_number(string):
    return string.isdigit()


def add_row(request):
    logged_in_user = request.user.username
    table_name = f"notes_{logged_in_user}"
    if request.method == 'POST':
        new_row_value = request.POST.get('new_row')
        if new_row_value != '':
            with connection.cursor() as cursor:
                cursor.execute(f"SELECT id FROM auth_user WHERE username = '{logged_in_user}'")
                id_user = [row[0] for row in cursor.fetchall()][0]
            with connection.cursor() as cursor:
                cursor.execute(f"INSERT INTO {table_name} (user_id, title, content_author, user1_id, content_user1, "
                               f"user2_id, content_user2, user3_id, content_user3) VALUES "
                               f"({id_user}, %s, NULL, NULL, NULL, NULL, NULL, NULL, NULL)", [new_row_value])
    return redirect('/workspace')


def delete_row(request):
    logged_in_user = request.user.username
    table_name = f"notes_{logged_in_user}"
    logged_in_user_id = request.user.id
    if request.method == 'POST':
        title = request.POST.get('title')
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT id FROM {table_name} WHERE title = %s", [title])
            id_title = [row[0] for row in cursor.fetchall()][0]
        # with connection.cursor() as cursor:
        #     cursor.execute(f"DELETE FROM {table_name} WHERE id = %s", [id_title])
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT user1_id, user2_id, user3_id FROM {table_name} WHERE id = %s", [id_title])
            users_id = []
            for row in cursor.fetchall():
                users_id.append(str(row[0]))
                users_id.append(str(row[1]))
                users_id.append(str(row[2]))
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT user_id FROM {table_name} WHERE id = %s", [id_title])
            user_id_author = [row[0] for row in cursor.fetchall()][0]
        if int(user_id_author) == int(logged_in_user_id):
            for user_id in users_id:
                if is_number(user_id):
                    with connection.cursor() as cursor:
                        cursor.execute(f"SELECT username FROM auth_user WHERE id = %s", [int(user_id)])
                        username = [row[0] for row in cursor.fetchall()][0]
                        table_name_user = f"notes_{username}"
                    with connection.cursor() as cursor:
                        cursor.execute(f"SELECT id FROM {table_name_user} WHERE title = %s", [title])
                        id_title_user = [row[0] for row in cursor.fetchall()][0]
                    with connection.cursor() as cursor:
                        cursor.execute(f"DELETE FROM {table_name_user} WHERE id = %s", [id_title_user])
            with connection.cursor() as cursor:
                cursor.execute(f"DELETE FROM {table_name} WHERE id = %s", [id_title])
        else:
            if int(users_id[0]) == int(logged_in_user_id):
                for user_id in users_id:
                    if is_number(user_id):
                        if int(user_id) != int(logged_in_user_id):
                            with connection.cursor() as cursor:
                                cursor.execute(f"SELECT username FROM auth_user WHERE id = %s", [int(user_id)])
                                username = [row[0] for row in cursor.fetchall()][0]
                                table_name_user = f"notes_{username}"
                            with connection.cursor() as cursor:
                                cursor.execute(f"SELECT id FROM {table_name_user} WHERE title = %s", [title])
                                id_title_user = [row[0] for row in cursor.fetchall()][0]
                            with connection.cursor() as cursor:
                                cursor.execute(f"UPDATE {table_name_user} SET user1_id = NULL WHERE id = %s",
                                               [id_title_user])
                            with connection.cursor() as cursor:
                                cursor.execute(f"UPDATE {table_name_user} SET content_user1 = NULL WHERE id = %s",
                                               [id_title_user])
                with connection.cursor() as cursor:
                    cursor.execute(f"SELECT username FROM auth_user WHERE id = %s", [int(user_id_author)])
                    username = [row[0] for row in cursor.fetchall()][0]
                    table_name_author = f"notes_{username}"
                with connection.cursor() as cursor:
                    cursor.execute(f"SELECT id FROM {table_name_author} WHERE title = %s", [title])
                    id_title_author = [row[0] for row in cursor.fetchall()][0]
                with connection.cursor() as cursor:
                    cursor.execute(f"UPDATE {table_name_author} SET user1_id = NULL WHERE id = %s",
                                   [id_title_author])
                with connection.cursor() as cursor:
                    cursor.execute(f"UPDATE {table_name_author} SET content_user1 = NULL WHERE id = %s",
                                   [id_title_author])
                with connection.cursor() as cursor:
                    cursor.execute(f"DELETE FROM {table_name} WHERE id = %s", [id_title])

            elif int(users_id[1]) == int(logged_in_user_id):
                for user_id in users_id:
                    if is_number(user_id):
                        if int(user_id) != int(logged_in_user_id):
                            with connection.cursor() as cursor:
                                cursor.execute(f"SELECT username FROM auth_user WHERE id = %s", [int(user_id)])
                                username = [row[0] for row in cursor.fetchall()][0]
                                table_name_user = f"notes_{username}"
                            with connection.cursor() as cursor:
                                cursor.execute(f"SELECT id FROM {table_name_user} WHERE title = %s", [title])
                                id_title_user = [row[0] for row in cursor.fetchall()][0]
                            with connection.cursor() as cursor:
                                cursor.execute(f"UPDATE {table_name_user} SET user2_id = NULL WHERE id = %s",
                                               [id_title_user])
                            with connection.cursor() as cursor:
                                cursor.execute(f"UPDATE {table_name_user} SET content_user2 = NULL WHERE id = %s",
                                               [id_title_user])
                    with connection.cursor() as cursor:
                        cursor.execute(f"SELECT username FROM auth_user WHERE id = %s", [int(user_id_author)])
                        username = [row[0] for row in cursor.fetchall()][0]
                        table_name_author = f"notes_{username}"
                    with connection.cursor() as cursor:
                        cursor.execute(f"SELECT id FROM {table_name_author} WHERE title = %s", [title])
                        id_title_author = [row[0] for row in cursor.fetchall()][0]
                    with connection.cursor() as cursor:
                        cursor.execute(f"UPDATE {table_name_author} SET user2_id = NULL WHERE id = %s",
                                       [id_title_author])
                    with connection.cursor() as cursor:
                        cursor.execute(f"UPDATE {table_name_author} SET content_user2 = NULL WHERE id = %s",
                                       [id_title_author])
                    with connection.cursor() as cursor:
                        cursor.execute(f"DELETE FROM {table_name} WHERE id = %s", [id_title])

            elif int(users_id[2]) == int(logged_in_user_id):
                for user_id in users_id:
                    if is_number(user_id):
                        if int(user_id) != int(logged_in_user_id):
                            with connection.cursor() as cursor:
                                cursor.execute(f"SELECT username FROM auth_user WHERE id = %s", [int(user_id)])
                                username = [row[0] for row in cursor.fetchall()][0]
                                table_name_user = f"notes_{username}"
                            with connection.cursor() as cursor:
                                cursor.execute(f"SELECT id FROM {table_name_user} WHERE title = %s", [title])
                                id_title_user = [row[0] for row in cursor.fetchall()][0]
                            with connection.cursor() as cursor:
                                cursor.execute(f"UPDATE {table_name_user} SET user3_id = NULL WHERE id = %s",
                                               [id_title_user])
                            with connection.cursor() as cursor:
                                cursor.execute(f"UPDATE {table_name_user} SET content_user3 = NULL WHERE id = %s",
                                               [id_title_user])
                    with connection.cursor() as cursor:
                        cursor.execute(f"SELECT username FROM auth_user WHERE id = %s", [int(user_id_author)])
                        username = [row[0] for row in cursor.fetchall()][0]
                        table_name_author = f"notes_{username}"
                    with connection.cursor() as cursor:
                        cursor.execute(f"SELECT id FROM {table_name_author} WHERE title = %s", [title])
                        id_title_author = [row[0] for row in cursor.fetchall()][0]
                    with connection.cursor() as cursor:
                        cursor.execute(f"UPDATE {table_name_author} SET user3_id = NULL WHERE id = %s",
                                       [id_title_author])
                    with connection.cursor() as cursor:
                        cursor.execute(f"UPDATE {table_name_author} SET content_user3 = NULL WHERE id = %s",
                                       [id_title_author])
                    with connection.cursor() as cursor:
                        cursor.execute(f"DELETE FROM {table_name} WHERE id = %s", [id_title])

    return redirect('/workspace')


def textarea_view(request):
    logged_in_user = request.user.username
    table_name = f"notes_{logged_in_user}"
    logged_in_user_id = request.user.id
    if request.method == 'POST':
        title = request.POST.get('title')
        if title:
            with connection.cursor() as cursor:
                cursor.execute(f"SELECT id FROM {table_name} WHERE title = %s", [title])
                id_title = [row[0] for row in cursor.fetchall()][0]
            with connection.cursor() as cursor:
                cursor.execute(f"SELECT content_author FROM {table_name} WHERE id = %s", [id_title])
                content_author = [row[0] for row in cursor.fetchall()][0]
            with connection.cursor() as cursor:
                cursor.execute(f"SELECT title FROM {table_name}")
                titles = [row[0] for row in cursor.fetchall()]
            with connection.cursor() as cursor:
                cursor.execute(f"SELECT content_user1 FROM {table_name} WHERE id = %s", [id_title])
                content_user1 = [row[0] for row in cursor.fetchall()][0]
            with connection.cursor() as cursor:
                cursor.execute(f"SELECT content_user2 FROM {table_name} WHERE id = %s", [id_title])
                content_user2 = [row[0] for row in cursor.fetchall()][0]
            with connection.cursor() as cursor:
                cursor.execute(f"SELECT content_user3 FROM {table_name} WHERE id = %s", [id_title])
                content_user3 = [row[0] for row in cursor.fetchall()][0]
            with connection.cursor() as cursor:
                cursor.execute(f"SELECT user_id, user1_id, user2_id, user3_id FROM {table_name} WHERE id = %s", [id_title])
                users_id = []
                for row in cursor.fetchall():
                    users_id.append(row[0])
                    users_id.append(row[1])
                    users_id.append(row[2])
                    users_id.append(row[3])

            with connection.cursor() as cursor:
                usernames = []
                for user_id in users_id:
                    if user_id:
                        cursor.execute(f"SELECT username FROM auth_user WHERE id = %s", [int(user_id)])
                        username = [row[0] for row in cursor.fetchall()][0]
                        usernames.append(username)
                    else:
                        usernames.append('None')
        return render(request, 'workspace/workspace.html', {'content_author': content_author, 'title': title, 'titles': titles,
                                                            'id_user': logged_in_user_id, 'content_user1': content_user1,
                                                            'content_user2': content_user2, 'content_user3': content_user3,
                                                            'author_id': users_id[0], 'user1_id': users_id[1], 'user2_id': users_id[2], 'user3_id': users_id[3],
                                                            'username_author': usernames[0], 'username_user1': usernames[1], 'username_user2': usernames[2], 'username_user3': usernames[3]})


def save_data(request):
    logged_in_user = request.user.username
    logged_in_user_id = request.user.id
    table_name = f"notes_{logged_in_user}"
    if request.method == 'POST':
        title = request.POST.get('title', '')
        if title:
            with connection.cursor() as cursor:
                cursor.execute(f"SELECT id FROM {table_name} WHERE title = %s", [title])
                id_title = [row[0] for row in cursor.fetchall()][0]
            with connection.cursor() as cursor:
                cursor.execute(f"SELECT user1_id, user2_id, user3_id FROM {table_name} WHERE id = %s", [id_title])
                users_id = []
                for row in cursor.fetchall():
                    users_id.append(str(row[0]))
                    users_id.append(str(row[1]))
                    users_id.append(str(row[2]))
            with connection.cursor() as cursor:
                cursor.execute(f"SELECT user_id FROM {table_name} WHERE id = %s", [id_title])
                user_id_author = [row[0] for row in cursor.fetchall()][0]
            if str(user_id_author) == str(logged_in_user_id):
                data_author = request.POST.get('data_author', '')
                for user_id in users_id:
                    if is_number(user_id):
                        with connection.cursor() as cursor:
                            cursor.execute(f"SELECT username FROM auth_user WHERE id = %s", [int(user_id)])
                            username = [row[0] for row in cursor.fetchall()][0]
                            table_name_user = f"notes_{username}"
                        with connection.cursor() as cursor:
                            cursor.execute(f"SELECT id FROM {table_name_user} WHERE title = %s", [title])
                            id_title_user = [row[0] for row in cursor.fetchall()][0]
                        with connection.cursor() as cursor:
                            cursor.execute(f"UPDATE {table_name_user} SET content_author = %s WHERE id = %s", [data_author, id_title_user])
                with connection.cursor() as cursor:
                    cursor.execute(f"SELECT id FROM {table_name} WHERE title = %s", [title])
                    id_title = [row[0] for row in cursor.fetchall()][0]
                with connection.cursor() as cursor:
                    cursor.execute(f"UPDATE {table_name} SET content_author = %s WHERE id = %s", [data_author, id_title])
            else:
                if str(users_id[0]) == str(logged_in_user_id):
                    data_user = request.POST.get('data_user1', '')
                    for user_id in users_id:
                        if is_number(user_id):
                            with connection.cursor() as cursor:
                                cursor.execute(f"SELECT username FROM auth_user WHERE id = %s", [int(user_id)])
                                username = [row[0] for row in cursor.fetchall()][0]
                                table_name_user = f"notes_{username}"
                            with connection.cursor() as cursor:
                                cursor.execute(f"SELECT id FROM {table_name_user} WHERE title = %s", [title])
                                id_title_user = [row[0] for row in cursor.fetchall()][0]
                            with connection.cursor() as cursor:
                                cursor.execute(f"UPDATE {table_name_user} SET content_user1 = %s WHERE id = %s",
                                               [data_user, id_title_user])
                    with connection.cursor() as cursor:
                        cursor.execute(f"SELECT username FROM auth_user WHERE id = %s", [int(user_id_author)])
                        username = [row[0] for row in cursor.fetchall()][0]
                        table_name_author = f"notes_{username}"
                    with connection.cursor() as cursor:
                        cursor.execute(f"SELECT id FROM {table_name_author} WHERE title = %s", [title])
                        id_title_author = [row[0] for row in cursor.fetchall()][0]
                    with connection.cursor() as cursor:
                        cursor.execute(f"UPDATE {table_name_author} SET content_user1 = %s WHERE id = %s",
                                       [data_user, id_title_author])

                elif str(users_id[1]) == str(logged_in_user_id):
                    data_user = request.POST.get('data_user2', '')
                    for user_id in users_id:
                        if is_number(user_id):
                            with connection.cursor() as cursor:
                                cursor.execute(f"SELECT username FROM auth_user WHERE id = %s", [int(user_id)])
                                username = [row[0] for row in cursor.fetchall()][0]
                                table_name_user = f"notes_{username}"
                            with connection.cursor() as cursor:
                                cursor.execute(f"SELECT id FROM {table_name_user} WHERE title = %s", [title])
                                id_title_user = [row[0] for row in cursor.fetchall()][0]
                            with connection.cursor() as cursor:
                                cursor.execute(f"UPDATE {table_name_user} SET content_user2 = %s WHERE id = %s",
                                               [data_user, id_title_user])
                    with connection.cursor() as cursor:
                        cursor.execute(f"SELECT username FROM auth_user WHERE id = %s", [int(user_id_author)])
                        username = [row[0] for row in cursor.fetchall()][0]
                        table_name_author = f"notes_{username}"
                    with connection.cursor() as cursor:
                        cursor.execute(f"SELECT id FROM {table_name_author} WHERE title = %s", [title])
                        id_title_author = [row[0] for row in cursor.fetchall()][0]
                    with connection.cursor() as cursor:
                        cursor.execute(f"UPDATE {table_name_author} SET content_user2 = %s WHERE id = %s",
                                       [data_user, id_title_author])

                elif str(users_id[2]) == str(logged_in_user_id):
                    data_user = request.POST.get('data_user3', '')
                    for user_id in users_id:
                        if is_number(user_id):
                            with connection.cursor() as cursor:
                                cursor.execute(f"SELECT username FROM auth_user WHERE id = %s", [int(user_id)])
                                username = [row[0] for row in cursor.fetchall()][0]
                                table_name_user = f"notes_{username}"
                            with connection.cursor() as cursor:
                                cursor.execute(f"SELECT id FROM {table_name_user} WHERE title = %s", [title])
                                id_title_user = [row[0] for row in cursor.fetchall()][0]
                            with connection.cursor() as cursor:
                                cursor.execute(f"UPDATE {table_name_user} SET content_user3 = %s WHERE id = %s",
                                               [data_user, id_title_user])
                    with connection.cursor() as cursor:
                        cursor.execute(f"SELECT username FROM auth_user WHERE id = %s", [int(user_id_author)])
                        username = [row[0] for row in cursor.fetchall()][0]
                        table_name_author = f"notes_{username}"
                    with connection.cursor() as cursor:
                        cursor.execute(f"SELECT id FROM {table_name_author} WHERE title = %s", [title])
                        id_title_author = [row[0] for row in cursor.fetchall()][0]
                    with connection.cursor() as cursor:
                        cursor.execute(f"UPDATE {table_name_author} SET content_user3 = %s WHERE id = %s",
                                       [data_user, id_title_author])

    return textarea_view(request)


def share(request):
    logged_in_user = request.user.username
    table_name = f"notes_{logged_in_user}"
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT title FROM {table_name}")
        titles = [row[0] for row in cursor.fetchall()]
    return render(request, 'workspace/share.html', {'titles': titles})


def send_share(request):
    logged_in_user_id = request.user.id
    logged_in_user = request.user.username
    table_name = f"notes_{logged_in_user}"
    if request.method == 'POST':
        title = request.POST.get('title')
        if title:
            with connection.cursor() as cursor:
                cursor.execute(f"SELECT title FROM {table_name}")
                titles = [row[0] for row in cursor.fetchall()]
            with connection.cursor() as cursor:
                cursor.execute(f"SELECT id FROM {table_name} WHERE title = %s", [title])
                id_title = [row[0] for row in cursor.fetchall()][0]
            with connection.cursor() as cursor:
                cursor.execute(f"SELECT user_id, user1_id, user2_id, user3_id FROM {table_name} WHERE id = %s", [id_title])
                users_id = []
                for row in cursor.fetchall():
                    users_id.append(row[0])
                    users_id.append(row[1])
                    users_id.append(row[2])
                    users_id.append(row[3])

        return render(request, 'workspace/share.html', {'titles': titles, 'title': title, 'user1_id': users_id[1],
                                                        'user2_id': users_id[2], 'user3_id': users_id[3],
                                                        'logged_in_user_id': logged_in_user_id, 'author_id': users_id[0]})


def save_share(request):
    logged_in_user = request.user.username
    logged_in_user_id = request.user.id
    table_name = f"notes_{logged_in_user}"
    if request.method == 'POST':
        title = request.POST.get('title', '')
        user1 = request.POST.get('user1', '')
        user2 = request.POST.get('user2', '')
        user3 = request.POST.get('user3', '')
        users_id_new = []
        users_id_new.append(str(user1))
        users_id_new.append(str(user2))
        users_id_new.append(str(user3))

        if title:
            with connection.cursor() as cursor:
                cursor.execute(f"SELECT id FROM {table_name} WHERE title = %s", [title])
                id_title = [row[0] for row in cursor.fetchall()][0]
            with connection.cursor() as cursor:
                cursor.execute(f"SELECT user_id FROM {table_name} WHERE id = %s", [id_title])
                user_id = [row[0] for row in cursor.fetchall()][0]

            if int(user_id) == int(logged_in_user_id):
                with connection.cursor() as cursor:
                    cursor.execute(f"SELECT user1_id, user2_id, user3_id FROM {table_name} WHERE id = %s", [id_title])
                    users_id_old = []
                    for row in cursor.fetchall():
                        users_id_old.append(str(row[0]))
                        users_id_old.append(str(row[1]))
                        users_id_old.append(str(row[2]))
                for i in range(0, len(users_id_old)):
                    if users_id_new[i] != users_id_old[i]:
                        if is_number(users_id_new[i]):
                            with connection.cursor() as cursor:
                                cursor.execute(f"SELECT title FROM {table_name} WHERE id = %s", [id_title])
                                title = [row[0] for row in cursor.fetchall()][0]
                            with connection.cursor() as cursor:
                                cursor.execute(f"SELECT username FROM auth_user WHERE id = %s", [users_id_new[i]])
                                username = [row[0] for row in cursor.fetchall()][0]
                                table_name_user = f"notes_{username}"
                            with connection.cursor() as cursor:
                                cursor.execute(f"SELECT title FROM {table_name_user}")
                                titles_user = [row[0] for row in cursor.fetchall()]
                            if titles_user.count(title) == 0:
                                for j in range(0, len(users_id_old)):
                                    if i != j:
                                        if is_number(users_id_old[j]):
                                            with connection.cursor() as cursor:
                                                cursor.execute(f"SELECT title FROM {table_name} WHERE id = %s", [id_title])
                                                title = [row[0] for row in cursor.fetchall()][0]
                                            with connection.cursor() as cursor:
                                                cursor.execute(f"SELECT username FROM auth_user WHERE id = %s", [users_id_old[j]])
                                                username = [row[0] for row in cursor.fetchall()][0]
                                                table_name_user = f"notes_{username}"
                                            with connection.cursor() as cursor:
                                                cursor.execute(f"SELECT id FROM {table_name_user} WHERE title = %s", [title])
                                                id_title_user = [row[0] for row in cursor.fetchall()][0]
                                            with connection.cursor() as cursor:
                                                cursor.execute(f"UPDATE {table_name_user} SET user{i+1}_id = %s WHERE id = %s",
                                                               [users_id_new[i], id_title_user])
                                    else:
                                        with connection.cursor() as cursor:
                                            cursor.execute(f"UPDATE {table_name} SET user{i+1}_id = %s WHERE id = %s",
                                                           [users_id_new[i], id_title])
                                        with connection.cursor() as cursor:
                                            cursor.execute(
                                                f"SELECT user_id, title, content_author, user1_id, content_user1, "
                                                f"user2_id, content_user2, user3_id, content_user3 FROM {table_name} WHERE id = %s",
                                                [id_title])
                                            for row in cursor.fetchall():
                                                data = row
                                        with connection.cursor() as cursor:
                                            cursor.execute(f"SELECT username FROM auth_user WHERE id = %s",
                                                           [users_id_new[i]])
                                            username = [row[0] for row in cursor.fetchall()][0]
                                            table_name_user = f"notes_{username}"
                                        with connection.cursor() as cursor:
                                            cursor.execute(
                                                f"INSERT INTO {table_name_user} (user_id, title, content_author, user1_id, content_user1, "
                                                f"user2_id, content_user2, user3_id, content_user3) "
                                                f"VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                                                [data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8]]
                                            )

                                        if is_number(users_id_old[i]):
                                            with connection.cursor() as cursor:
                                                cursor.execute(f"SELECT username FROM auth_user WHERE id = %s", [users_id_old[i]])
                                                username = [row[0] for row in cursor.fetchall()][0]
                                                table_name_user = f"notes_{username}"
                                            with connection.cursor() as cursor:
                                                cursor.execute(f"SELECT id FROM {table_name_user} WHERE title = %s", [title])
                                                id_title_delete = [row[0] for row in cursor.fetchall()][0]
                                            with connection.cursor() as cursor:
                                                cursor.execute(f"DELETE FROM {table_name_user} WHERE id = %s", [id_title_delete])
                        else:
                            if users_id_new[i] == 'None' or users_id_new[i] == 'NULL' or users_id_new[i] == '':
                                with connection.cursor() as cursor:
                                    cursor.execute(f"SELECT title FROM {table_name} WHERE id = %s", [id_title])
                                    title = [row[0] for row in cursor.fetchall()][0]
                                for j in range(0, len(users_id_old)):
                                    if i != j:
                                        if is_number(users_id_old[j]):
                                            with connection.cursor() as cursor:
                                                cursor.execute(f"SELECT title FROM {table_name} WHERE id = %s",
                                                               [id_title])
                                                title = [row[0] for row in cursor.fetchall()][0]
                                            with connection.cursor() as cursor:
                                                cursor.execute(f"SELECT username FROM auth_user WHERE id = %s",
                                                               [users_id_old[j]])
                                                username = [row[0] for row in cursor.fetchall()][0]
                                                table_name_user = f"notes_{username}"
                                            with connection.cursor() as cursor:
                                                cursor.execute(f"SELECT id FROM {table_name_user} WHERE title = %s",
                                                               [title])
                                                id_title_user = [row[0] for row in cursor.fetchall()][0]
                                            with connection.cursor() as cursor:
                                                cursor.execute(
                                                    f"UPDATE {table_name_user} SET user{i + 1}_id = NULL WHERE id = %s",
                                                    [id_title_user])
                                            with connection.cursor() as cursor:
                                                cursor.execute(
                                                    f"UPDATE {table_name_user} SET content_user{i + 1} = NULL WHERE id = %s",
                                                    [id_title_user])
                                    else:
                                        with connection.cursor() as cursor:
                                            cursor.execute(
                                                f"UPDATE {table_name} SET user{i + 1}_id = NULL WHERE id = %s",
                                                [id_title])
                                        with connection.cursor() as cursor:
                                            cursor.execute(
                                                f"UPDATE {table_name} SET content_user{i + 1} = NULL WHERE id = %s",
                                                [id_title])

                                        with connection.cursor() as cursor:
                                            cursor.execute(f"SELECT username FROM auth_user WHERE id = %s",
                                                           [users_id_old[i]])
                                            username = [row[0] for row in cursor.fetchall()][0]
                                            table_name_user = f"notes_{username}"
                                        with connection.cursor() as cursor:
                                            cursor.execute(f"SELECT id FROM {table_name_user} WHERE title = %s",
                                                           [title])
                                            id_title_delete = [row[0] for row in cursor.fetchall()][0]
                                        with connection.cursor() as cursor:
                                            cursor.execute(f"DELETE FROM {table_name_user} WHERE id = %s",
                                                           [id_title_delete])

    return send_share(request)


def download_file(request):
    if request.method == 'POST':
        title = request.POST.get('title', '')
        if title:
            data_author = request.POST.get('hidden_data_author', '')
            data_user1 = request.POST.get('hidden_data_user1', '')
            data_user2 = request.POST.get('hidden_data_user2', '')
            data_user3 = request.POST.get('hidden_data_user3', '')
            username_author = request.POST.get('hidden_username_author', '')
            if username_author == 'None':
                username_author = ''
                data_author = ''
            username_user1 = request.POST.get('hidden_username_user1', '')
            if username_user1 == 'None':
                username_user1 = ''
                data_user1 = ''
            username_user2 = request.POST.get('hidden_username_user2', '')
            if username_user2 == 'None':
                username_user2 = ''
                data_user2 = ''
            username_user3 = request.POST.get('hidden_username_user3', '')
            if username_user3 == 'None':
                username_user3 = ''
                data_user3 = ''

            file_content = f"{username_author}\n{data_author}\n{username_user1}\n{data_user1}\n{username_user2}\n{data_user2}\n{username_user3}\n{data_user3}"

            # Создаем байтовый поток (BytesIO) и записываем содержимое файла в него, используя указанную кодировку
            byte_stream = BytesIO()
            byte_stream.write(codecs.encode(file_content, 'utf-8'))

            # Сбрасываем указатель потока в начало файла
            byte_stream.seek(0)

            # Используем FileResponse для возврата файла в ответе
            response = FileResponse(byte_stream, as_attachment=True, filename=f"{title}.txt")

            return response
        else:
            return redirect('/workspace')


# def update_content(request):
#     logged_in_user = request.user.username
#     table_name = f"notes_{logged_in_user}"
#     if request.method == 'POST':
#         title = request.POST.get('title')
#         if title:
#             with connection.cursor() as cursor:
#                 cursor.execute(f"SELECT id FROM {table_name} WHERE title = %s", [title])
#                 id_title = [row[0] for row in cursor.fetchall()][0]
#             with connection.cursor() as cursor:
#                 cursor.execute(f"SELECT content FROM {table_name} WHERE id = %s", [id_title])
#                 content = [row[0] for row in cursor.fetchall()][0]
#
#             return JsonResponse({'content': content})
#
#     return JsonResponse({'error': 'Invalid request'})


def auto_save(request):
    logged_in_user = request.user.username
    logged_in_user_id = request.user.id
    table_name = f"notes_{logged_in_user}"
    if request.method == 'POST':
        data = json.loads(request.body)
        text = data['text']
        title = data['title']
        if title:
            with connection.cursor() as cursor:
                cursor.execute(f"SELECT id FROM {table_name} WHERE title = %s", [title])
                id_title = [row[0] for row in cursor.fetchall()][0]
            with connection.cursor() as cursor:
                cursor.execute(f"SELECT user1_id, user2_id, user3_id FROM {table_name} WHERE id = %s", [id_title])
                users_id = []
                for row in cursor.fetchall():
                    users_id.append(row[0])
                    users_id.append(row[1])
                    users_id.append(row[2])
            with connection.cursor() as cursor:
                cursor.execute(f"SELECT user_id FROM {table_name} WHERE id = %s", [id_title])
                user_id_author = [row[0] for row in cursor.fetchall()][0]
            if int(user_id_author) == int(logged_in_user_id):
                with connection.cursor() as cursor:
                    cursor.execute(f"UPDATE {table_name} SET content_author = %s WHERE id = %s", [text, id_title])
            elif int(users_id[0]) == int(logged_in_user_id):
                with connection.cursor() as cursor:
                    cursor.execute(f"UPDATE {table_name} SET content_user1 = %s WHERE id = %s", [text, id_title])
            elif int(user_id_author) == int(logged_in_user_id):
                with connection.cursor() as cursor:
                    cursor.execute(f"UPDATE {table_name} SET content_user2 = %s WHERE id = %s", [text, id_title])
            elif int(user_id_author) == int(logged_in_user_id):
                with connection.cursor() as cursor:
                    cursor.execute(f"UPDATE {table_name} SET content_user3 = %s WHERE id = %s", [text, id_title])

    return JsonResponse({'error': 'Invalid request'})


def upload_file(request):
    logged_in_user = request.user.username
    logged_in_user_id = request.user.id
    table_name = f"notes_{logged_in_user}"
    if request.method == 'POST' and request.FILES['file']:
        title = request.FILES['file'].name
        title = title.rsplit(".", 1)[0]
        content = request.FILES['file'].read()
        content = content.decode('utf-8')

        with connection.cursor() as cursor:
            cursor.execute(f"INSERT INTO {table_name}(user_id, title, content_author, user1_id, content_user1, "
                           f"user2_id, content_user2, user3_id, content_user3) VALUES "
                           f"({logged_in_user_id}, %s, %s, NULL, NULL, NULL, NULL, NULL, NULL)", [title, content])

    return redirect('/workspace')
