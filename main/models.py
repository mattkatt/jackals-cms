from django.db import models

from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField
from wagtail.snippets.models import register_snippet


@register_snippet
class FooterTextSnippet(models.Model):
    class Meta:
        verbose_name = 'footer text'
        verbose_name_plural = 'footer texts'
        ordering = ['display_order']

    text = RichTextField()
    display_order = models.IntegerField(default=0)

    panels = [
        FieldPanel('text'),
        FieldPanel('display_order')
    ]

    def __str__(self):
        return self.text


class AdminData(models.Model):
    class Meta:
        verbose_name = 'Admin Resource'

    resource_name = models.CharField(max_length=255)
    resource_url = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
