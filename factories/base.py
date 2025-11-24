import random
from faker import Faker
from faker.providers import BaseProvider


class IranianProvider(BaseProvider):
    """Custom provider for Iranian data generation."""

    IRANIAN_FIRST_NAMES = [
        'علی', 'محمد', 'احمد', 'حسن', 'حسین', 'فرهاد', 'رضا', 'کمال',
        'نادر', 'بهرام', 'سعید', 'شاهین', 'داریوش', 'جهانگیر', 'پرویز',
        'مهران', 'اسفندیار', 'آرتین', 'کیومرث', 'بابک', 'ایرج', 'امیر'
    ]

    IRANIAN_LAST_NAMES = [
        'محمدی', 'علوی', 'حسینی', 'موسوی', 'زاده', 'نژاد', 'پور',
        'فرشادی', 'رفیعی', 'غفاری', 'معمولی', 'مرادی', 'شریفی', 'یاسی',
        'روایتی', 'حیدری', 'اکبری', 'آزادی', 'حقیقی', 'کریمی', 'عادلی'
    ]

    IRANIAN_CITIES = [
        'تهران', 'مشهد', 'اصفهان', 'تبریز', 'شیراز', 'قم', 'اهواز',
        'کرمانشاه', 'رشت', 'کرج', 'بندرعباس', 'همدان', 'هرمزگان',
        'سنندج', 'یاسوج', 'زاهدان', 'کرمان', 'ارومیه', 'بجنورد'
    ]

    IRANIAN_BANK_NAMES = [
        'بانک ملی ایران',
        'بانک سپه',
        'بانک صنعت و معدن',
        'بانک کشاورزی',
        'بانک رفاه',
        'بانک سلام',
        'بانک اقتصاد نوین',
        'بانک تات',
        'بانک پست',
        'بانک توسعه تعاون',
        'بانک توسعه صادرات',
        'بانک گردشگری',
        'بانک حکمت ایرانیان',
        'بانک کارآفرین',
        'بانک توسعه و تعمیر',
        'بانک دی',
    ]

    def iranian_phone_number(self, add_country_code=False):
        """Generate Iranian mobile phone number."""
        if add_country_code:
            prefix = random.choice(['+98', '0098'])
            return f"{prefix}9{random.randint(10, 99)}{random.randint(1000000, 9999999):07d}"
        else:
            return f"09{random.randint(10, 99)}{random.randint(1000000, 9999999):07d}"

    def national_id(self):
        """Generate Iranian national ID (کد ملی)."""
        digits = [random.randint(0, 9) for _ in range(9)]
        check_digit = sum((10 - i) * digit for i, digit in enumerate(digits)) % 11
        if check_digit < 2:
            check_digit = 0
        else:
            check_digit = 11 - check_digit
        
        national_id = ''.join(map(str, digits)) + str(check_digit)
        return national_id.zfill(10)

    def iranian_name(self, gender=None):
        """Generate Iranian full name."""
        first = random.choice(self.IRANIAN_FIRST_NAMES)
        last = random.choice(self.IRANIAN_LAST_NAMES)
        return f"{first} {last}"

    def iranian_city(self):
        """Generate Iranian city."""
        return random.choice(self.IRANIAN_CITIES)

    def bank_name(self):
        """Generate Iranian bank name."""
        return random.choice(self.IRANIAN_BANK_NAMES)

    def iban(self):
        """Generate Iranian IBAN number."""
        return f"IR{''.join([str(random.randint(0, 9)) for _ in range(24)])}"

    def bank_account_number(self):
        """Generate Iranian bank account number."""
        return f"{''.join([str(random.randint(0, 9)) for _ in range(16)])}"


def get_iranian_faker():
    """Get Faker instance with Iranian provider."""
    fake = Faker('fa_IR')
    fake.add_provider(IranianProvider)
    return fake


INVOICE_PURPOSES = [
    'خرید مواد اولیه',
    'اجاره محل',
    'هزینه برق و گاز',
    'هزینه تلفن',
    'هزینه پست و بسته',
    'هزینه سفر کاری',
    'هزینه نرم‌افزار',
    'هزینه تعمیر و نگهداری',
    'هزینه تبلیغات',
    'هزینه حق‌الزحمه',
    'فروش محصول',
    'خدمات مشاوره',
    'درآمد اجاره',
    'سود سرمایه‌گذاری',
]

SERVICE_DESCRIPTIONS = {
    'commercial': [
        'خدمات واردات و صادرات',
        'مشاوره بازاریابی',
        'ثبت شرکت',
        'تدوین قرارداد تجاری',
        'مشاوره مالی',
    ],
    'registration': [
        'ثبت شرکت جدید',
        'تغییر نام تجاری',
        'تغییر مالک',
        'صدور مجوز',
        'تمدید مجوزهای تجاری',
    ],
    'legal': [
        'مشاوره حقوقی',
        'تدوین قرارداد',
        'نمایندگی در دادگاه',
        'مشاوره کار',
        'طراحی سند',
    ],
    'leasing': [
        'اجاره تجهیزات',
        'اجاره تجهیزات صنعتی',
        'اجاره خودرو',
        'اجاره فضای اداری',
        'اجاره دستگاه‌های تکنولوژی',
    ],
}

SALARY_DESCRIPTIONS = [
    'حقوق ماهانه',
    'پاداش عملکرد',
    'بن خواری',
    'اضافه‌کاری',
    'پاداش ختم‌خدمت',
]

POSITIONS = [
    'مدیر',
    'معاون',
    'سرپرست',
    'کارشناس',
    'کارمند',
    'کارگر',
    'سرایدار',
    'چاپگر',
]
