from django.db import models

NULLABLE = {"blank": True, "null": True}


class Blog(models.Model):
    """ Blog Model """
    title = models.CharField(max_length=255, verbose_name='название')
    slug = models.CharField(max_length=255, verbose_name='slug')
    content = models.TextField(verbose_name='контент')
    preview_image = models.ImageField(upload_to="blog/", verbose_name='изображение', **NULLABLE)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='дата создания')
    published = models.BooleanField(default=False, verbose_name='опубликовано')
    views_count = models.IntegerField(default=0, verbose_name='просмотры')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'блог'
        verbose_name_plural = 'блоги'
