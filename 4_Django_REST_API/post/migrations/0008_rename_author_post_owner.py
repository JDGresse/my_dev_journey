# Generated by Django 4.2.7 on 2023-11-10 12:28

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("post", "0007_remove_post_highlighted"),
    ]

    operations = [
        migrations.RenameField(
            model_name="post",
            old_name="author",
            new_name="owner",
        ),
    ]
