document.addEventListener('DOMContentLoaded', function() {
    const categorySelect = document.getElementById('id_service_category');
    const serviceSelect = document.getElementById('id_service_id');
    const otherServiceTitleField = document.getElementById('id_other_service_title');
    
    if (!categorySelect || !serviceSelect) {
        return;
    }

    const otherServiceTitleRow = otherServiceTitleField ? otherServiceTitleField.closest('.fieldBox') || otherServiceTitleField.closest('.form-group') || otherServiceTitleField.parentElement : null;

    // Initialize the modal service selector
    ServiceModal.init('id_service_category', 'id_service_id', 'service_display_field');
    
    categorySelect.addEventListener('change', function() {
        updateOtherServiceTitleVisibility();
    });

    serviceSelect.addEventListener('change', function() {
        updateOtherServiceTitleVisibility();
    });

    function updateOtherServiceTitleVisibility() {
        const selectedValue = serviceSelect.value;
        if (otherServiceTitleField && otherServiceTitleRow) {
            // Check if service name contains 'سایر' (Other)
            // We'll check the display field or the select value
            const isOtherService = selectedValue && selectedValue.toString().includes('سایر');
            
            if (isOtherService) {
                otherServiceTitleRow.style.display = 'block';
                otherServiceTitleField.required = true;
            } else {
                otherServiceTitleRow.style.display = 'none';
                otherServiceTitleField.required = false;
                otherServiceTitleField.value = '';
            }
        }
    }

    updateOtherServiceTitleVisibility();
});
