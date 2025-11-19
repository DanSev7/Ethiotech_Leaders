"""
Management command to export content analytics data to CSV
"""
import csv
from django.core.management.base import BaseCommand
from django.utils import timezone
from core.models import Section, CardBlock, Hero, NavigationItem

class Command(BaseCommand):
    help = 'Export content analytics data to CSV files'

    def add_arguments(self, parser):
        parser.add_argument(
            '--output-dir',
            type=str,
            default='.',
            help='Directory to save CSV files (default: current directory)'
        )

    def handle(self, *args, **options):
        output_dir = options['output_dir']
        timestamp = timezone.now().strftime('%Y%m%d_%H%M%S')
        
        # Export Section analytics
        self.export_sections(f"{output_dir}/sections_analytics_{timestamp}.csv")
        
        # Export CardBlock analytics
        self.export_card_blocks(f"{output_dir}/card_blocks_analytics_{timestamp}.csv")
        
        # Export Hero analytics
        self.export_hero_sections(f"{output_dir}/hero_sections_analytics_{timestamp}.csv")
        
        # Export NavigationItem analytics
        self.export_navigation_items(f"{output_dir}/navigation_items_analytics_{timestamp}.csv")
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully exported analytics data to {output_dir} with timestamp {timestamp}'
            )
        )

    def export_sections(self, filename):
        """Export section analytics to CSV"""
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = [
                'id', 'name', 'section_type', 'is_active', 'view_count',
                'card_count', 'cta_label', 'cta_url', 'created_at', 'updated_at'
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            for section in Section.objects.all():
                writer.writerow({
                    'id': section.id,
                    'name': section.name,
                    'section_type': section.get_section_type_display(),
                    'is_active': section.is_active,
                    'view_count': section.view_count,
                    'card_count': section.card_block.count(),
                    'cta_label': section.cta_label,
                    'cta_url': section.cta_url,
                    'created_at': section.created_at,
                    'updated_at': section.updated_at,
                })

    def export_card_blocks(self, filename):
        """Export card block analytics to CSV"""
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = [
                'id', 'title', 'section_name', 'is_active', 'click_count',
                'has_image', 'has_video', 'has_cta', 'cta_label', 'cta_url',
                'created_at', 'updated_at'
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            for card in CardBlock.objects.select_related('section').all():
                writer.writerow({
                    'id': card.id,
                    'title': card.title,
                    'section_name': card.section.name if card.section else '',
                    'is_active': card.is_active,
                    'click_count': card.click_count,
                    'has_image': bool(card.image),
                    'has_video': bool(card.video_file or card.video_url),
                    'has_cta': bool(card.cta_label and card.cta_url),
                    'cta_label': card.cta_label,
                    'cta_url': card.cta_url,
                    'created_at': card.created_at,
                    'updated_at': card.updated_at,
                })

    def export_hero_sections(self, filename):
        """Export hero section analytics to CSV"""
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = [
                'id', 'title', 'layout_type', 'is_active', 'view_count',
                'cta_click_count', 'rotating_text_count', 'background_image_count',
                'cta_text', 'cta_link', 'created_at', 'updated_at'
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            for hero in Hero.objects.all():
                writer.writerow({
                    'id': hero.id,
                    'title': hero.title,
                    'layout_type': hero.get_layout_type_display(),
                    'is_active': hero.is_active,
                    'view_count': hero.view_count,
                    'cta_click_count': hero.cta_click_count,
                    'rotating_text_count': hero.rotating_texts.count(),
                    'background_image_count': hero.background_images.count(),
                    'cta_text': hero.cta_text,
                    'cta_link': hero.cta_link,
                    'created_at': hero.created_at,
                    'updated_at': hero.updated_at,
                })

    def export_navigation_items(self, filename):
        """Export navigation item analytics to CSV"""
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = [
                'id', 'label', 'url', 'is_active', 'is_dropdown', 'is_button',
                'click_count', 'dropdown_item_count', 'created_at', 'updated_at'
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            for nav_item in NavigationItem.objects.prefetch_related('dropdown_items').all():
                writer.writerow({
                    'id': nav_item.id,
                    'label': nav_item.label,
                    'url': nav_item.url,
                    'is_active': nav_item.is_active,
                    'is_dropdown': nav_item.is_dropdown,
                    'is_button': nav_item.is_button,
                    'click_count': nav_item.click_count,
                    'dropdown_item_count': nav_item.dropdown_items.count(),
                    'created_at': nav_item.created_at,
                    'updated_at': nav_item.updated_at,
                })