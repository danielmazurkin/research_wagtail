from django.db import models
from django.forms.utils import flatatt
from django.utils.html import format_html, format_html_join
from wagtail import blocks
from wagtail.admin.panels import FieldPanel
from wagtail.fields import StreamField
from wagtail.models import Page
from wagtailmedia.blocks import AbstractMediaChooserBlock
from wagtail.fields import RichTextField
from wagtail.models import Page
from videos.custom_panel import VideoChooserCustomPanel


class TestMediaBlock(AbstractMediaChooserBlock):

    def render_basic(self, value, context=None):
        if not value:
            return ""

        if value.type == "video":
            player_code = """
            <h1> Имя файла: {3} </h1>
            <div>
                <video width="{1}" height="{2}" controls>
                    {0}
                    Your browser does not support the video tag.
                </video>
            </div>
            """
        else:
            player_code = """
            <div>
                <audio controls>
                    {0}
                    Your browser does not support the audio element.
                </audio>
            </div>
            """

        return format_html(
            player_code,
            format_html_join(
                "\n", "<source{0}>", [[flatatt(s)] for s in value.sources]
            ),
            value.width,
            value.height,
            value.title
        )


PAGE_TEMPLATE_VAR = "page"


class MediaPage(Page):
    template = "blog.html"
    author = models.CharField(max_length=255)
    date = models.DateField("Post date")
    body = StreamField(
        [
            ("heading", blocks.CharBlock(classname="title", icon="title")),
            ("paragraph", blocks.RichTextBlock(icon="pilcrow")),
            ("media", TestMediaBlock(icon="media")),
        ], use_json_field=True
    )

    content_panels = Page.content_panels + [
        FieldPanel("author"),
        FieldPanel("date"),
        FieldPanel("body"),
    ]

    class Meta:
        verbose_name = 'Страница с медиа'
        verbose_name_plural = 'Страница с медиа'


class VideoPage(Page):
    body = RichTextField()
    header_video = models.ForeignKey('wagtailvideos.Video',
                                     related_name='+',
                                     null=True,
                                     on_delete=models.SET_NULL)

    content_panels = Page.content_panels + [
        FieldPanel('body'),
        VideoChooserCustomPanel('header_video'),
    ]
