from django.db import models
class Member(models.Model):
    name = models.CharField('user name',max_length=20, null=False)
    age = models.PositiveIntegerField('age',default=0)

    deleted = models.BooleanField('削除',default=0)
    image = models.ImageField('画像', upload_to="member/", blank=True, null=True)

    def __str__(self):
        return self.name
# Create your models here.
