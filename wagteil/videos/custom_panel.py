import functools

from django.core.exceptions import FieldDoesNotExist
from django.db.models import ForeignKey
from django.template.loader import get_template
from django.utils.functional import cached_property
from django.utils.text import capfirst

from wagtail.admin.forms.models import registry as model_field_registry
from wagtail.admin.panels import Panel
from wagtail.blocks import BlockField
from wagtailvideos.edit_handlers import VideoChooserPanel


class VideoChooserCustomPanel(VideoChooserPanel):
    class BoundPanel(Panel.BoundPanel):
        template_name = "custom_field_panel.html"
        # Default icons for common model field types,
        # based on the corresponding FieldBlock's icon.
        default_field_icons = {
            "DateField": "date",
            "TimeField": "time",
            "DateTimeField": "date",
            "URLField": "link-external",
            "TaggableManager": "tag",
            "EmailField": "mail",
            "TextField": "pilcrow",
            "RichTextField": "pilcrow",
            "FloatField": "decimal",
            "DecimalField": "decimal",
            "BooleanField": "tick-inverse",
        }

        def __init__(self, **kwargs):
            super().__init__(**kwargs)

            self.bound_field = None
            self.read_only = False

            if self.form is None:
                return

            try:
                self.bound_field = self.form[self.field_name]
            except KeyError:
                if self.panel.read_only:
                    self.read_only = True
                    # Ensure heading and help_text are set to something useful
                    self.heading = self.panel.heading or capfirst(
                        self.panel.db_field.verbose_name
                    )
                    self.help_text = self.panel.help_text or capfirst(
                        self.panel.db_field.help_text
                    )
                return

            # Ensure heading and help_text are consistent across
            # Panel, BoundPanel and Field
            if self.panel.heading:
                self.heading = self.bound_field.label = self.panel.heading
            else:
                self.heading = self.bound_field.label

            self.help_text = self.panel.help_text or self.bound_field.help_text

        @property
        def field_name(self):
            return self.panel.field_name

        def is_shown(self):
            if (
                self.form is not None
                and self.bound_field is None
                and not self.read_only
            ):
                # this field is missing from the form
                return False

            if (
                self.panel.permission
                and self.request
                and not self.request.user.has_perm(self.panel.permission)
            ):
                return False

            return True

        def is_required(self):
            if self.bound_field is None:
                return False
            return self.bound_field.field.required

        def classes(self):
            classes = self.panel.classes()
            if self.bound_field and isinstance(self.bound_field.field, BlockField):
                classes.append("w-panel--nested")
            return classes

        @property
        def icon(self):
            """
            Display a different icon depending on the field's type.
            """
            # If the panel has an icon, use that.
            if self.panel.icon:
                return self.panel.icon

            # Try to use the model field first, then the form field because it's
            # possible to use FieldPanel without a model field by using a custom
            # form class.
            try:
                field = self.panel.db_field
            except FieldDoesNotExist:
                # The defined default icons are for model fields, but most of them
                # have a corresponding form field with the same name, so we just
                # hope the name matches.
                field = self.bound_field.field

            field_type = type(field)

            # ForeignKey fields can have a custom icon defined in the form field's widget
            # (e.g. page, image, and document choosers). If there's an overridden widget
            # with an icon attribute, use that.
            if issubclass(field_type, ForeignKey):
                overrides = model_field_registry.get(field) or {}
                widget = overrides.get("widget", None)
                return getattr(widget, "icon", None)

            # Otherwise, find a default icon based on the field's class or superclasses.
            for field_class in field_type.mro():
                field_name = field_class.__name__
                if field_name in self.default_field_icons:
                    return self.default_field_icons[field_name]

            return None

        def id_for_label(self):
            if self.read_only:
                return self.prefix
            return self.bound_field.id_for_label

        @property
        def comments_enabled(self):
            if self.panel.disable_comments is None and not self.read_only:
                # by default, enable comments on all fields except StreamField (which has its own comment handling)
                return not isinstance(self.bound_field.field, BlockField)
            else:
                return not self.panel.disable_comments

        @cached_property
        def value_from_instance(self):
            return getattr(self.instance, self.field_name)

        def get_context_data(self, parent_context=None):
            context = super().get_context_data(parent_context)

            if hasattr(context['self'], 'instance') and context['self'].instance.header_video is not None:
                context['video_url'] = context['self'].instance.header_video.file.url
            if self.read_only:
                context.update(self.get_read_only_context_data())
            else:
                context.update(self.get_editable_context_data())
            return context

        def get_editable_context_data(self):
            widget_described_by_ids = []
            help_text_id = "%s-helptext" % self.prefix
            error_message_id = "%s-errors" % self.prefix

            widget_described_by_ids = []
            if self.help_text:
                widget_described_by_ids.append(help_text_id)

            if self.bound_field.errors:
                widget = self.bound_field.field.widget
                if hasattr(widget, "render_with_errors"):
                    widget_attrs = {
                        "id": self.bound_field.auto_id,
                    }
                    if widget_described_by_ids:
                        widget_attrs["aria-describedby"] = " ".join(
                            widget_described_by_ids
                        )

                    rendered_field = widget.render_with_errors(
                        self.bound_field.html_name,
                        self.bound_field.value(),
                        attrs=widget_attrs,
                        errors=self.bound_field.errors,
                    )
                else:
                    widget_described_by_ids.append(error_message_id)
                    rendered_field = self.bound_field.as_widget(
                        attrs={
                            "aria-invalid": "true",
                            "aria-describedby": " ".join(widget_described_by_ids),
                        }
                    )
            else:
                widget_attrs = {}
                if widget_described_by_ids:
                    widget_attrs["aria-describedby"] = " ".join(widget_described_by_ids)

                rendered_field = self.bound_field.as_widget(attrs=widget_attrs)

            return {
                "field": self.bound_field,
                "rendered_field": rendered_field,
                "error_message_id": error_message_id,
                "help_text": self.help_text,
                "help_text_id": help_text_id,
                "show_add_comment_button": self.comments_enabled
                and getattr(
                    self.bound_field.field.widget,
                    "show_add_comment_button",
                    True,
                ),
            }

        def get_read_only_context_data(self):
            # Define context data for BoundPanel AND read-only output rendering
            context = {
                "id_for_label": self.id_for_label(),
                "help_text_id": "%s-helptext" % self.prefix,
                "help_text": self.help_text,
                "show_add_comment_button": self.comments_enabled,
                "raw_value": self.value_from_instance,
                "display_value": self.panel.format_value_for_display(
                    self.value_from_instance
                ),
            }

            # Render read-only output
            template = get_template(self.panel.read_only_output_template_name)
            rendered_field = template.render(context)

            # Add rendered output to BoundPanel context data
            context["rendered_field"] = rendered_field
            return context

        def get_comparison(self):
            comparator_class = self.panel.get_comparison_class()

            if comparator_class and self.is_shown():
                try:
                    return [functools.partial(comparator_class, self.panel.db_field)]
                except FieldDoesNotExist:
                    return []
            return []

        def __repr__(self):
            return "<{} '{}' with model={} instance={} request={} form={}>".format(
                self.__class__.__name__,
                self.field_name,
                self.panel.model,
                self.instance,
                self.request,
                self.form.__class__.__name__,
            )