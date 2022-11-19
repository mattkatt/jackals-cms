import datetime

from django import forms
from django.db import models
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase
from wagtail.core.models import Orderable, Page
from wagtail.core.fields import RichTextField
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.search import index
from wagtail.snippets.models import register_snippet

from main.helper_methods import append_sidebar_to_context


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
    subpage_types = []

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request)

        # filter by cat
        category = request.GET.get('category')
        library_pages = LibraryPage.objects.filter(categories__name=category, live=True)
        context['library_pages'] = library_pages

        append_sidebar_to_context(context)

        return context


class LibraryIndexPage(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full")
    ]

    subpage_types = ['library.LibraryPage', ]

    def get_context(self, request, *args, **kwargs):
        # Update context to include only published posts, ordered by reverse-chron
        context = super().get_context(request)

        library_pages = self.get_children().live().order_by('title')
        context['library_pages'] = library_pages

        append_sidebar_to_context(context)

        return context


class LibraryPageTag(TaggedItemBase):
    content_object = ParentalKey(
        'LibraryPage',
        related_name='tagged_items',
        on_delete=models.CASCADE
    )


class LibraryTagIndexPage(Page):
    subpage_types = []

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request)

        # Filter by tag
        tag = request.GET.get('tag')
        library_pages = LibraryPage.objects.filter(tags__name=tag, live=True)
        context['library_pages'] = library_pages

        append_sidebar_to_context(context)

        return context


class LibraryPage(Page):
    date = models.DateField("Post date", default=datetime.datetime.now)
    intro = models.CharField(max_length=250)
    body = RichTextField(blank=True)
    tags = ClusterTaggableManager(through=LibraryPageTag, blank=True)
    categories = ParentalManyToManyField('library.LibraryCategory', blank=True)

    subpage_types = ['library.LibraryPage']

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

        append_sidebar_to_context(context)

        return context


class LibraryPageGalleryImage(Orderable):
    page = ParentalKey(LibraryPage, on_delete=models.CASCADE, related_name='gallery_images')
    image = models.ForeignKey('wagtailimages.Image', on_delete=models.CASCADE, related_name='+')
    caption = models.CharField(blank=True, max_length=250)

    panels = [
        FieldPanel('image'),
        FieldPanel('caption'),
    ]
