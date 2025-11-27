function toggleDateFields() {
    const checkbox = document.getElementById('id_use_date_range');
    const singleDateDiv = document.querySelector('.single-date-input');
    const dateRangeDiv = document.querySelector('.date-range-input');
    
    if (checkbox.checked) {
        singleDateDiv.style.display = 'none';
        dateRangeDiv.style.display = 'grid';
    } else {
        singleDateDiv.style.display = 'block';
        dateRangeDiv.style.display = 'none';
    }
}

function loadServices() {
    const category = document.getElementById('id_service_category').value;
    const serviceIdField = document.getElementById('id_service_id');
    
    if (!category) {
        serviceIdField.innerHTML = '<option value="">انتخاب دسته‌بندی ابتدا</option>';
        return;
    }
    
    const apiUrl = document.querySelector('[data-api-url]').dataset.apiUrl;
    fetch(apiUrl + '?category=' + category)
        .then(response => response.json())
        .then(data => {
            const services = data.services || [];
            serviceIdField.innerHTML = '<option value="">تمام خدمات</option>';
            services.forEach(service => {
                const option = document.createElement('option');
                option.value = service.id;
                option.textContent = service.name;
                serviceIdField.appendChild(option);
            });
        });
}

document.addEventListener('DOMContentLoaded', function() {
    toggleDateFields();
    const checkbox = document.getElementById('id_use_date_range');
    if (checkbox) {
        checkbox.addEventListener('change', toggleDateFields);
    }
    
    const categorySelect = document.getElementById('id_service_category');
    if (categorySelect) {
        categorySelect.addEventListener('change', loadServices);
    }
});
