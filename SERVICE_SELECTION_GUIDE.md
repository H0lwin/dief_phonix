# دليل نظام اختيار الخدمات

## نظرة عامة
تم تطوير نظام فلترة وبحث ديناميكي لاختيار الخدمات في نماذج فاکتور الشراء والفروش. عندما يختار المستخدم دسته‌بندی خدمت، يتم تحديث قائمة الخدمات تلقائياً لعرض فقط الخدمات المرتبطة بهذه الدسته‌بندی.

## المميزات الرئيسية

### 1. **فلترة ديناميكية**
- عند اختيار دسته‌بندی خدمت، يتم جلب الخدمات المتعلقة بها فقط
- يتم استدعاء API endpoint في `persons/api/services-by-category/`
- تُعرض النتائج في Select Box

### 2. **البحث والتصفية**
- استخدام Select2 library لتوفير مربع بحث قابل للاستخدام
- يمكن البحث بأي جزء من اسم الخدمة
- البحث يدعم اللغة الفارسية

### 3. **دعم كل الفئات**
- **خدمات بازرگانی** (CommercialService)
- **خدمات ثبت** (RegistrationService)  
- **خدمات حقوقی** (LegalService)
- **خدمات لیزینگ** (LeasingService)
- **خدمات وام** (LoanService)

## المكونات الفنية

### Models
- `SalesInvoice` و `PurchaseInvoice` - نماذج الفواتير الرئيسية
- خمسة نماذج خدمة مختلفة في تطبيق `services`

### Forms
- `SalesInvoiceForm` - نموذج فاکتور الفروش
- `PurchaseInvoiceForm` - نموذج فاکتور الشراء

### JavaScript
- `sales_invoice_admin.js` - معالجة الأحداث لنموذج الفروش
- `purchase_invoice_admin.js` - معالجة الأحداث لنموذج الشراء

### API Endpoints
- `/persons/api/services-by-category/?service_type=<type>` - لجلب الخدمات

## سير العمل

### للمستخدم (في Django Admin):

1. **الدخول إلى لوحة المدير**
   - Admin Panel > فاکتورهای فروش (Sales Invoices)
   - أو فاکتورهای خرید (Purchase Invoices)

2. **ملء النموذج**
   - اختر خریدار/فروشنده
   - اختر تاریخ
   - **اختر دسته‌بندی خدمت** ← هنا يحدث السحر
   
3. **بعد اختيار الدسته‌بندی**
   - يتم تفعيل حقل "خدمت" تلقائياً
   - تظهر قائمة بالخدمات المرتبطة فقط
   - يمكن البحث وتصفية الخدمات

4. **اختر الخدمة**
   - اختر من القائمة المتاحة
   - أو اكتب للبحث عن خدمة معينة

## الملفات المحدثة

### 1. `persons/forms.py`
```python
class SalesInvoiceForm(forms.ModelForm):
    service_id = forms.IntegerField(
        required=False,
        widget=forms.Select(attrs={...}),
        label=_('خدمت')
    )
```

### 2. `persons/admin.py`
```python
class SalesInvoiceAdmin(admin.ModelAdmin):
    form = SalesInvoiceForm
    # ... admin configuration
```

### 3. `static/js/sales_invoice_admin.js`
- معالجة أحداث تغيير الفئة
- استدعاء API لجلب الخدمات
- تحديث Select2

### 4. `persons/views.py`
```python
@require_http_methods(["GET"])
@csrf_exempt
def get_services_by_category(request):
    # جلب الخدمات حسب الفئة المختارة
    service_type = request.GET.get('service_type')
    # ... معالجة البيانات
```

## الاختبار

### إضافة بيانات تجريبية:
1. اذهب إلى Django Admin
2. أضف خدمات تحت "خدمات بازرگانی"
3. انتقل لإنشاء فاکتور فروش جديد
4. اختر "خدمات بازرگانی"
5. يجب أن ترى الخدمات المضافة في حقل "خدمت"

## المتطلبات

- Django 4.2+
- Select2 (تم تحميله من CDN)
- JavaScript modern (ES6+)

## ملاحظات مهمة

- يتم استخدام `IntegerField` للـ `service_id` في كلا النموذجين
- يتم التحويل التلقائي للقيم عند الحفظ
- يدعم LoanService الذي يتطلب معالجة خاصة
- النظام يدعم اللغة الفارسية بالكامل

## استكشاف الأخطاء

### المشكلة: لا تظهر الخدمات بعد اختيار الفئة
- تحقق من وجود خدمات نشطة (`is_active=True`) في قاعدة البيانات
- افتح DevTools في المتصفح وتحقق من استدعاء API
- تأكد من تحميل Select2 بشكل صحيح

### المشكلة: البحث لا يعمل
- تأكد من تحميل Select2 من CDN
- تحقق من JavaScript console للأخطاء
- تأكد من معرفات العناصر الصحيحة (id_service_id, id_service_category)

## التطوير المستقبلي

- إضافة عرض معلومات إضافية للخدمات
- تحسين أداء البحث للخدمات الكثيرة
- إضافة خيارات متقدمة للتصفية
