from django.db import models
from wagtail.admin.panels import FieldPanel


from wagtail.models import Page

from wagtailmarkdown.fields import MarkdownField

class DataIndexPage(Page):
    body = MarkdownField(default='')

    content_panels = Page.content_panels + [
        FieldPanel("body"),
    ]
