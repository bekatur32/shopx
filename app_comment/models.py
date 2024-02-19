from datetime import datetime
from django.db import models

from product.models import Product
from user_profiles.models import CustomUser

class Comment(models.Model):
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="comments",
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="comments",
    )
    # sub_comment = models.ForeignKey(
    #     "self",
    #     on_delete=models.CASCADE,
    #     related_name="subcomments",
    #     null=True,
    #     blank=True,
    # )
    photo1 = models.ImageField(upload_to="comment/%Y/%m/%d/", blank=True, null=True)
    photo2 = models.ImageField(upload_to="comment/%Y/%m/%d/", blank=True, null=True)
    photo3 = models.ImageField(upload_to="comment/%Y/%m/%d/", blank=True, null=True)
    photo4 = models.ImageField(upload_to="comment/%Y/%m/%d/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    body = models.TextField()
    # is_confirm = models.BooleanField(default=False)
    # confirmed = ConfirmedCommentManager()
    # is_sub = models.BooleanField(default=False)
    # objects = models.Manager()

    def __str__(self):
        return self.body[:20]

    # def save(self, *args, **kwargs):
    #     if self.sub_comment:
    #         self.is_sub = True

    #     if not self.register_date:
    #         self.register_date = datetime.now()

    #     super(Comment, self).save(*args, **kwargs)


