
# Create your models here.

from django.db import models
from django.utils import timezone


class Article(models.Model):
    title = models.CharField('제목', max_length=126, null=False)
    content = models.TextField('내용', null=False)
    author = models.CharField('작성자', max_length=16, null=False)
    created_at = models.DateTimeField('작성일', default=timezone.now)

    created_at.editable = True
    # 메소드 오버라이드
    def __str__(self):
        return '[{}] {}'.format(self.id, self.title)