(function() {
    let currentInputId = null;
    let iconsPopulated = false;
    
    // Add clear icon function
    function clearIcon(inputId) {
        if (inputId) {
            const input = document.getElementById(inputId);
            const preview = document.getElementById(`${inputId}_preview`);
            
            if (input) {
                input.value = '';
            }
            
            if (preview) {
                preview.innerHTML = '<span style="color:#999;">No icon selected</span>';
            }
        }
    }
    
    // Make sure clearIcon is available globally
    if (typeof window !== 'undefined') {
        window.clearIcon = clearIcon;
    }

    // --- Utility Function: CRITICAL FIX FOR CASE MISMATCH ---
    function pascalToKebabCase(name) {
        // Handle common camelCase/PascalCase to kebab-case conversion
        // First handle sequences of capitals followed by lowercase (XMLHttpRequest -> xml-http-request)
        let result = name.replace(/([A-Z]+)([A-Z][a-z])/g, '$1-$2');
        // Then handle normal camelCase (camelCase -> camel-case)
        result = result.replace(/([a-z])([A-Z])/g, '$1-$2');
        // Handle numbers (icon1 -> icon-1)
        result = result.replace(/([a-zA-Z])(\d)/g, '$1-$2');
        result = result.replace(/(\d)([a-zA-Z])/g, '$1-$2');
        return result.toLowerCase();
    }

    // --- Core Functions ---

    // Function to get all Lucide icon names (returns them in kebab-case)
    function getAllLucideIcons() {
        if (typeof lucide !== 'undefined' && lucide.icons) {
            // Lucide.icons keys are already in kebab-case/snake_case/lower-case, so we use them directly.
            return Object.keys(lucide.icons);
        }
        console.error('Lucide icons object is not yet available.');
        return [];
    }

    // Function to categorize icons alphabetically
    function categorizeIcons(iconNames) {
        const categories = {};
        iconNames.sort().forEach(iconName => {
            // Use the first letter of the kebab-case name for categorization
            const firstLetter = iconName.charAt(0).toUpperCase(); 
            if (!categories[firstLetter]) {
                categories[firstLetter] = [];
            }
            categories[firstLetter].push(iconName);
        });
        return categories;
    };

    // --- Modal Structure & Population (Optimized) ---

    function createIconPickerModal() {
        if (document.getElementById('icon-picker-modal')) {
            return document.getElementById('icon-picker-modal');
        }

        // Create Modal and Content containers (CSS styles omitted for brevity, ensure they are in admin/css/icon-picker.css)
        const modal = document.createElement('div');
        modal.id = 'icon-picker-modal';
        modal.className = 'icon-picker-modal';
        modal.style.cssText = `display: none; position: fixed; z-index: 10000; left: 0; top: 0; width: 100%; height: 100%; background-color: rgba(0,0,0,0.5);`;

        const modalContent = document.createElement('div');
        modalContent.className = 'icon-picker-modal-content';
        modalContent.style.cssText = `background-color: #fff; margin: 5% auto; padding: 20px; border-radius: 8px; width: 80%; max-width: 800px; max-height: 80vh; overflow: hidden; box-shadow: 0 4px 6px rgba(0,0,0,0.1);`;

        const iconsContainer = document.createElement('div');
        iconsContainer.id = 'icon-picker-icons-container';
        iconsContainer.className = 'icon-picker-icons';
        iconsContainer.style.cssText = `display: grid; grid-template-columns: repeat(auto-fill, minmax(80px, 1fr)); gap: 15px; max-height: 60vh; overflow-y: auto; padding: 10px 0;`;

        // Create Header & Search
        const header = document.createElement('div');
        header.className = 'icon-picker-header';
        header.style.cssText = `display: flex; justify-content: space-between; align-items: center; padding-bottom: 15px; border-bottom: 1px solid #eee;`;
        
        const title = document.createElement('h2');
        title.textContent = 'Select an Icon';
        title.style.margin = '0';

        const closeButton = document.createElement('button');
        closeButton.innerHTML = '&times;';
        closeButton.style.cssText = `background: none; border: none; font-size: 24px; cursor: pointer; color: #999;`;
        closeButton.onclick = () => modal.style.display = 'none';

        header.appendChild(title);
        header.appendChild(closeButton);

        const searchInput = document.createElement('input');
        searchInput.type = 'text';
        searchInput.placeholder = 'Search icons...';
        searchInput.className = 'icon-search';
        searchInput.style.cssText = `width: 100%; padding: 10px; margin: 15px 0; border: 1px solid #ddd; border-radius: 4px; box-sizing: border-box;`;

        // Search Functionality (Now uses kebab-case for comparison)
        searchInput.addEventListener('input', (e) => {
            const searchTerm = e.target.value.toLowerCase();
            const items = iconsContainer.querySelectorAll('.icon-wrapper, .icon-category-header');
            
            items.forEach(item => {
                if (item.classList.contains('icon-category-header')) {
                    return; 
                }
                const iconName = item.querySelector('span').textContent.toLowerCase();
                item.style.display = iconName.includes(searchTerm) ? 'block' : 'none';
            });

            // Logic to hide empty category headers
            iconsContainer.querySelectorAll('.icon-category-header').forEach(header => {
                let nextSibling = header.nextElementSibling;
                let visibleIcons = 0;
                while (nextSibling && !nextSibling.classList.contains('icon-category-header')) {
                    if (nextSibling.style.display !== 'none') {
                        visibleIcons++;
                    }
                    nextSibling = nextSibling.nextElementSibling;
                }
                header.style.display = visibleIcons > 0 ? 'block' : 'none';
            });
        });

        // Assemble modal
        modalContent.appendChild(header);
        modalContent.appendChild(searchInput);
        modalContent.appendChild(iconsContainer);
        modal.appendChild(modalContent);
        document.body.appendChild(modal);

        return modal;
    }

    function populateIcons() {
        if (iconsPopulated) {
            return;
        }

        const iconsContainer = document.getElementById('icon-picker-icons-container');
        if (!iconsContainer) return;

        iconsContainer.innerHTML = ''; 

        const allIcons = getAllLucideIcons();
        
        if (allIcons.length === 0) {
            iconsContainer.innerHTML = '<p style="grid-column: 1 / -1; text-align: center; color: red;">Error: Lucide icons are not available. Check CDN link and browser console.</p>';
            return;
        }

        const lucideIcons = categorizeIcons(allIcons);
        
        // Update the modal title with the total count
        const titleElement = document.querySelector('.icon-picker-header h2');
        if (titleElement) {
            titleElement.textContent = `Select an Icon (${allIcons.length} total)`;
        }

        Object.keys(lucideIcons).forEach(category => {
            // Category Header
            const categoryHeader = document.createElement('div');
            categoryHeader.className = 'icon-category-header';
            categoryHeader.style.cssText = `grid-column: 1 / -1; margin: 20px 0 10px 0; padding: 10px 0; border-bottom: 2px solid #eee; font-weight: bold; font-size: 18px; color: #333;`;
            categoryHeader.textContent = category;
            iconsContainer.appendChild(categoryHeader);
            
            // Icons for this category
            lucideIcons[category].forEach(iconName => {
                const iconWrapper = document.createElement('div');
                iconWrapper.className = 'icon-wrapper';
                iconWrapper.style.cssText = `text-align: center; padding: 10px; border: 1px solid #eee; border-radius: 4px; cursor: pointer; transition: all 0.2s;`;
                iconWrapper.onclick = () => selectIcon(iconName); // iconName is already kebab-case here

                // This <i> tag is what Lucide replaces with the SVG
                // Ensure the icon name is in kebab-case
                const kebabIconName = pascalToKebabCase(iconName);
                const iconElement = document.createElement('i');
                iconElement.setAttribute('data-lucide', kebabIconName);
                iconElement.style.cssText = `width: 32px; height: 32px; display: block; margin: 0 auto 8px; color: #495057;`;
                
                // Add a fallback for missing icons
                iconElement.setAttribute('data-lucide-fallback', 'help-circle');

                const iconLabel = document.createElement('span');
                iconLabel.textContent = iconName;
                iconLabel.style.cssText = `font-size: 12px; display: block; overflow: hidden; text-overflow: ellipsis;`;

                iconWrapper.appendChild(iconElement);
                iconWrapper.appendChild(iconLabel);
                iconsContainer.appendChild(iconWrapper);
            });
        });
        
        // Call Lucide's creation function ONLY once after all icons are added
        if (typeof lucide !== 'undefined') {
            lucide.createIcons({ parent: iconsContainer }); 
        }

        iconsPopulated = true;
    }

    // --- Global Functions ---

    window.openIconPicker = function(inputId) {
        currentInputId = inputId;
        const modal = createIconPickerModal();
        modal.style.display = 'block';
        
        if (!iconsPopulated) {
            populateIcons();
        } else {
            if (typeof lucide !== 'undefined') {
                 // Re-render hidden icons when modal opens
                 setTimeout(() => lucide.createIcons(), 10); 
            }
        }
    };

    // clearIcon function is defined above and attached to window

    function selectIcon(iconName) {
        if (currentInputId) {
            const input = document.getElementById(currentInputId);
            const preview = document.getElementById(`${currentInputId}_preview`);
            
            // IMPORTANT: The value saved to the database/input must be the kebab-case name!
            if (input) {
                input.value = iconName; 
            }
            
            if (preview) {
                // Update preview element with the kebab-case name
                const kebabIconName = pascalToKebabCase(iconName);
                preview.innerHTML = `<span style="display:inline-flex; align-items:center; vertical-align:middle;">
                                        <i data-lucide="${kebabIconName}" data-lucide-fallback="help-circle" style="width:24px;height:24px;margin-right:8px;color:currentColor;"></i>
                                        ${iconName}
                                     </span>`;
                
                // CRITICAL: Re-run Lucide's creation function on the preview element
                if (typeof lucide !== 'undefined') {
                    lucide.createIcons({ parent: preview }); 
                }
            }
        }
        
        document.getElementById('icon-picker-modal').style.display = 'none';
    }

    // --- Initialization & Event Listeners ---
    
    document.addEventListener('DOMContentLoaded', createIconPickerModal);

    window.addEventListener('load', function() {
        populateIcons(); 
        
        // Render initial previews for existing icons in the form
        if (typeof lucide !== 'undefined') {
            // Find all inputs that are part of the IconPickerWidget
            document.querySelectorAll('.icon-picker-input').forEach(input => {
                const iconName = input.value;
                const preview = document.getElementById(`${input.id}_preview`);
                
                // If the value exists, but the preview is still using a non-rendered <i> tag
                if (iconName && preview) {
                    // This is the step that fixes existing DB values: 
                    // It tries to convert the database value to kebab-case for rendering.
                    // If the DB already uses kebab-case, it's harmless.
                    const kebabIconName = pascalToKebabCase(iconName); 
                    
                    preview.innerHTML = `<span style="display:inline-flex; align-items:center; vertical-align:middle;">
                                            <i data-lucide="${kebabIconName}" data-lucide-fallback="help-circle" style="width:24px;height:24px;margin-right:8px;color:currentColor;"></i>
                                            ${iconName}
                                         </span>`;

                    // Re-render the icon
                    if (typeof lucide !== 'undefined') {
                        lucide.createIcons({ parent: preview });
                    }
                } else if (!iconName && preview) {
                    // Handle case where there's no icon selected
                    preview.innerHTML = '<span style="color:#999;">No icon selected</span>';
                }
            });
            // Final call to render all current and initial icon placeholders
            lucide.createIcons(); 
        }
    });

    // Close modal when clicking outside or pressing escape key
    document.addEventListener('click', function(e) {
        const modal = document.getElementById('icon-picker-modal');
        if (modal && e.target === modal) {
            modal.style.display = 'none';
        }
    });

    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            const modal = document.getElementById('icon-picker-modal');
            if (modal) {
                modal.style.display = 'none';
            }
        }
    });

})();