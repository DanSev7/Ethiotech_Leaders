# core/views.py
from django.shortcuts import render, get_object_or_404
from django.utils import translation
from django.conf import settings
from django.http import JsonResponse
from .models import SiteSettings, Hero, Section, NavigationItem, Footer, CardBlock

def home(request):
    # Handle language switching
    lang = request.GET.get('lang')
    if lang and lang in ['en', 'am']:
        translation.activate(lang)
        request.session['_language'] = lang
    
    settings = get_object_or_404(SiteSettings, is_active=True)
    request.site_settings = settings          # attach for templates

    hero = Hero.objects.filter(is_active=True).order_by('order').first()
    sections = Section.objects.filter(is_active=True).order_by('order')
    nav = NavigationItem.objects.prefetch_related('dropdown_items').order_by('order')
    footer = Footer.objects.filter(is_active=True).first()
    
    # Increment view count for hero section
    if hero:
        hero.increment_view_count()
    
    # Increment view count for all sections
    for section in sections:
        section.increment_view_count()

    return render(request, 'index.html', {
        'site_settings': settings,
        'hero': hero,
        'sections': sections,
        'navigation_items': nav,
        'footer': footer,
    })

def navigation_page(request, nav_id):
    # Handle language switching
    lang = request.GET.get('lang')
    if lang and lang in ['en', 'am']:
        translation.activate(lang)
        request.session['_language'] = lang
    
    settings = get_object_or_404(SiteSettings, is_active=True)
    request.site_settings = settings
    
    # Get the navigation item
    nav_item = get_object_or_404(NavigationItem, id=nav_id)
    
    # Increment click count for navigation item
    nav_item.increment_click_count()
    
    # Get all navigation items for the sidebar
    nav = NavigationItem.objects.prefetch_related('dropdown_items').order_by('order')
    
    # Get sections related to this navigation item (you might want to add a foreign key relationship)
    # For now, we'll get all sections
    sections = Section.objects.filter(is_active=True).order_by('order')
    
    # Get footer
    footer = Footer.objects.filter(is_active=True).first()
    
    return render(request, 'navigation_page.html', {
        'site_settings': settings,
        'nav_item': nav_item,
        'navigation_items': nav,
        'sections': sections,
        'footer': footer,
    })

def navigation_page_by_url(request, nav_url):
    # Handle language switching
    lang = request.GET.get('lang')
    if lang and lang in ['en', 'am']:
        translation.activate(lang)
        request.session['_language'] = lang
    
    settings = get_object_or_404(SiteSettings, is_active=True)
    request.site_settings = settings
    
    # Get the navigation item by URL
    nav_item = get_object_or_404(NavigationItem, url=nav_url)
    
    # Increment click count for navigation item
    nav_item.increment_click_count()
    
    # Get all navigation items for the sidebar
    nav = NavigationItem.objects.prefetch_related('dropdown_items').order_by('order')
    
    # Get sections related to this navigation item (you might want to add a foreign key relationship)
    # For now, we'll get all sections
    sections = Section.objects.filter(is_active=True).order_by('order')
    
    # Get footer
    footer = Footer.objects.filter(is_active=True).first()
    
    return render(request, 'navigation_page.html', {
        'site_settings': settings,
        'nav_item': nav_item,
        'navigation_items': nav,
        'sections': sections,
        'footer': footer,
    })

def track_card_click(request, card_id):
    """Track clicks on card CTAs"""
    if request.method == 'POST':
        card = get_object_or_404(CardBlock, id=card_id)
        card.increment_click_count()
        return JsonResponse({'success': True, 'click_count': card.click_count})
    return JsonResponse({'success': False})

def track_hero_cta_click(request, hero_id):
    """Track clicks on hero section CTAs"""
    if request.method == 'POST':
        hero = get_object_or_404(Hero, id=hero_id)
        hero.increment_cta_click_count()
        return JsonResponse({'success': True, 'cta_click_count': hero.cta_click_count})
    return JsonResponse({'success': False})

def track_section_cta_click(request, section_id):
    """Track clicks on section CTAs"""
    if request.method == 'POST':
        section = get_object_or_404(Section, id=section_id)
        section.increment_view_count()
        return JsonResponse({'success': True, 'view_count': section.view_count})
    return JsonResponse({'success': False})
