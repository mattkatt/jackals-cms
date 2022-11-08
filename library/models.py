import datetime

from django import forms
from django.apps import apps
from django.db import models
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase
from wagtail.core.models import Orderable, Page
from wagtail.core.fields import RichTextField
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.search import index
from wagtail.snippets.models import register_snippet


@register_snippet
class LibraryCategory(models.Model):
    class Meta:
        verbose_name_plural = 'library categories'

    name = models.CharField(max_length=255)

    panels = [
        FieldPanel('name'),
    ]

    def __str__(self):
        return self.name


class LibraryCategoryIndexPage(Page):
    def get_context(self, request, *args, **kwargs):
        # filter by cat
        category = request.GET.get('category')
        library_pages = LibraryPage.objects.filter(categories__name=category)

        context = super().get_context(request)
        context['library_pages'] = library_pages

        library_categories = LibraryCategory.objects.all()
        context['library_categories'] = library_categories

        try:
            events: Page = apps.get_model(app_label='events', model_name='EventPage')
            latest_event = events.objects.latest('event_date')
        except Page.DoesNotExist:
            latest_event = None
        context['latest_event'] = latest_event

        return context


class LibraryIndexPage(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full")
    ]

    def get_context(self, request, *args, **kwargs):
        # Update context to include only published posts, ordered by reverse-chron
        context = super().get_context(request)

        library_pages = self.get_children().live().order_by('title')
        context['library_pages'] = library_pages

        library_categories = LibraryCategory.objects.all()
        context['library_categories'] = library_categories

        try:
            events: Page = apps.get_model(app_label='events', model_name='EventPage')
            latest_event = events.objects.latest('event_date')
        except Page.DoesNotExist:
            latest_event = None
        context['latest_event'] = latest_event

        return context


class LibraryPageTag(TaggedItemBase):
    content_object = ParentalKey(
        'LibraryPage',
        related_name='tagged_items',
        on_delete=models.CASCADE
    )


class LibraryTagIndexPage(Page):
    def get_context(self, request, *args, **kwargs):
        # Filter by tag
        tag = request.GET.get('tag')
        library_pages = LibraryPage.objects.filter(tags__name=tag)

        # Update template context
        context = super().get_context(request)
        context['library_pages'] = library_pages

        library_categories = LibraryCategory.objects.all()
        context['library_categories'] = library_categories

        try:
            events: Page = apps.get_model(app_label='events', model_name='EventPage')
            latest_event = events.objects.latest('event_date')
        except Page.DoesNotExist:
            latest_event = None
        context['latest_event'] = latest_event

        return context


class LibraryPage(Page):
    date = models.DateField("Post date", default=datetime.datetime.now)
    intro = models.CharField(max_length=250)
    body = RichTextField(blank=True)
    tags = ClusterTaggableManager(through=LibraryPageTag, blank=True)
    categories = ParentalManyToManyField('library.LibraryCategory', blank=True)

    def main_image(self):
        gallery_item = self.gallery_images.first()
        if gallery_item:
            return gallery_item.image
        else:
            return None

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
    ]

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('date'),
            FieldPanel('tags'),
            FieldPanel('categories', widget=forms.CheckboxSelectMultiple),
        ], heading='Library Page information'),
        FieldPanel('intro'),
        FieldPanel('body', classname="full"),
        InlinePanel('gallery_images', label="Gallery images"),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request)

        library_categories = LibraryCategory.objects.all()
        context['library_categories'] = library_categories

        try:
            events: Page = apps.get_model(app_label='events', model_name='EventPage')
            latest_event = events.objects.latest('event_date')
        except Page.DoesNotExist:
            latest_event = None
        context['latest_event'] = latest_event

        return context


class LibraryPageGalleryImage(Orderable):
    page = ParentalKey(LibraryPage, on_delete=models.CASCADE, related_name='gallery_images')
    image = models.ForeignKey('wagtailimages.Image', on_delete=models.CASCADE, related_name='+')
    caption = models.CharField(blank=True, max_length=250)

    panels = [
        FieldPanel('image'),
        FieldPanel('caption'),
    ]
