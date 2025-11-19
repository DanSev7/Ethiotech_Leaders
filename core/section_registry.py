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
        'description': 'A flexible grid layout for displaying content cards'
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
        'description': 'A section for showcasing team members'
    },
    'pricing': {
        'name': 'Pricing Plans',
        'template': 'sections/pricing.html',
        'required_fields': [],
        'optional_fields': ['cta_label', 'cta_url', 'cta_bg_color', 'cta_text_color', 'cta_target'],
        'description': 'A section for displaying pricing plans'
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