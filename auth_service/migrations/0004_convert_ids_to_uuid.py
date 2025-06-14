from django.db import migrations
import uuid


def convert_user_ids(apps, schema_editor):
    User = apps.get_model('auth_service', 'User')
    connection = schema_editor.connection

    referencing = []
    for model in apps.get_models():
        for field in model._meta.get_fields():
            if (field.is_relation and field.many_to_one and field.related_model == User):
                referencing.append((model._meta.db_table, field.column))

    with connection.cursor() as cursor:
        cursor.execute(f"SELECT id FROM {User._meta.db_table}")
        rows = cursor.fetchall()
        for (old_id,) in rows:
            try:
                uuid.UUID(str(old_id))
            except ValueError:
                new_id = str(uuid.uuid4())
                cursor.execute(
                    f"UPDATE {User._meta.db_table} SET id=%s WHERE id=%s",
                    [new_id, old_id],
                )
                for table, column in referencing:
                    cursor.execute(
                        f"UPDATE {table} SET {column}=%s WHERE {column}=%s",
                        [new_id, old_id],
                    )


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ('auth_service', '0003_alter_user_id'),
    ]

    operations = [
        migrations.RunPython(convert_user_ids, noop),
    ]
