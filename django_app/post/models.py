from django.conf import settings
from django.db import models


# Create your models here.
class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    created_date = models.DateTimeField(auto_now_add=True)

    def to_dict(self):
        return {
            'pk': self.pk,
            'created_date': self.created_date,
            'author': {
              self.author.to_dict()
            },
            'photo_list': [photo.to_dict() for photo in self.postphoto_set.all()]
        }


class PostPhoto(models.Model):
    post = models.ForeignKey(Post)
    photo = models.ImageField(upload_to='post')
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        order_with_respect_to = 'post'

    def to_dict(self):
        return {
            'pk': self.pk,
            'photo': self.photo.url,
        }
