# core/models.py
from django.db import models
from django.core.validators import RegexValidator
from django_ckeditor_5.fields import CKEditor5Field
from django.db import models as django_models
from colorfield.fields import ColorField


ICON_NAME_VALIDATOR = RegexValidator(
    r'^[a-z0-9-]+$', 
    'Enter a valid Lucide icon name (e.g. rocket-launch, heart-pulse).'
)

class SiteSettings(models.Model):
    site_name = models.CharField(max_length=100, default="Ethiotech Leader")
    logo_text = models.CharField(max_length=50, blank=True, help_text="e.g., [Logo] or leave blank")
    logo = models.ImageField(upload_to='logos/', blank=True, null=True, help_text="Upload your logo image")
    favicon = models.ImageField(upload_to='favicon/', blank=True, null=True)
    header_bg_color = ColorField(default="#ffffff", help_text="Header background color")
    header_text_color = ColorField(default="#000000", help_text="Header text color")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.site_name)

    class Meta:
        verbose_name = "Site Settings"

class NavigationItem(models.Model):
    label = models.CharField(max_length=100)
    url = models.CharField(max_length=200, blank=True)
    description = django_models.TextField(blank=True, help_text="Description of the navigation item")
    is_active = models.BooleanField(default=True)
    is_dropdown = models.BooleanField(default=False)
    is_button = models.BooleanField(default=False)
    button_color = ColorField(default="#3b82f6")
    button_text_color = ColorField(default="#ffffff")
    order = models.PositiveIntegerField(default=0)
    # Content tracking fields
    click_count = models.PositiveIntegerField(default=0, help_text="Number of times this navigation item has been clicked")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return str(self.label)

    def get_preview_data(self):
        """Return data needed for admin preview"""
        return {
            'label': self.label,
            'url': self.url,
            'is_active': self.is_active,
            'is_dropdown': self.is_dropdown,
            'is_button': self.is_button,
            'click_count': self.click_count
        }

    def increment_click_count(self):
        """Increment the click count for this navigation item"""
        self.click_count += 1
        self.save(update_fields=['click_count'])

class DropdownItem(models.Model):
    parent = models.ForeignKey(NavigationItem, related_name='dropdown_items', on_delete=models.CASCADE)
    label = models.CharField(max_length=100)
    url = models.CharField(max_length=200)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return str(self.label)

class Section(models.Model):
    """Content section within a business website."""
    # site_settings = models.ForeignKey(
    #     SiteSettings,
    #     on_delete=models.CASCADE,
    #     related_name='sections',
    #     help_text="Site settings this section belongs to"
    # )
    name = models.CharField(
        max_length=100,
        help_text="Descriptive name for this content section"
    )
    description = django_models.TextField(blank=True, help_text="Description of this content section")
    rows = models.PositiveIntegerField(default=1)
    columns = models.PositiveIntegerField(default=3)
    card_gap = models.CharField(max_length=20, default="1.5rem")
    vertical_alignment = models.CharField(max_length=20, choices=[
        ('start', 'Top'), ('center', 'Center'), ('end', 'Bottom')
    ], default='start')
    horizontal_alignment = models.CharField(max_length=20, choices=[
        ('start', 'Left'), ('center', 'Center'), ('end', 'Right')
    ], default='center')
    section_bg_color = ColorField(default="#ffffff")
    section_text_color = ColorField(default="#000000")
    title_font_size = models.CharField(
        max_length=20,
        default="2xl",
        help_text="Title font size (e.g., sm, md, lg, xl, 2xl, 3xl, 4xl,6xl)"
    )
    section_type = models.CharField(
        max_length=50,
        choices=[
            ('default', 'Default Grid'),
            ('hero', 'Hero Section'),
            ('stats', 'Statistics'),
            ('impact', 'Impact'),
            ('testimonials', 'Testimonials'),
            ('features', 'Features'),
            ('cta', 'Call to Action'),
            ('team', 'Team Members'),
            ('pricing', 'Pricing Plans'),
            ('faq', 'Frequently Asked Questions'),
            ('contact', 'Contact Form'),
        ],
        default='default',
        help_text="Predefined section template type"
    )
    cta_label = models.CharField(max_length=100, blank=True, help_text="Text for the section CTA")
    cta_url = models.URLField(blank=True, help_text="URL for the section CTA")
    cta_bg_color = ColorField(default="#3b82f6", help_text="CTA background color", blank=True)
    cta_text_color = ColorField(default="#ffffff", help_text="CTA text color", blank=True)
    cta_target = models.CharField(max_length=10, choices=[
        ('_self', 'Same Tab'), ('_blank', 'New Tab')
    ], default='_self', blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    # Content tracking fields
    view_count = models.PositiveIntegerField(default=0, help_text="Number of times this section has been viewed")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Section"
        verbose_name_plural = "Sections"
        ordering = ['order']

    def __str__(self):
        return self.name

    def get_preview_data(self):
        """Return data needed for admin preview"""
        return {
            'title': self.name,
            'type': self.get_section_type_display(),
            'is_active': self.is_active,
            'card_count': self.card_block.count(),
            'view_count': self.view_count
        }

    def increment_view_count(self):
        """Increment the view count for this section"""
        self.view_count += 1
        self.save(update_fields=['view_count'])

class CardBlock(models.Model):
    """Individual content card within a section."""
    section = models.ForeignKey(Section, related_name='card_block', on_delete=models.CASCADE)

    title = models.CharField(
        max_length=200,
        help_text="Card title displayed prominently"
    )
    text = django_models.TextField(
        blank=True, 
        help_text="Rich text content for the card"
    )
    icon = models.CharField(
        max_length=60,
        # validators=[ICON_NAME_VALIDATOR],
        help_text="Lucide icon name (e.g. rocket-launch)",
        blank=True
    )
    icon_size = models.PositiveIntegerField(
        default=32, 
        help_text="Icon size in pixels",
        blank=True
    )
    icon_color = ColorField(
        default="#3b82f6", 
        help_text="Icon color in HEX format",
        blank=True
    )
    card_bg_color = ColorField(
        default="#ffffff",
        help_text="Card background color",
        blank=True
    )
    card_text_color = ColorField(
        default="#000000",
        help_text="Card text color",
        blank=True
    )
    icon_layout = models.CharField(
        max_length=20,
        choices=[
            ('side-by-side', 'Side by Side (Icon Left, Title Right)'),
            ('top-down', 'Top Down (Icon Top, Title Bottom)'),
            ('top-down-center', 'Top Down (Icon Center, Title Center)'),
        ],
        default='top-down',
        help_text="How icon and title are displayed"
    )
    image = models.ImageField(upload_to='cards/', blank=True, null=True)
    image_alt = models.CharField(max_length=200, blank=True)
    video_file = models.FileField(upload_to='videos/', blank=True, null=True)
    video_thumbnail = models.ImageField(upload_to='video_thumbnails/', blank=True, null=True)
    video_url = models.URLField(blank=True)
    cta_label = models.CharField(max_length=100, blank=True, help_text="Call-to-Action label text")
    cta_url = models.URLField(blank=True, help_text="Call-to-Action URL link")
    button_color = ColorField(
        default="#3b82f6", 
        help_text="Button color in HEX format",
        blank=True
    )
    button_text_color = ColorField(
        default="#ffffff", 
        help_text="Button text color in HEX format",
        blank=True
    )
    button_target = models.CharField(max_length=10, choices=[
        ('_self', 'Same Tab'), ('_blank', 'New Tab')
    ], default='_self', blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    payload = models.JSONField(default=dict, blank=True, help_text="Type-specific data for dynamic card layouts")
    # Content tracking fields
    click_count = models.PositiveIntegerField(default=0, help_text="Number of times CTA link has been clicked")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Card Block"
        verbose_name_plural = "Card Blocks"
        ordering = ['order']

    def __str__(self):
        return self.title

    def get_preview_data(self):
        """Return data needed for admin preview"""
        return {
            'title': self.title,
            'has_image': bool(self.image),
            'has_video': bool(self.video_file or self.video_url),
            'has_cta': bool(self.cta_label and self.cta_url),
            'click_count': self.click_count,
            'payload_keys': list((self.payload or {}).keys()),
        }

    def increment_click_count(self):
        """Increment the click count for this card's CTA"""
        self.click_count += 1
        self.save(update_fields=['click_count'])

    def get_payload_value(self, key, default=None):
        if not self.payload:
            return default
        return self.payload.get(key, default)

    def get_payload_list(self, key):
        value = self.get_payload_value(key, [])
        if isinstance(value, str):
            value = [item.strip() for item in value.splitlines() if item.strip()]
        return value or []

    def has_type_specific_data(self):
        return bool(self.payload)

class Hero(models.Model):
    """Hero section with rotating text and background images."""
    title = models.CharField(
        max_length=200,
        help_text="Main heading. Plain text (no rich text editor)."
    )
    subtitle_description = django_models.TextField(
        blank=True,
        help_text="Supporting text. Rich text editor enabled."
    )
    cta_text = models.CharField(
        max_length=100,
        blank=True,
        help_text="Call-to-Action button text"
    )
    cta_link = models.URLField(
        blank=True,
        help_text="Call-to-Action button URL"
    )
    cta_bg_color = ColorField(
        default="#3b82f6",
        help_text="Button background color"
    )
    layout_type = models.CharField(
        max_length=50,
        choices=[
            ('text-left-image-right', 'Text Left / Image Right'),
            ('text-right-image-left', 'Text Right / Image Left'),
            ('text-center-image-background', 'Text Center / Image Background'),
            ('text-center-no-image', 'Text Center / No Image'),
        ],
        default='text-center-image-background',
        help_text="Descriptive layout type"
    )
    rotating_text_settimeout = models.PositiveIntegerField(
        default=3000,
        help_text="Delay (ms) for text rotation"
    )
    image_settimeout = models.PositiveIntegerField(
        default=5000,
        help_text="Delay (ms) for background image rotation"
    )
    bg_color = ColorField(
        default="#ffffff",
        help_text="Background color for the Hero section"
    )
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    # Content tracking fields
    view_count = models.PositiveIntegerField(default=0, help_text="Number of times this hero section has been viewed")
    cta_click_count = models.PositiveIntegerField(default=0, help_text="Number of times CTA button has been clicked")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Hero Section"
        verbose_name_plural = "Hero Sections"
        ordering = ['order']

    def __str__(self):
        return self.title or "Hero Section"

    def get_preview_data(self):
        """Return data needed for admin preview"""
        return {
            'title': self.title,
            'layout_type': self.get_layout_type_display(),
            'is_active': self.is_active,
            'rotating_text_count': self.rotating_texts.count(),
            'background_image_count': self.background_images.count(),
            'view_count': self.view_count,
            'cta_click_count': self.cta_click_count
        }

    def increment_view_count(self):
        """Increment the view count for this hero section"""
        self.view_count += 1
        self.save(update_fields=['view_count'])

    def increment_cta_click_count(self):
        """Increment the CTA click count for this hero section"""
        self.cta_click_count += 1
        self.save(update_fields=['cta_click_count'])

class RotatingTextItem(models.Model):
    """Individual text string to be rotated in the Hero section."""
    hero = models.ForeignKey(
        Hero,
        related_name='rotating_texts',
        on_delete=models.CASCADE,
        help_text="Parent Hero section"
    )
    text = models.CharField(
        max_length=200,
        help_text="The individual text string to be rotated"
    )
    order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "Rotating Text Item"
        verbose_name_plural = "Rotating Text Items"
        ordering = ['order']

    def __str__(self):
        return self.text

class HeroBackgroundImage(models.Model):
    """Background image for the Hero section slider."""
    hero = models.ForeignKey(
        Hero,
        related_name='background_images',
        on_delete=models.CASCADE,
        help_text="Parent Hero section"
    )
    image = models.ImageField(
        upload_to='hero_backgrounds/',
        help_text="Image file for the background slider"
    )
    order = models.PositiveIntegerField(
        default=0,
        help_text="Used for sorting the slide rotation"
    )

    class Meta:
        verbose_name = "Hero Background Image"
        verbose_name_plural = "Hero Background Images"
        ordering = ['order']

    def __str__(self):
        return f"Background Image {self.order} for {self.hero.title}"


class Footer(models.Model):
    """Footer content for the website"""
    description = models.TextField(blank=True, help_text="Site description for footer")
    address = models.CharField(max_length=200, blank=True, help_text="Company address")
    phone = models.CharField(max_length=20, blank=True, help_text="Contact phone number")
    email = models.EmailField(blank=True, help_text="Contact email")
    opening_hours = models.TextField(blank=True, help_text="Opening hours (use line breaks for multiple lines)")
    facebook_url = models.URLField(blank=True, help_text="Facebook page URL")
    twitter_url = models.URLField(blank=True, help_text="Twitter profile URL")
    instagram_url = models.URLField(blank=True, help_text="Instagram profile URL")
    linkedin_url = models.URLField(blank=True, help_text="LinkedIn profile URL")
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Footer"
        verbose_name_plural = "Footer"
    
    def __str__(self):
        site_settings = SiteSettings.objects.filter(is_active=True).first()
        site_name = site_settings.site_name if site_settings else "Website"
        return f"Footer for {site_name}"
