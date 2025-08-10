# Generated manually

from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_todo_user'),
    ]

    operations = [
        migrations.RunSQL(
            "DROP TABLE IF EXISTS app_todo;",
            reverse_sql=""
        ),
        migrations.RunSQL(
            """
            CREATE TABLE app_category (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(100) NOT NULL,
                color VARCHAR(7) NOT NULL,
                user_id INTEGER NOT NULL,
                created_at DATETIME NOT NULL,
                FOREIGN KEY (user_id) REFERENCES auth_user (id)
            );
            """,
            reverse_sql="DROP TABLE IF EXISTS app_category;"
        ),
        migrations.RunSQL(
            """
            CREATE TABLE app_todo (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title VARCHAR(200) NOT NULL,
                description TEXT,
                status VARCHAR(20) NOT NULL,
                priority VARCHAR(10) NOT NULL,
                completed BOOLEAN NOT NULL,
                due_date DATETIME,
                created_at DATETIME NOT NULL,
                updated_at DATETIME NOT NULL,
                todo_order INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                category_id INTEGER,
                FOREIGN KEY (user_id) REFERENCES auth_user (id),
                FOREIGN KEY (category_id) REFERENCES app_category (id)
            );
            """,
            reverse_sql="DROP TABLE IF EXISTS app_todo;"
        ),
        migrations.RunSQL(
            """
            CREATE TABLE app_note (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT NOT NULL,
                created_at DATETIME NOT NULL,
                updated_at DATETIME NOT NULL,
                todo_id INTEGER NOT NULL,
                FOREIGN KEY (todo_id) REFERENCES app_todo (id)
            );
            """,
            reverse_sql="DROP TABLE IF EXISTS app_note;"
        ),
    ]
