# Generated by Django 5.0.2 on 2024-03-11 04:45

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0005_alter_blog_published"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="blog",
            options={"verbose_name": "блог", "verbose_name_plural": "блоги"},
        ),
        migrations.AlterField(
            model_name="blog",
            name="content",
            field=models.TextField(verbose_name="контент"),
        ),
        migrations.AlterField(
            model_name="blog",
            name="created_at",
            field=models.DateTimeField(auto_now_add=True, verbose_name="дата создания"),
        ),
        migrations.AlterField(
            model_name="blog",
            name="preview_image",
            field=models.ImageField(
                blank=True, null=True, upload_to="blog/", verbose_name="изображение"
            ),
        ),
        migrations.AlterField(
            model_name="blog",
            name="published",
            field=models.BooleanField(default=False, verbose_name="опубликовано"),
        ),
        migrations.AlterField(
            model_name="blog",
            name="slug",
            field=models.CharField(max_length=255, verbose_name="slug"),
        ),
        migrations.AlterField(
            model_name="blog",
            name="title",
            field=models.CharField(max_length=255, verbose_name="название"),
        ),
        migrations.AlterField(
            model_name="blog",
            name="views_count",
            field=models.IntegerField(default=0, verbose_name="просмотры"),
        ),
    ]