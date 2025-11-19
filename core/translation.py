from modeltranslation.translator import TranslationOptions, translator
from .models import (
    SiteSettings, 
    NavigationItem, 
    Section, 
    CardBlock, 
    Hero, 
    HeroBackgroundImage, 
    RotatingTextItem,
    Footer
)

class SiteSettingsTranslationOptions(TranslationOptions):
    fields = ('site_name', 'logo_text')


class FooterTranslationOptions(TranslationOptions):
    fields = ('description', 'address')

class NavigationItemTranslationOptions(TranslationOptions):
    fields = ('label','description')

class SectionTranslationOptions(TranslationOptions):
    fields = (
        'name', 
        'description',
        'title_font_size',
        'cta_label'
    )

class CardBlockTranslationOptions(TranslationOptions):
    fields = (
        'title', 
        'text',
        'cta_label',
        'cta_url'
    )

class HeroTranslationOptions(TranslationOptions):
    fields = (
        'title', 
        'subtitle_description',
        'cta_text'
    )

class HeroBackgroundImageTranslationOptions(TranslationOptions):
    fields = ()

class RotatingTextItemTranslationOptions(TranslationOptions):
    fields = ('text',)

# Register the models for translation
translator.register(SiteSettings, SiteSettingsTranslationOptions)
translator.register(Footer, FooterTranslationOptions)
translator.register(NavigationItem, NavigationItemTranslationOptions)
translator.register(Section, SectionTranslationOptions)
translator.register(CardBlock, CardBlockTranslationOptions)
translator.register(Hero, HeroTranslationOptions)
translator.register(HeroBackgroundImage, HeroBackgroundImageTranslationOptions)
translator.register(RotatingTextItem, RotatingTextItemTranslationOptions)