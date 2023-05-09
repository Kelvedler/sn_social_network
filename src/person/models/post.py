from django.db import models

from main.models import BaseModel
from main.utils.time import to_timestamp


class Post(BaseModel):
    text = models.CharField(max_length=500)
    person = models.ForeignKey('Person', on_delete=models.CASCADE, related_name='posts')

    def as_dict(self, caller=None):
        return {
            'id': str(self.id),
            'created_at': to_timestamp(self.created_at),
            'author': self.person.as_dict(),
            'text': self.text,
            'is_liked': True if caller and self.likes.filter(person=caller).exists() else False,
            'likes_count': self.likes.count()
        }


class PostLike(BaseModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    person = models.ForeignKey('Person', on_delete=models.CASCADE, related_name='post_likes')
