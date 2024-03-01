from django.db import models

NULLABLE = {"blank": True, "null": True}


class Blog(models.Model):
    """ Blog Model """
    title = models.CharField(max_length=255, verbose_name='Title')
    slug = models.CharField(max_length=255, verbose_name='Slug')
    content = models.TextField(verbose_name='Content')
    preview_image = models.ImageField(upload_to="blog/", verbose_name='Preview_image', **NULLABLE)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created')
    published = models.BooleanField(default=False, verbose_name='Published')
    views_count = models.IntegerField(default=0, verbose_name='Views')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Blog'
        verbose_name_plural = 'Blogs'
