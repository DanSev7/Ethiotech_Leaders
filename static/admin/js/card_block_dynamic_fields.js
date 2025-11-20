/**
 * Dynamic Card Block Field Visibility
 * Shows/hides fields and updates labels based on section type
 */
(function($) {
    'use strict';
    
    // Field visibility rules per section type (mirrors Python CARD_FIELD_RULES)
    const FIELD_RULES = {
        'team': {
            visible: ['title', 'image', 'image_alt', 'cta_label', 'text', 'cta_url', 'button_target', 'card_bg_color', 'card_text_color'],
            hidden: ['icon', 'icon_size', 'icon_color', 'icon_layout', 'video_file', 'video_thumbnail', 'video_url', 'button_color', 'button_text_color'],
            labels: {
                'title': 'Name',
                'cta_label': 'Position / Role',
                'text': 'Bio',
                'cta_url': 'Social Link / Profile URL'
            }
        },
        'pricing': {
            visible: ['title', 'cta_label', 'text', 'cta_url', 'button_color', 'button_text_color', 'button_target', 'card_bg_color', 'card_text_color'],
            hidden: ['icon', 'icon_size', 'icon_color', 'icon_layout', 'image', 'image_alt', 'video_file', 'video_thumbnail', 'video_url'],
            labels: {
                'title': 'Plan Name',
                'cta_label': 'Price / Month',
                'text': 'Features List',
                'cta_url': 'Buy / Sign Up Link'
            }
        },
        'faq': {
            visible: ['title', 'text', 'card_bg_color', 'card_text_color'],
            hidden: ['icon', 'icon_size', 'icon_color', 'icon_layout', 'image', 'image_alt', 'video_file', 'video_thumbnail', 'video_url', 'cta_label', 'cta_url', 'button_color', 'button_text_color', 'button_target'],
            labels: {
                'title': 'Question',
                'text': 'Answer'
            }
        },
        'default': {
            visible: ['title', 'text', 'icon', 'icon_size', 'icon_color', 'icon_layout', 'image', 'image_alt', 'video_file', 'video_thumbnail', 'video_url', 'cta_label', 'cta_url', 'button_color', 'button_text_color', 'button_target', 'card_bg_color', 'card_text_color'],
            hidden: [],
            labels: {}
        }
    };
    
    // Section types cache - will be populated from page data
    let sectionsCache = {};
    
    function getSectionType() {
        const sectionSelect = $('#id_section');
        if (!sectionSelect.length) return 'default';
        
        const sectionId = sectionSelect.val();
        if (!sectionId) return 'default';
        
        // Check cache first
        if (sectionsCache[sectionId]) {
            return sectionsCache[sectionId];
        }
        
        // Try to get from data attribute on option
        const option = sectionSelect.find('option[value="' + sectionId + '"]');
        const sectionType = option.data('section-type');
        if (sectionType) {
            sectionsCache[sectionId] = sectionType;
            return sectionType;
        }
        
        return 'default';
    }
    
    function updateFieldVisibility(sectionType) {
        const rules = FIELD_RULES[sectionType] || FIELD_RULES['default'];
        
        // Hide fields and their fieldsets if all fields are hidden
        rules.hidden.forEach(function(fieldName) {
            const fieldRow = $('.form-row.field-' + fieldName);
            if (fieldRow.length) {
                fieldRow.hide();
            }
        });
        
        // Show visible fields and ensure their fieldsets are visible
        rules.visible.forEach(function(fieldName) {
            const fieldRow = $('.form-row.field-' + fieldName);
            if (fieldRow.length) {
                fieldRow.show();
                // Show parent fieldset
                const fieldset = fieldRow.closest('fieldset');
                if (fieldset.length) {
                    fieldset.show();
                }
            }
        });
        
        // Hide fieldsets that have no visible fields
        $('fieldset').each(function() {
            const $fieldset = $(this);
            const visibleRows = $fieldset.find('.form-row').not(':hidden').length;
            if (visibleRows === 0 && $fieldset.find('legend').text() !== 'Card Information') {
                $fieldset.hide();
            }
        });
        
        // Update labels
        Object.keys(rules.labels).forEach(function(fieldName) {
            const label = $('.form-row.field-' + fieldName + ' label');
            if (label.length) {
                const labelText = rules.labels[fieldName];
                // Preserve required asterisk if present
                const hasRequired = label.html().includes('<span class="required">*</span>');
                label.html(labelText + ':' + (hasRequired ? ' <span class="required">*</span>' : ''));
            }
        });
    }
    
    function initializeDynamicFields() {
        // Try to get sections data from a script tag
        const sectionsScript = $('#sections-data-script');
        if (sectionsScript.length) {
            try {
                const sectionsData = JSON.parse(sectionsScript.text());
                sectionsData.forEach(function(section) {
                    sectionsCache[section.id] = section.section_type;
                    // Add data attribute to option
                    $('#id_section option[value="' + section.id + '"]').attr('data-section-type', section.section_type);
                });
            } catch (e) {
                console.warn('Could not parse sections data:', e);
            }
        }
        
        const sectionType = getSectionType();
        updateFieldVisibility(sectionType);
        
        // Listen for section changes
        $('#id_section').on('change', function() {
            const sectionType = getSectionType();
            updateFieldVisibility(sectionType);
        });
    }
    
    $(document).ready(function() {
        // Wait for Django admin to fully initialize
        setTimeout(initializeDynamicFields, 200);
    });
    
})(django.jQuery);

