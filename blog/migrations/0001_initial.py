# Generated by Django 5.0.2 on 2024-03-01 14:45

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Blog",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=255, verbose_name="Title")),
                ("slug", models.CharField(max_length=255, verbose_name="Slug")),
                ("content", models.TextField(verbose_name="Content")),
                (
                    "preview_image",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to="blog/",
                        verbose_name="Preview_image",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="Created"),
                ),
                (
                    "published",
                    models.BooleanField(default=False, verbose_name="Published"),
                ),
                ("views_count", models.IntegerField(default=0, verbose_name="Views")),
            ],
            options={
                "verbose_name": "Blog",
                "verbose_name_plural": "Blogs",
            },
        ),
    ]
