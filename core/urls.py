# core/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('page/<int:nav_id>/', views.navigation_page, name='navigation_page'),
    path('<slug:nav_url>/', views.navigation_page_by_url, name='navigation_page_by_url'),
    path('track/card-click/<int:card_id>/', views.track_card_click, name='track_card_click'),
    path('track/hero-cta-click/<int:hero_id>/', views.track_hero_cta_click, name='track_hero_cta_click'),
    path('track/section-cta-click/<int:section_id>/', views.track_section_cta_click, name='track_section_cta_click'),
]