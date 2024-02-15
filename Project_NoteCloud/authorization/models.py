from django.db import models
from django.db import connection


def create_user_table(username):
    with connection.cursor() as cursor:
        cursor.execute(f"""
            CREATE TABLE notes_{username} (
                id INTEGER PRIMARY KEY AUTO_INCREMENT,
                user_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                content_author TEXT,
                user1_id INTEGER,
                content_user1 TEXT,
                user2_id INTEGER,
                content_user2 TEXT,
                user3_id INTEGER,
                content_user3 TEXT,

                CONSTRAINT fk_user
                    FOREIGN KEY (user_id)
                    REFERENCES auth_user (id),

                CONSTRAINT fk_user1
                    FOREIGN KEY (user1_id)
                    REFERENCES auth_user (id),

                CONSTRAINT fk_user2
                    FOREIGN KEY (user2_id)
                    REFERENCES auth_user (id),

                CONSTRAINT fk_user3
                    FOREIGN KEY (user3_id)
                    REFERENCES auth_user (id)
            )
        """)
