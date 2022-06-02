from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from ckeditor.fields import RichTextField

# Create your models here.


class Post(models.Model):
    """Blog form data"""
    title = models.CharField ('Заголовок', max_length=255)
    header_image = models.ImageField('Изображение',null=True, blank=True, upload_to="images/")
    author = models.ForeignKey(User, on_delete=models.CASCADE, help_text="Выберете автора")
    body = RichTextField('Описание',blank=True, null=True)

    class Meta:
        verbose_name_plural = "Новости"
        verbose_name = "Новость"

    def __str__(self):
        return self.title + ' | Автор новости: ' + str(self.author)

    def get_absolute_url(self):
        return reverse('blog')
