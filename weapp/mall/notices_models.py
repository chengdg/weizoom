# -*- coding: utf-8 -*-
from django.db import models


class Notice(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.title

    class Meta:
        db_table = 'mall_notice'
        verbose_name = '通知'
        verbose_name_plural = '通知'
