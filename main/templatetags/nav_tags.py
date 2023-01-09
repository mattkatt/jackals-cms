from django import template
from main.models import FooterTextSnippet

register = template.Library()


@register.inclusion_tag('snippets/footer_text.html', takes_context=True)
def get_footer_text(context):
    footer_text = context.get('footer_text')
    if footer_text:
        return context

    footer_text = FooterTextSnippet.objects.all()

    return {
        'footer_text': footer_text
    }
