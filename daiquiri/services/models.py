from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField

# Add these:
from wagtail.models import Page


class ServicesIndexPage(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [FieldPanel("intro")]
