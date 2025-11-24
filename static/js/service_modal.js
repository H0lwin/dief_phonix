const ServiceModal = {
    currentCategorySelect: null,
    currentServiceSelect: null,
    selectedServiceId: null,
    selectedServiceName: null,
    currentServiceType: null,
    
    init(categorySelectId, serviceSelectId, displayFieldId) {
        this.categorySelectElement = document.getElementById(categorySelectId);
        this.serviceSelectElement = document.getElementById(serviceSelectId);
        this.displayFieldElement = document.getElementById(displayFieldId);
        
        if (!this.categorySelectElement || !this.serviceSelectElement) {
            console.error('Required elements not found');
            return;
        }
        
        this.setupElements();
        this.attachEventListeners();
    },
    
    setupElements() {
        // Hide the original select element
        this.serviceSelectElement.style.display = 'none';
        
        // Create display field if it doesn't exist
        if (!this.displayFieldElement) {
            const wrapper = this.serviceSelectElement.parentElement;
            this.displayFieldElement = document.createElement('div');
            this.displayFieldElement.id = 'service_display_field';
            this.displayFieldElement.className = 'service-field-display';
            this.displayFieldElement.innerHTML = '<span class="service-field-display-placeholder">ابتدا دسته‌بندی را انتخاب کنید</span>';
            wrapper.insertBefore(this.displayFieldElement, this.serviceSelectElement);
        }
        
        // Create modal if it doesn't exist
        if (!document.getElementById('service_modal_overlay')) {
            this.createModal();
        }
    },
    
    createModal() {
        const modalHTML = `
            <div id="service_modal_overlay" class="service-modal-overlay">
                <div class="service-modal">
                    <div class="service-modal-header">
                        <h3>انتخاب خدمت</h3>
                        <button type="button" class="service-modal-close" id="service_modal_close">×</button>
                    </div>
                    <div class="service-modal-search">
                        <input 
                            type="text" 
                            id="service_search_input" 
                            placeholder="جستجو برای خدمت..."
                            autocomplete="off"
                        />
                    </div>
                    <div class="service-modal-body">
                        <div id="service_list_container"></div>
                    </div>
                    <div class="service-modal-footer">
                        <button type="button" class="service-modal-button cancel" id="service_modal_cancel">انصراف</button>
                        <button type="button" class="service-modal-button confirm" id="service_modal_confirm" disabled>تأیید</button>
                    </div>
                </div>
            </div>
        `;
        
        document.body.insertAdjacentHTML('beforeend', modalHTML);
        
        // Attach modal event listeners
        document.getElementById('service_modal_close').addEventListener('click', () => this.closeModal());
        document.getElementById('service_modal_cancel').addEventListener('click', () => this.closeModal());
        document.getElementById('service_modal_confirm').addEventListener('click', () => this.confirmSelection());
        document.getElementById('service_search_input').addEventListener('input', (e) => this.filterServices(e.target.value));
        document.getElementById('service_modal_overlay').addEventListener('click', (e) => {
            if (e.target.id === 'service_modal_overlay') {
                this.closeModal();
            }
        });
    },
    
    attachEventListeners() {
        this.categorySelectElement.addEventListener('change', () => this.onCategoryChange());
        this.displayFieldElement.addEventListener('click', () => this.openModal());
    },
    
    onCategoryChange() {
        const serviceType = this.categorySelectElement.value;
        
        if (!serviceType) {
            this.resetServiceField();
            return;
        }
        
        this.currentServiceType = serviceType;
        this.openModal();
    },
    
    openModal() {
        const serviceType = this.categorySelectElement.value;
        
        if (!serviceType) {
            alert('لطفاً ابتدا دسته‌بندی خدمت را انتخاب کنید');
            return;
        }
        
        this.loadServices(serviceType);
        document.getElementById('service_modal_overlay').classList.add('active');
        document.getElementById('service_search_input').focus();
    },
    
    closeModal() {
        document.getElementById('service_modal_overlay').classList.remove('active');
        document.getElementById('service_search_input').value = '';
        this.selectedServiceId = null;
        this.selectedServiceName = null;
        document.getElementById('service_modal_confirm').disabled = true;
    },
    
    loadServices(serviceType) {
        const container = document.getElementById('service_list_container');
        container.innerHTML = `
            <div class="service-modal-loading">
                <div class="service-modal-loading-spinner"></div>
                <div>در حال بارگیری خدمات...</div>
            </div>
        `;
        
        const url = `/persons/api/services-by-category/?service_type=${encodeURIComponent(serviceType)}`;
        
        fetch(url)
            .then(response => {
                if (!response.ok) throw new Error('Network error');
                return response.json();
            })
            .then(data => {
                if (data.success && data.services && Array.isArray(data.services)) {
                    this.renderServicesList(data.services);
                } else {
                    container.innerHTML = '<div class="service-modal-empty">خدمتی موجود نیست</div>';
                }
            })
            .catch(error => {
                console.error('Error loading services:', error);
                container.innerHTML = '<div class="service-modal-empty"><div class="service-modal-empty-icon">⚠️</div><div class="service-modal-empty-text">خطا در بارگیری خدمات</div></div>';
            });
    },
    
    renderServicesList(services) {
        const container = document.getElementById('service_list_container');
        
        if (services.length === 0) {
            container.innerHTML = '<div class="service-modal-empty"><div class="service-modal-empty-icon">📭</div><div class="service-modal-empty-text">خدمتی موجود نیست</div></div>';
            return;
        }
        
        const listHTML = `
            <ul class="service-list">
                ${services.map(service => `
                    <li class="service-list-item" data-service-id="${service.id}" data-service-name="${this.escapeHtml(service.name)}">
                        <div class="service-list-item-content">
                            <span class="service-list-item-name">${this.escapeHtml(service.name)}</span>
                        </div>
                    </li>
                `).join('')}
            </ul>
        `;
        
        container.innerHTML = listHTML;
        
        // Attach click listeners to service items
        container.querySelectorAll('.service-list-item').forEach(item => {
            item.addEventListener('click', () => this.selectService(item));
        });
    },
    
    selectService(item) {
        // Remove previous selection
        document.querySelectorAll('.service-list-item').forEach(i => i.classList.remove('active'));
        
        // Add active class to clicked item
        item.classList.add('active');
        
        // Store selected service data
        this.selectedServiceId = item.getAttribute('data-service-id');
        this.selectedServiceName = item.getAttribute('data-service-name');
        
        // Enable confirm button
        document.getElementById('service_modal_confirm').disabled = false;
    },
    
    filterServices(searchTerm) {
        const items = document.querySelectorAll('.service-list-item');
        const term = searchTerm.toLowerCase().trim();
        
        let visibleCount = 0;
        
        items.forEach(item => {
            const name = item.getAttribute('data-service-name').toLowerCase();
            if (name.includes(term)) {
                item.style.display = '';
                visibleCount++;
            } else {
                item.style.display = 'none';
            }
        });
        
        // Show empty message if no results
        if (visibleCount === 0 && term.length > 0) {
            const container = document.getElementById('service_list_container');
            if (!document.getElementById('no_results_message')) {
                const message = document.createElement('div');
                message.id = 'no_results_message';
                message.className = 'service-modal-empty';
                message.innerHTML = `<div class="service-modal-empty-icon">🔍</div><div class="service-modal-empty-text">بدون نتیجه برای: ${this.escapeHtml(searchTerm)}</div>`;
                container.appendChild(message);
            }
        } else {
            const noResults = document.getElementById('no_results_message');
            if (noResults) {
                noResults.remove();
            }
        }
    },
    
    confirmSelection() {
        if (!this.selectedServiceId) {
            return;
        }
        
        // Set the hidden select value
        this.serviceSelectElement.value = this.selectedServiceId;
        
        // Update display field
        this.displayFieldElement.innerHTML = `<span class="service-field-display-value">${this.escapeHtml(this.selectedServiceName)}</span>`;
        this.displayFieldElement.classList.add('active');
        
        // Close modal
        this.closeModal();
        
        // Trigger change event on the actual select
        const event = new Event('change', { bubbles: true });
        this.serviceSelectElement.dispatchEvent(event);
    },
    
    resetServiceField() {
        this.serviceSelectElement.value = '';
        this.displayFieldElement.innerHTML = '<span class="service-field-display-placeholder">ابتدا دسته‌بندی را انتخاب کنید</span>';
        this.displayFieldElement.classList.remove('active');
        this.selectedServiceId = null;
        this.selectedServiceName = null;
    },
    
    escapeHtml(text) {
        const map = {
            '&': '&amp;',
            '<': '&lt;',
            '>': '&gt;',
            '"': '&quot;',
            "'": '&#039;'
        };
        return text.replace(/[&<>"']/g, m => map[m]);
    }
};

// Wait for DOM to be ready before initializing
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function() {
        // Will be initialized by the invoice admin JS files
    });
}
