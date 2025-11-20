# core/admin.py

from django import forms
import core.translation
from django.contrib import admin
from django.forms.models import BaseInlineFormSet
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.db import models 
from unfold.admin import ModelAdmin
from modeltranslation.admin import TabbedTranslationAdmin
from unfold.contrib.filters.admin import RelatedDropdownFilter
from adminsortable2.admin import SortableAdminMixin
from django_ckeditor_5.widgets import CKEditor5Widget
from colorfield.fields import ColorField
from django.db import models
from .models import (
    SiteSettings, Hero, RotatingTextItem, HeroBackgroundImage,
    Section, CardBlock, NavigationItem, DropdownItem, Footer
)
from .section_registry import SECTION_TYPES, get_card_schema


# Sites framework is not used in this project

# --- Custom Widgets ---

# 1. NEW: Simple Color Input Widget
class ColorInputWidget(forms.TextInput):
    # This widget specifically forces the input type to 'color'
    def __init__(self, attrs=None):
        final_attrs = {'type': 'color'}
        if attrs:
            final_attrs.update(attrs)
        super().__init__(final_attrs)

class IconPickerWidget(forms.TextInput):
    def render(self, name, value, attrs=None, renderer=None):
        # We need to explicitly check and set the input class here since we overrode __init__ previously
        attrs = attrs or {}
        attrs['class'] = (attrs.get('class', '') + ' icon-picker-input').strip()
        attrs['placeholder'] = 'Click to select an icon'
        # Set readonly attribute to prevent manual typing which could break the kebab-case assumption
        attrs['readonly'] = 'readonly' 

        # --- FIX 1: RESTORED INPUT FIELD ---
        html = super().render(name, value, attrs, renderer)
        # -----------------------------------
        
        # Add the icon picker button
        button = format_html(
            '<button type="button" class="btn icon-picker-btn" onclick="openIconPicker(\'{}\')">Select Icon</button>',
            attrs['id'] if attrs and 'id' in attrs else ''
        )
        
        # Add clear icon button
        clear_button = format_html(
            '<button type="button" class="btn icon-clear-btn" onclick="clearIcon(\'{}\')" style="margin-left: 5px;">Clear</button>',
            attrs['id'] if attrs and 'id' in attrs else ''
        )
        
        preview = ''
        if value:
            # IMPORTANT: The JavaScript handles case conversion, so we trust the DB value is renderable here.
            preview = format_html(
                '<span class="icon-preview" id="{}_preview">'
                '<i data-lucide="{}" style="width:24px;height:24px;margin-right:8px;vertical-align:middle;"></i>'
                '{}'
                '</span>',
                attrs['id'] if attrs and 'id' in attrs else '',
                value, value
            )
        else:
            preview = format_html(
                '<span class="icon-preview" id="{}_preview">No icon selected</span>',
                attrs['id'] if attrs and 'id' in attrs else ''
            )
        # Re-added the input field (`html`) back to the wrapper
        return mark_safe(f'<div class="icon-picker-wrapper">{html}{button}{clear_button}{preview}</div>')

    class Media:
        css = {
            'all': (
                'admin/css/icon-picker.css',
            )
        }
        js = (
            'https://unpkg.com/lucide@0.446.0/dist/umd/lucide.js',
            'admin/js/icon-picker.js',
        )

# --- Custom Formset Classes ---
class SortableInlineFormSet(BaseInlineFormSet):
    """Custom formset that filters out adminsortable2 kwargs that Django doesn't accept."""
    def __init__(self, *args, **kwargs):
        # Remove kwargs that Django's BaseFormSet doesn't accept
        kwargs.pop('default_order_direction', None)
        kwargs.pop('default_order_field', None)
        super().__init__(*args, **kwargs)

# --- Forms ---
class CardBlockAdminForm(forms.ModelForm):
    class Meta:
        model = CardBlock
        fields = '__all__'
        widgets = {
            'icon': IconPickerWidget(),
            'icon_color': ColorInputWidget(),
            'button_color': ColorInputWidget(),
            'card_bg_color': ColorInputWidget(),
            'card_text_color': ColorInputWidget(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dynamic_field_configs = {}
        self.dynamic_field_names = []
        self.section_type = self._determine_section_type()
        
        # Apply field visibility and mappings based on section type
        from .section_registry import get_card_field_rules, get_field_mapping_for_section_type
        field_rules = get_card_field_rules(self.section_type)
        hidden_fields = field_rules.get('hidden_fields', [])
        field_mappings = field_rules.get('field_mappings', {})
        
        # Hide fields that shouldn't be visible for this section type
        for field_name in hidden_fields:
            if field_name in self.fields:
                self.fields[field_name].widget = forms.HiddenInput()
        
        # Apply field label and help_text mappings
        for field_name, mapping in field_mappings.items():
            if field_name in self.fields:
                if 'label' in mapping:
                    self.fields[field_name].label = mapping['label']
                if 'help_text' in mapping:
                    self.fields[field_name].help_text = mapping['help_text']
        
        # Add dynamic payload fields from schema
        schema = get_card_schema(self.section_type)
        self.schema_label = schema.get('label', 'Type-specific Settings')
        for field_config in schema.get('fields', []):
            form_field = self._build_dynamic_field(field_config)
            if not form_field:
                continue
            field_name = field_config['name']
            self.fields[field_name] = form_field
            self.dynamic_field_configs[field_name] = field_config
            self.dynamic_field_names.append(field_name)
            initial_value = None
            if self.instance and self.instance.pk:
                initial_value = self.instance.get_payload_value(field_name)
                if field_config.get('type') == 'list' and isinstance(initial_value, list):
                    initial_value = "\n".join(initial_value)
            if initial_value is not None:
                self.initial[field_name] = initial_value

    def _determine_section_type(self):
        section = getattr(self.instance, 'section', None)
        if not section:
            section_id = self.data.get('section') or self.initial.get('section')
            if section_id:
                try:
                    section = Section.objects.get(pk=section_id)
                except Section.DoesNotExist:
                    section = None
        return section.section_type if section else 'default'

    def _build_dynamic_field(self, config):
        field_type = config.get('type', 'text')
        required = config.get('required', False)
        label = config.get('label', config['name'].replace('_', ' ').title())
        help_text = config.get('help_text', '')
        if field_type == 'text':
            return forms.CharField(required=required, label=label, help_text=help_text)
        if field_type == 'textarea':
            return forms.CharField(required=required, label=label, help_text=help_text, widget=forms.Textarea)
        if field_type == 'list':
            hint = help_text or 'Enter one item per line.'
            return forms.CharField(required=required, label=label, help_text=hint, widget=forms.Textarea)
        if field_type == 'boolean':
            return forms.BooleanField(required=False, label=label, help_text=help_text)
        return None

    def clean(self):
        cleaned_data = super().clean()
        payload = dict(self.instance.payload or {})
        for name in self.dynamic_field_names:
            value = cleaned_data.get(name)
            field_type = self.dynamic_field_configs[name].get('type', 'text')
            if field_type == 'list':
                value = [item.strip() for item in (value or '').splitlines() if item.strip()]
            if field_type == 'boolean':
                value = bool(value)
            if value in (None, '', []):
                payload.pop(name, None)
            else:
                payload[name] = value
        cleaned_data['_dynamic_payload'] = payload
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        dynamic_payload = self.cleaned_data.get('_dynamic_payload', {})
        instance.payload = dynamic_payload
        if commit:
            instance.save()
            self.save_m2m()
        return instance

class RotatingTextItemForm(forms.ModelForm):
    class Meta:
        model = RotatingTextItem
        fields = '__all__'
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add help text to indicate multilingual support
        self.fields['text'].help_text = "Text to rotate in the hero section. This field supports multiple languages."


class DropdownItemInline(SortableAdminMixin, admin.TabularInline):
    model = DropdownItem
    formset = SortableInlineFormSet
    sortable_field_name = "order"
    extra = 1

class RotatingTextItemInline(SortableAdminMixin, admin.TabularInline):
    model = RotatingTextItem
    form = RotatingTextItemForm
    formset = SortableInlineFormSet
    sortable_field_name = "order"
    extra = 1
    verbose_name = "Rotating Text Item"
    verbose_name_plural = "Rotating Text Items"

class HeroBackgroundImageInline(SortableAdminMixin, admin.TabularInline):
    model = HeroBackgroundImage
    formset = SortableInlineFormSet
    sortable_field_name = "order"
    extra = 1
    
    @admin.display(description="Preview")
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width:100px;height:60px;object-fit:cover;border-radius:4px;">',
                obj.image.url
            )
        return format_html('<span style="color:#999;">No image</span>')

@admin.register(SiteSettings)
class SiteSettingsAdmin(ModelAdmin, TabbedTranslationAdmin):
    formfield_overrides = {
        models.TextField: {'widget': CKEditor5Widget(config_name='default')},
    }
    list_display = ('site_name', 'logo_preview', 'favicon_preview', 'is_active_badge') 
    list_filter = ('is_active',)
    search_fields = ('site_name', 'logo_text')
    actions = ['delete_selected']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('site_name', 'is_active'),
            'classes': ('wide',),
        }),
        ('Branding', {
            'fields': ('logo_text', 'logo', 'favicon'),
            'classes': ('wide',),
            'description': 'Upload your site logo and favicon for branding consistency.',
        }),
        ('Header Styling', {
            'fields': ('header_bg_color', 'header_text_color'),
            'classes': ('wide',),
            'description': 'Customize the header background and text colors.',
        }),
    )
    
    @admin.display(description="Logo", ordering='logo')
    def logo_preview(self, obj):
        if obj.logo:
            return format_html(
                '<img src="{}" alt="Logo" style="width:40px;height:40px;border-radius:4px;object-fit:contain;">',
                obj.logo.url
            )
        return format_html('<span style="color:#999;">No logo</span>')
    
    @admin.display(description="Favicon", ordering='favicon')
    def favicon_preview(self, obj):
        if obj.favicon:
            return format_html(
                '<img src="{}" alt="Favicon" style="width:24px;height:24px;border-radius:2px;">',
                obj.favicon.url
            )
        return format_html('<span style="color:#999;">No favicon</span>')
    
    @admin.display(description="Status", boolean=True, ordering='is_active')
    def is_active_badge(self, obj):
        if obj.is_active:
            return format_html(
                '<span style="background-color:#10b981;color:white;padding:4px 8px;border-radius:4px;font-size:11px;font-weight:600;">ACTIVE</span>'
            )
        return format_html(
            '<span style="background-color:#ef4444;color:white;padding:4px 8px;border-radius:4px;font-size:11px;font-weight:600;">INACTIVE</span>'
        )

@admin.register(Section)
class SectionAdmin(SortableAdminMixin, ModelAdmin, TabbedTranslationAdmin):
    formfield_overrides = {
        models.TextField: {'widget': CKEditor5Widget(config_name='default')},
    }
    list_display = ('name', 'layout_badge', 'color_preview', 'grid_info', 'is_active_badge', 'order', 'view_count')
    list_filter = ('section_type', 'is_active', 'vertical_alignment', 'horizontal_alignment')
    search_fields = ('name', 'description')
    list_editable = ('order',)
    sortable_field_name = "order"
    actions = ['delete_selected', 'duplicate_section']
    
    fieldsets = (
        ('Section Information', {
            'fields': ('name', 'description', 'is_active', 'order'),
            'classes': ('wide',),
        }),
        ('Layout Settings', {
            'fields': ('section_type', 'rows', 'columns', 'card_gap'),
            'classes': ('wide',),
            'description': 'Configure how this section is displayed on the page.',
        }),
        ('Styling', {
            'fields': ('section_bg_color', 'section_text_color', 'title_font_size', 'vertical_alignment', 'horizontal_alignment'),
            'classes': ('wide',),
            'description': 'Customize the appearance of this section.',
        }),
        ('Call to Action', {
            'fields': ('cta_label', 'cta_url', 'cta_bg_color', 'cta_text_color', 'cta_target'),
            'classes': ('wide',),
            'description': 'Add a call-to-action button at the bottom of this section.',
        }),
        ('Analytics', {
            'fields': ('view_count', 'created_at', 'updated_at'),
            'classes': ('wide',),
            'description': 'Content performance tracking metrics.',
        }),
    )
    
    readonly_fields = ('view_count', 'created_at', 'updated_at')
    
    @admin.display(description="Layout", ordering='section_type')
    def layout_badge(self, obj):
        # Get choices directly from the field
        section_type_field = Section._meta.get_field('section_type')
        section_types = dict(section_type_field.choices)
        type_name = section_types.get(obj.section_type, obj.section_type)
        colors = {
            'default': '#6b7280',    # gray
            'hero': '#3b82f6',       # blue
            'stats': '#10b981',      # green
            'impact': '#8b5cf6',     # violet
            'testimonials': '#f59e0b', # amber
            'features': '#ec4899',   # pink
            'cta': '#ef4444',        # red
            'team': '#06b6d4',       # cyan
            'pricing': '#f97316',    # orange
            'faq': '#8b5cf6',        # violet
            'contact': '#10b981',    # green
        }
        color = colors.get(obj.section_type, '#6b7280')
        return format_html(
            '<span style="background-color:{};color:white;padding:4px 8px;border-radius:4px;font-size:11px;font-weight:600;">{}</span>',
            color, type_name
        )
    
    @admin.display(description="Colors", ordering='section_bg_color')
    def color_preview(self, obj):
        return format_html(
            '<div style="display:flex;align-items:center;gap:8px;">'
            '<div style="width:20px;height:20px;border-radius:4px;background-color:{};border:1px solid #ddd;"></div>'
            '<div style="width:20px;height:20px;border-radius:4px;background-color:{};border:1px solid #ddd;"></div>'
            '</div>',
            obj.section_bg_color, obj.section_text_color
        )
    
    @admin.display(description="Grid", ordering='columns')
    def grid_info(self, obj):
        return format_html(
            '<span style="background-color:#e5e7eb;color:#374151;padding:4px 8px;border-radius:4px;font-size:11px;font-weight:600;">{}×{}</span>',
            obj.rows, obj.columns
        )
    
    @admin.display(description="Status", boolean=True, ordering='is_active')
    def is_active_badge(self, obj):
        if obj.is_active:
            return format_html(
                '<span style="background-color:#10b981;color:white;padding:4px 8px;border-radius:4px;font-size:11px;font-weight:600;">ACTIVE</span>'
            )
        return format_html(
            '<span style="background-color:#ef4444;color:white;padding:4px 8px;border-radius:4px;font-size:11px;font-weight:600;">INACTIVE</span>'
        )
    
    @admin.action(description="Duplicate selected sections")
    def duplicate_section(self, request, queryset):
        """Duplicate sections with all their card blocks"""
        for section in queryset:
            # Create a copy of the section
            section_copy = Section(
                name=f"{section.name} (Copy)",
                description=section.description,
                rows=section.rows,
                columns=section.columns,
                card_gap=section.card_gap,
                vertical_alignment=section.vertical_alignment,
                horizontal_alignment=section.horizontal_alignment,
                section_bg_color=section.section_bg_color,
                section_text_color=section.section_text_color,
                title_font_size=section.title_font_size,
                section_type=section.section_type,
                cta_label=section.cta_label,
                cta_url=section.cta_url,
                cta_bg_color=section.cta_bg_color,
                cta_text_color=section.cta_text_color,
                cta_target=section.cta_target,
                order=section.order + 1000,  # Place after original
                is_active=False  # Start as inactive
            )
            section_copy.save()
            
            # Duplicate all card blocks
            for card_block in section.card_block.all():
                card_block_copy = CardBlock(
                    section=section_copy,
                    title=card_block.title,
                    text=card_block.text,
                    icon=card_block.icon,
                    icon_size=card_block.icon_size,
                    icon_color=card_block.icon_color,
                    card_bg_color=card_block.card_bg_color,
                    card_text_color=card_block.card_text_color,
                    icon_layout=card_block.icon_layout,
                    image=card_block.image,
                    image_alt=card_block.image_alt,
                    video_file=card_block.video_file,
                    video_thumbnail=card_block.video_thumbnail,
                    video_url=card_block.video_url,
                    cta_label=card_block.cta_label,
                    cta_url=card_block.cta_url,
                    button_color=card_block.button_color,
                    button_text_color=card_block.button_text_color,
                    button_target=card_block.button_target,
                    payload=card_block.payload,
                    order=card_block.order,
                    is_active=card_block.is_active
                )
                card_block_copy.save()
                
        self.message_user(request, f"Successfully duplicated {queryset.count()} section(s).")

@admin.register(NavigationItem)
class NavigationItemAdmin(SortableAdminMixin, ModelAdmin, TabbedTranslationAdmin):
    formfield_overrides = {
        models.TextField: {'widget': CKEditor5Widget(config_name='default')},
    }
    list_display = ('label', 'url', 'is_active', 'is_dropdown', 'is_button', 'order', 'is_active_badge', 'click_count')
    list_filter = ('is_dropdown', 'is_button')
    search_fields = ('label', 'url')
    list_editable = ('order',)
    sortable_field_name = "order"
    actions = ['delete_selected']
    
    fieldsets = (
        ('Navigation Item', {
            'fields': ('label', 'url', 'description', 'is_active', 'order'),
            'classes': ('wide',),
        }),
        ('Dropdown Settings', {
            'fields': ('is_dropdown',),
            'classes': ('wide',),
            'description': 'Enable this to create a dropdown menu.',
        }),
        ('Button Settings', {
            'fields': ('is_button', 'button_color', 'button_text_color'),
            'classes': ('wide',),
            'description': 'Configure this navigation item as a button.',
        }),
        ('Analytics', {
            'fields': ('click_count', 'created_at', 'updated_at'),
            'classes': ('wide',),
            'description': 'Content performance tracking metrics.',
        }),
    )
    
    readonly_fields = ('click_count', 'created_at', 'updated_at')
    
    inlines = [DropdownItemInline]
    
    @admin.display(description="Status", boolean=True, ordering='is_active')
    def is_active_badge(self, obj):
        if obj.is_active:
            return format_html(
                '<span style="background-color:#10b981;color:white;padding:4px 8px;border-radius:4px;font-size:11px;font-weight:600;">ACTIVE</span>'
            )
        return format_html(
            '<span style="background-color:#ef4444;color:white;padding:4px 8px;border-radius:4px;font-size:11px;font-weight:600;">INACTIVE</span>'
        )

@admin.register(Hero)
class HeroAdmin(SortableAdminMixin, ModelAdmin, TabbedTranslationAdmin):
    formfield_overrides = {
        models.TextField: {'widget': CKEditor5Widget(config_name='default')},
    }
    list_display = ('title', 'layout_type', 'is_active_badge', 'order', 'view_count', 'cta_click_count')
    list_filter = ('layout_type', 'is_active')
    search_fields = ('title',)
    list_editable = ('order',)
    sortable_field_name = "order"
    actions = ['delete_selected']
    
    fieldsets = (
        ('Hero Content', {
            'fields': ('title', 'subtitle_description', 'is_active', 'order'),
            'classes': ('wide',),
        }),
        ('Call to Action', {
            'fields': ('cta_text', 'cta_link', 'cta_bg_color'),
            'classes': ('wide',),
        }),
        ('Layout', {
            'fields': ('layout_type',),
            'classes': ('wide',),
        }),
        ('Animation Timing', {
            'fields': ('rotating_text_settimeout', 'image_settimeout'),
            'classes': ('wide',),
            'description': 'Timing settings for text and image rotation (in milliseconds).',
        }),
        ('Styling', {
            'fields': ('bg_color',),
            'classes': ('wide',),
        }),
        ('Analytics', {
            'fields': ('view_count', 'cta_click_count', 'created_at', 'updated_at'),
            'classes': ('wide',),
            'description': 'Content performance tracking metrics.',
        }),
    )
    
    readonly_fields = ('view_count', 'cta_click_count', 'created_at', 'updated_at')
    inlines = [RotatingTextItemInline, HeroBackgroundImageInline]
    
    @admin.display(description="Layout", ordering='layout_type')
    def layout_type(self, obj):
        # Get choices directly from the field
        layout_type_field = Hero._meta.get_field('layout_type')
        layout_types = dict(layout_type_field.choices)
        type_name = layout_types.get(obj.layout_type, obj.layout_type)
        return format_html(
            '<span style="background-color:#3b82f6;color:white;padding:4px 8px;border-radius:4px;font-size:11px;font-weight:600;">{}</span>',
            type_name
        )
    
    @admin.display(description="Status", boolean=True, ordering='is_active')
    def is_active_badge(self, obj):
        if obj.is_active:
            return format_html(
                '<span style="background-color:#10b981;color:white;padding:4px 8px;border-radius:4px;font-size:11px;font-weight:600;">ACTIVE</span>'
            )
        return format_html(
            '<span style="background-color:#ef4444;color:white;padding:4px 8px;border-radius:4px;font-size:11px;font-weight:600;">INACTIVE</span>'
        )

@admin.register(Footer)
class FooterAdmin(ModelAdmin, TabbedTranslationAdmin):
    formfield_overrides = {
        models.TextField: {'widget': CKEditor5Widget(config_name='default')},
    }
    list_display = ('__str__', 'is_active_badge')
    list_filter = ('is_active',)
    actions = ['delete_selected']
    
    fieldsets = (
        ('Footer Content', {
            'fields': ('description', 'address', 'phone', 'email', 'opening_hours'),
            'classes': ('wide',),
            'description': 'Main content for the website footer.',
        }),
        ('Social Media Links', {
            'fields': ('facebook_url', 'twitter_url', 'instagram_url', 'linkedin_url'),
            'classes': ('wide',),
            'description': 'Links to your social media profiles.',
        }),
        ('Settings', {
            'fields': ('is_active',),
            'classes': ('wide',),
        }),
    )
    
    @admin.display(description="Status", boolean=True, ordering='is_active')
    def is_active_badge(self, obj):
        if obj.is_active:
            return format_html(
                '<span style="background-color:#10b981;color:white;padding:4px 8px;border-radius:4px;font-size:11px;font-weight:600;">ACTIVE</span>'
            )
        return format_html(
            '<span style="background-color:#ef4444;color:white;padding:4px 8px;border-radius:4px;font-size:11px;font-weight:600;">INACTIVE</span>'
        )

# Register CardBlock separately in admin
@admin.register(CardBlock)
class CardBlockAdmin(SortableAdminMixin, ModelAdmin, TabbedTranslationAdmin):
    form = CardBlockAdminForm
    formfield_overrides = {
        models.TextField: {'widget': CKEditor5Widget(config_name='default')},
    }
    list_display = ('title', 'section', 'order', 'is_active_badge', 'click_count')
    list_filter = ('section', 'is_active')
    search_fields = ('title', 'text')
    list_editable = ('order',)
    sortable_field_name = "order"
    actions = ['delete_selected']
    
    fieldsets = (
        ('Card Information', {
            'fields': ('section', 'title', 'text', 'is_active', 'order'),
            'classes': ('wide',),
        }),
        ('Icon Settings', {
            'fields': ('icon', 'icon_size', 'icon_color', 'icon_layout'),
            'classes': ('wide',),
        }),
        ('Media', {
            'fields': ('image', 'image_alt', 'video_file', 'video_thumbnail', 'video_url'),
            'classes': ('wide',),
        }),
        ('Button Settings', {
            'fields': ('cta_label', 'cta_url', 'button_color', 'button_text_color', 'button_target'),
            'classes': ('wide',),
        }),
        ('Styling', {
            'fields': ('card_bg_color', 'card_text_color'),
            'classes': ('wide',),
        }),
        ('Analytics', {
            'fields': ('click_count', 'created_at', 'updated_at'),
            'classes': ('wide',),
            'description': 'Content performance tracking metrics.',
        }),
    )
    
    readonly_fields = ('click_count', 'created_at', 'updated_at')
    
    class Media:
        js = ('admin/js/card_block_dynamic_fields.js',)
    
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        # Store section type in form for JavaScript access
        if obj and obj.section:
            form.section_type = obj.section.section_type
        elif request.method == 'GET' and 'section' in request.GET:
            try:
                section = Section.objects.get(pk=request.GET['section'])
                form.section_type = section.section_type
            except Section.DoesNotExist:
                form.section_type = 'default'
        else:
            form.section_type = 'default'
        return form
    
    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        extra_context = extra_context or {}
        # Add all sections with their types for the select dropdown (as JSON string)
        import json
        sections = Section.objects.all().values('id', 'section_type', 'name')
        extra_context['sections_data'] = json.dumps(list(sections))
        return super().changeform_view(request, object_id, form_url, extra_context)
    
    @admin.display(description="Status", boolean=True, ordering='is_active')
    def is_active_badge(self, obj):
        if obj.is_active:
            return format_html(
                '<span style="background-color:#10b981;color:white;padding:4px 8px;border-radius:4px;font-size:11px;font-weight:600;">ACTIVE</span>'
            )
        return format_html(
            '<span style="background-color:#ef4444;color:white;padding:4px 8px;border-radius:4px;font-size:11px;font-weight:600;">INACTIVE</span>'
        )
