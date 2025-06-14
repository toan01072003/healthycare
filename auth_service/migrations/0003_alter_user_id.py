from django.db import migrations, models
import uuid

class Migration(migrations.Migration):
    dependencies = [
        ('auth_service', '0002_user_is_staff_alter_user_is_superuser'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='id',
            field=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False),
        ),
    ]

