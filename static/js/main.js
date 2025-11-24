document.addEventListener('DOMContentLoaded', function() {
    console.log('سیستم مدیریت فونیکس بارگذاری شد');

    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            alert.style.display = 'none';
        }, 5000);
    });
});

function fetchDashboardStats() {
    fetch('/dashboard/stats/')
        .then(response => response.json())
        .then(data => {
            console.log('آمار داشبورد:', data);
        })
        .catch(error => console.error('خطا:', error));
}
