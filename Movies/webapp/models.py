from django.db import models


class GeeksModel(models.Model):
    title = models.CharField(max_length=200)
    img = models.ImageField(upload_to="webapp/static/images/upload/profile_picture/")

    def __str__(self):
        return self.title
