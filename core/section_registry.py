"""
Section Type Registry for EthioSites CMS
This module defines all available section types and their properties.
"""

SECTION_TYPES = {
    'default': {
        'name': 'Default Grid',
        'template': 'sections/default.html',
        'required_fields': ['rows', 'columns'],
        'optional_fields': ['cta_label', 'cta_url', 'cta_bg_color', 'cta_text_color', 'cta_target'],
        'description': 'A flexible grid layout for displaying content cards',
        'card_schema': 'default',
    },
    'hero': {
        'name': 'Hero Section',
        'template': 'sections/hero.html',
        'required_fields': ['title'],
        'optional_fields': ['subtitle_description', 'cta_text', 'cta_link', 'cta_bg_color', 
                           'layout_type', 'rotating_text_settimeout', 'image_settimeout', 'bg_color'],
        'description': 'A prominent hero section with rotating text and background images'
    },
    'stats': {
        'name': 'Statistics',
        'template': 'sections/stats.html',
        'required_fields': [],
        'optional_fields': ['cta_label', 'cta_url', 'cta_bg_color', 'cta_text_color', 'cta_target'],
        'description': 'A section for displaying key statistics and metrics'
    },
    'impact': {
        'name': 'Impact',
        'template': 'sections/impact.html',
        'required_fields': [],
        'optional_fields': ['cta_label', 'cta_url', 'cta_bg_color', 'cta_text_color', 'cta_target'],
        'description': 'A section for showcasing impact and achievements'
    },
    'testimonials': {
        'name': 'Testimonials',
        'template': 'sections/testimonials.html',
        'required_fields': [],
        'optional_fields': ['cta_label', 'cta_url', 'cta_bg_color', 'cta_text_color', 'cta_target'],
        'description': 'A section for displaying customer testimonials'
    },
    'features': {
        'name': 'Features',
        'template': 'sections/features.html',
        'required_fields': [],
        'optional_fields': ['cta_label', 'cta_url', 'cta_bg_color', 'cta_text_color', 'cta_target'],
        'description': 'A section for highlighting product or service features'
    },
    'cta': {
        'name': 'Call to Action',
        'template': 'sections/cta.html',
        'required_fields': [],
        'optional_fields': ['cta_label', 'cta_url', 'cta_bg_color', 'cta_text_color', 'cta_target'],
        'description': 'A prominent call-to-action section'
    },
    'team': {
        'name': 'Team Members',
        'template': 'sections/team.html',
        'required_fields': [],
        'optional_fields': ['cta_label', 'cta_url', 'cta_bg_color', 'cta_text_color', 'cta_target'],
        'description': 'A section for showcasing team members',
        'card_schema': 'team',
    },
    'pricing': {
        'name': 'Pricing Plans',
        'template': 'sections/pricing.html',
        'required_fields': [],
        'optional_fields': ['cta_label', 'cta_url', 'cta_bg_color', 'cta_text_color', 'cta_target'],
        'description': 'A section for displaying pricing plans',
        'card_schema': 'pricing',
    },
    'faq': {
        'name': 'Frequently Asked Questions',
        'template': 'sections/faq.html',
        'required_fields': [],
        'optional_fields': ['cta_label', 'cta_url', 'cta_bg_color', 'cta_text_color', 'cta_target'],
        'description': 'A section for answering frequently asked questions'
    },
    'contact': {
        'name': 'Contact Form',
        'template': 'sections/contact.html',
        'required_fields': [],
        'optional_fields': ['cta_label', 'cta_url', 'cta_bg_color', 'cta_text_color', 'cta_target'],
        'description': 'A section with a contact form and information'
    }
}

# Helper functions
def get_section_type_info(section_type):
    """Get information about a specific section type"""
    return SECTION_TYPES.get(section_type, None)

def get_all_section_types():
    """Get all available section types"""
    return SECTION_TYPES

def get_section_template(section_type):
    """Get the template path for a section type"""
    section_info = SECTION_TYPES.get(section_type)
    return section_info['template'] if section_info else 'sections/default.html'

def is_valid_section_type(section_type):
    """Check if a section type is valid"""
    return section_type in SECTION_TYPES

# Card field visibility and mapping rules per section type
CARD_FIELD_RULES = {
    'team': {
        'visible_fields': ['section', 'title', 'image', 'image_alt', 'cta_label', 'text', 'cta_url', 'button_target', 'card_bg_color', 'card_text_color', 'is_active', 'order'],
        'hidden_fields': ['icon', 'icon_size', 'icon_color', 'icon_layout', 'video_file', 'video_thumbnail', 'video_url', 'button_color', 'button_text_color'],
        'field_mappings': {
            'title': {'label': 'Name', 'help_text': 'Team member full name'},
            'cta_label': {'label': 'Position / Role', 'help_text': 'Job title or role (e.g., "Lead Designer", "CEO")'},
            'text': {'label': 'Bio', 'help_text': 'Short biography or description'},
            'cta_url': {'label': 'Social Link / Profile URL', 'help_text': 'Link to LinkedIn, Twitter, or personal website'},
            'image': {'help_text': 'Team member photo (recommended: square, 400x400px)'},
        },
        'required_fields': ['title', 'image'],
    },
    'pricing': {
        'visible_fields': ['section', 'title', 'cta_label', 'text', 'cta_url', 'button_color', 'button_text_color', 'button_target', 'card_bg_color', 'card_text_color', 'is_active', 'order'],
        'hidden_fields': ['icon', 'icon_size', 'icon_color', 'icon_layout', 'image', 'image_alt', 'video_file', 'video_thumbnail', 'video_url'],
        'field_mappings': {
            'title': {'label': 'Plan Name', 'help_text': 'Name of the pricing tier (e.g., "Starter", "Professional")'},
            'cta_label': {'label': 'Price / Month', 'help_text': 'Price displayed on button (e.g., "$49/mo", "Free")'},
            'text': {'label': 'Features List', 'help_text': 'List of features (one per line or use bullet points)'},
            'cta_url': {'label': 'Buy / Sign Up Link', 'help_text': 'URL to purchase or sign up for this plan'},
        },
        'required_fields': ['title', 'cta_label'],
    },
    'faq': {
        'visible_fields': ['section', 'title', 'text', 'card_bg_color', 'card_text_color', 'is_active', 'order'],
        'hidden_fields': ['icon', 'icon_size', 'icon_color', 'icon_layout', 'image', 'image_alt', 'video_file', 'video_thumbnail', 'video_url', 'cta_label', 'cta_url', 'button_color', 'button_text_color', 'button_target'],
        'field_mappings': {
            'title': {'label': 'Question', 'help_text': 'The frequently asked question'},
            'text': {'label': 'Answer', 'help_text': 'The answer to the question'},
        },
        'required_fields': ['title', 'text'],
    },
    'default': {
        'visible_fields': ['section', 'title', 'text', 'icon', 'icon_size', 'icon_color', 'icon_layout', 'image', 'image_alt', 'video_file', 'video_thumbnail', 'video_url', 'cta_label', 'cta_url', 'button_color', 'button_text_color', 'button_target', 'card_bg_color', 'card_text_color', 'is_active', 'order'],
        'hidden_fields': [],
        'field_mappings': {},
        'required_fields': ['title'],
    },
}

CARD_SCHEMAS = {
    'default': {
        'label': 'Default Card Enhancements',
        'description': 'Optional badge and supporting text shared across all layouts.',
        'fields': [
            {
                'name': 'badge_text',
                'type': 'text',
                'label': 'Badge Text',
                'help_text': 'Short label displayed above the title (e.g., "New").',
            },
            {
                'name': 'supporting_text',
                'type': 'textarea',
                'label': 'Supporting Text',
                'help_text': 'Additional paragraph displayed under the main content.',
            },
        ],
    },
    'team': {
        'label': 'Team Member Details',
        'description': 'Additional fields tailored for team profiles.',
        'fields': [
            {
                'name': 'role',
                'type': 'text',
                'label': 'Role / Position',
                'help_text': 'Displayed beneath the name (e.g., "Lead Designer").',
            },
            {
                'name': 'highlight',
                'type': 'text',
                'label': 'Highlight',
                'help_text': 'One line quote or specialty.',
            },
            {
                'name': 'primary_link_label',
                'type': 'text',
                'label': 'Primary Link Label',
                'help_text': 'Label for the main profile/social link.',
            },
            {
                'name': 'primary_link_url',
                'type': 'text',
                'label': 'Primary Link URL',
                'help_text': 'URL for the main profile/social link.',
            },
            {
                'name': 'secondary_link_label',
                'type': 'text',
                'label': 'Secondary Link Label',
                'help_text': 'Optional second link label.',
            },
            {
                'name': 'secondary_link_url',
                'type': 'text',
                'label': 'Secondary Link URL',
                'help_text': 'Optional second link URL.',
            },
        ],
    },
    'pricing': {
        'label': 'Pricing Plan Details',
        'description': 'Structured fields for pricing tiers.',
        'fields': [
            {
                'name': 'price_amount',
                'type': 'text',
                'label': 'Price Amount',
                'help_text': 'Displayed prominently (e.g., "$49").',
            },
            {
                'name': 'price_interval',
                'type': 'text',
                'label': 'Billing Interval',
                'help_text': 'e.g., "per month".',
            },
            {
                'name': 'price_subtitle',
                'type': 'text',
                'label': 'Price Subtitle',
                'help_text': 'Short supporting line beneath the price.',
            },
            {
                'name': 'feature_list',
                'type': 'list',
                'label': 'Feature List',
                'help_text': 'Enter one feature per line.',
            },
            {
                'name': 'is_featured',
                'type': 'boolean',
                'label': 'Highlight Plan',
                'help_text': 'Marks this tier as emphasized.',
            },
        ],
    },
}


def get_card_schema(section_type):
    schema_key = SECTION_TYPES.get(section_type, {}).get('card_schema', 'default')
    return CARD_SCHEMAS.get(schema_key, CARD_SCHEMAS['default'])

def get_card_field_rules(section_type):
    """Get field visibility and mapping rules for a section type"""
    return CARD_FIELD_RULES.get(section_type, CARD_FIELD_RULES['default'])

def get_visible_fields_for_section_type(section_type):
    """Get list of visible fields for a section type"""
    rules = get_card_field_rules(section_type)
    return rules.get('visible_fields', [])

def get_hidden_fields_for_section_type(section_type):
    """Get list of hidden fields for a section type"""
    rules = get_card_field_rules(section_type)
    return rules.get('hidden_fields', [])

def get_field_mapping_for_section_type(section_type, field_name):
    """Get label and help_text mapping for a field in a section type"""
    rules = get_card_field_rules(section_type)
    mappings = rules.get('field_mappings', {})
    return mappings.get(field_name, {})