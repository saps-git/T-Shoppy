from django.db import migrations
from api.user.models import CustomUser


class Migration(migrations.Migration):
    def seed_data(apps, schema_editor):
        user = CustomUser(name="saps-admin",
                          email="saptarshi0002@gmail.com",
                          is_staff=True,
                          is_superuser=True,
                          phone="5555544444",
                          gender="Male"
                          )
        user.set_password("Admin@99")
        user.save()

    dependencies = [

    ]

    operations = [
        migrations.RunPython(seed_data),
    ]
