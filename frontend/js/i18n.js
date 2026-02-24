/**
 * Internationalization (i18n) - English & Arabic Support
 */

const translations = {
    en: {
        // Navigation
        login: 'Login',
        getStarted: 'Get Started',
        register: 'Register',

        // Hero
        heroTitle: 'AI-Powered Skin Disease Diagnosis',
        heroSubtitle: 'Get accurate skin condition analysis in minutes using advanced AI technology, with optional verification from certified dermatologists.',
        startDiagnosis: 'Start Diagnosis',
        howItWorks: 'How It Works',
        uploadSkinPhoto: 'Upload a photo of your skin condition',

        // Banner Slides
        slide1Title: 'AI-Powered Skin<br>Disease Diagnosis',
        slide1Desc: 'Get accurate skin analysis in minutes using advanced AI technology.',
        slide2Title: 'Verified by<br>Expert Doctors',
        slide2Desc: 'Optional verification from certified dermatologists for peace of mind.',
        slide3Title: 'Results in<br>Under 2 Minutes',
        slide3Desc: 'Upload a photo and get your diagnosis with treatment recommendations.',

        // Stats
        accuracy: 'Accuracy',
        diagnoses: 'Diagnoses',
        doctors: 'Doctors',
        available: 'Available',
        results: 'Results',
        conditions: 'Conditions',

        // Steps
        howItWorksTitle: 'How It Works',
        step1Title: 'Upload Photo',
        step1Desc: 'Take or upload a clear photo of the affected skin area.',
        step2Title: 'AI Analysis',
        step2Desc: 'Our multi-stage AI analyzes your image in seconds.',
        step3Title: 'Doctor Review',
        step3Desc: 'Optional verification by certified dermatologists.',
        step4Title: 'Get Treatment',
        step4Desc: 'Receive diagnosis with recommendations.',

        // Features
        featuresTitle: 'Why Choose Us',
        feature1Title: 'High Accuracy',
        feature1Desc: 'Multi-stage AI pipeline with 98% accuracy rate.',
        feature2Title: 'Fast Results',
        feature2Desc: 'Get preliminary diagnosis in under 2 minutes.',
        feature3Title: 'Secure & Private',
        feature3Desc: 'Your medical data is encrypted and protected.',
        feature4Title: 'Multilingual',
        feature4Desc: 'Available in English and Arabic.',

        // CTA
        ctaTitle: 'Ready to Get Started?',
        ctaDesc: 'Join thousands of users getting accurate skin diagnoses.',
        createAccount: 'Create Free Account',

        // Footer
        footerDesc: 'AI-powered skin disease diagnosis',
        privacy: 'Privacy Policy',
        terms: 'Terms of Service',
        contact: 'Contact',
        disclaimer: '⚠️ This service is for informational purposes only and does not replace professional medical advice. Always consult a qualified healthcare provider for medical concerns.',

        // Auth
        loginTitle: 'Welcome Back',
        loginSubtitle: 'Sign in to your account',
        registerTitle: 'Create Account',
        registerSubtitle: 'Start your journey to better skin health',
        email: 'Email',
        password: 'Password',
        rememberMe: 'Remember me',
        forgotPassword: 'Forgot password?',
        signIn: 'Sign In',
        noAccount: "Don't have an account?",
        signUp: 'Sign up',
        haveAccount: 'Already have an account?',
        patient: 'Patient',
        doctor: 'Doctor',
        firstName: 'First Name',
        lastName: 'Last Name',
        phone: 'Phone Number',
        confirmPassword: 'Confirm Password',
        licenseNumber: 'Medical License Number',
        specialty: 'Specialty',
        agreeTerms: 'I agree to the',
        termsOfService: 'Terms of Service',
        and: 'and',
        privacyPolicy: 'Privacy Policy',

        // Dashboard
        dashboard: 'Dashboard',
        newDiagnosis: 'New Diagnosis',
        history: 'History',
        wallet: 'Wallet',
        assistant: 'AI Assistant',
        profile: 'Profile',
        settings: 'Settings',
        logout: 'Logout',

        // Common
        submit: 'Submit',
        cancel: 'Cancel',
        save: 'Save',
        delete: 'Delete',
        edit: 'Edit',
        view: 'View',
        loading: 'Loading...',
        error: 'Error',
        success: 'Success',
        back: 'Back',
        next: 'Next',
        close: 'Close'
    },
    ar: {
        // Navigation
        login: 'تسجيل الدخول',
        getStarted: 'ابدأ الآن',
        register: 'التسجيل',

        // Hero
        heroTitle: 'تشخيص أمراض الجلد بالذكاء الاصطناعي',
        heroSubtitle: 'احصل على تحليل دقيق لحالة بشرتك في دقائق باستخدام تقنية الذكاء الاصطناعي المتقدمة، مع إمكانية التحقق من أطباء جلدية معتمدين.',
        startDiagnosis: 'ابدأ التشخيص',
        howItWorks: 'كيف يعمل',
        uploadSkinPhoto: 'قم بتحميل صورة لحالة بشرتك',

        // Banner Slides
        slide1Title: 'تشخيص أمراض الجلد<br>بالذكاء الاصطناعي',
        slide1Desc: 'احصل على تحليل دقيق للبشرة في دقائق باستخدام تقنية الذكاء الاصطناعي.',
        slide2Title: 'معتمد من<br>أطباء خبراء',
        slide2Desc: 'تحقق اختياري من أطباء جلدية معتمدين لراحة بالك.',
        slide3Title: 'نتائج في<br>أقل من دقيقتين',
        slide3Desc: 'ارفع صورة واحصل على تشخيصك مع توصيات العلاج.',

        // Stats
        accuracy: 'الدقة',
        diagnoses: 'التشخيصات',
        doctors: 'الأطباء',
        available: 'متاح',
        results: 'النتائج',
        conditions: 'الحالات',

        // Steps
        howItWorksTitle: 'كيف يعمل',
        step1Title: 'ارفع صورة',
        step1Desc: 'التقط أو ارفع صورة واضحة للمنطقة المصابة.',
        step2Title: 'تحليل الذكاء الاصطناعي',
        step2Desc: 'يقوم الذكاء الاصطناعي بتحليل صورتك في ثوانٍ.',
        step3Title: 'مراجعة الطبيب',
        step3Desc: 'تحقق اختياري من أطباء جلدية معتمدين.',
        step4Title: 'احصل على العلاج',
        step4Desc: 'استلم التشخيص مع التوصيات.',

        // Features
        featuresTitle: 'لماذا تختارنا',
        feature1Title: 'دقة عالية',
        feature1Desc: 'نظام ذكاء اصطناعي متعدد المراحل بدقة 98%.',
        feature2Title: 'نتائج سريعة',
        feature2Desc: 'احصل على تشخيص مبدئي في أقل من دقيقتين.',
        feature3Title: 'آمن وخاص',
        feature3Desc: 'بياناتك الطبية مشفرة ومحمية.',
        feature4Title: 'متعدد اللغات',
        feature4Desc: 'متاح باللغتين الإنجليزية والعربية.',

        // CTA
        ctaTitle: 'مستعد للبدء؟',
        ctaDesc: 'انضم إلى آلاف المستخدمين الذين يحصلون على تشخيصات دقيقة.',
        createAccount: 'إنشاء حساب مجاني',

        // Footer
        footerDesc: 'تشخيص أمراض الجلد بالذكاء الاصطناعي',
        privacy: 'سياسة الخصوصية',
        terms: 'شروط الخدمة',
        contact: 'اتصل بنا',
        disclaimer: '⚠️ هذه الخدمة لأغراض إعلامية فقط ولا تحل محل الاستشارة الطبية المتخصصة. استشر دائماً مقدم رعاية صحية مؤهل.',

        // Auth
        loginTitle: 'مرحباً بعودتك',
        loginSubtitle: 'سجل الدخول إلى حسابك',
        registerTitle: 'إنشاء حساب',
        registerSubtitle: 'ابدأ رحلتك نحو بشرة أفضل',
        email: 'البريد الإلكتروني',
        password: 'كلمة المرور',
        rememberMe: 'تذكرني',
        forgotPassword: 'نسيت كلمة المرور؟',
        signIn: 'تسجيل الدخول',
        noAccount: 'ليس لديك حساب؟',
        signUp: 'إنشاء حساب',
        haveAccount: 'لديك حساب بالفعل؟',
        patient: 'مريض',
        doctor: 'طبيب',
        firstName: 'الاسم الأول',
        lastName: 'اسم العائلة',
        phone: 'رقم الهاتف',
        confirmPassword: 'تأكيد كلمة المرور',
        licenseNumber: 'رقم الترخيص الطبي',
        specialty: 'التخصص',
        agreeTerms: 'أوافق على',
        termsOfService: 'شروط الخدمة',
        and: 'و',
        privacyPolicy: 'سياسة الخصوصية',

        // Dashboard
        dashboard: 'لوحة التحكم',
        newDiagnosis: 'تشخيص جديد',
        history: 'السجل',
        wallet: 'المحفظة',
        assistant: 'المساعد الذكي',
        profile: 'الملف الشخصي',
        settings: 'الإعدادات',
        logout: 'تسجيل الخروج',

        // Common
        submit: 'إرسال',
        cancel: 'إلغاء',
        save: 'حفظ',
        delete: 'حذف',
        edit: 'تعديل',
        view: 'عرض',
        loading: 'جاري التحميل...',
        error: 'خطأ',
        success: 'نجاح',
        back: 'رجوع',
        next: 'التالي',
        close: 'إغلاق'
    }
};

const i18n = {
    currentLang: 'en',

    /**
     * Get translation
     */
    t(key) {
        const lang = translations[this.currentLang] || translations.en;
        return lang[key] || translations.en[key] || key;
    },

    /**
     * Change language
     */
    setLang(lang) {
        const supportedLangs = window.Config ? Config.SUPPORTED_LANGS : ['en', 'ar'];
        if (supportedLangs.includes(lang)) {
            this.currentLang = lang;
            localStorage.setItem('lang', lang);
            document.documentElement.lang = lang;
            document.documentElement.dir = lang === 'ar' ? 'rtl' : 'ltr';
            this.updatePage();
            this.updateToggleButton();

            // Dispatch event for components that need to react
            window.dispatchEvent(new CustomEvent('langchange', { detail: { lang } }));
        }
    },

    /**
     * Toggle language
     */
    toggle() {
        const newLang = this.currentLang === 'en' ? 'ar' : 'en';
        this.setLang(newLang);
    },

    /**
     * Update toggle button display
     */
    updateToggleButton() {
        const toggle = document.getElementById('lang-toggle');
        if (toggle) {
            const displayLang = this.currentLang === 'en' ? 'عربي' : 'EN';
            toggle.innerHTML = `<span>${displayLang}</span>`;
        }
    },

    /**
     * Update all elements with data-i18n
     */
    updatePage() {
        document.querySelectorAll('[data-i18n]').forEach(el => {
            const key = el.getAttribute('data-i18n');
            const translated = this.t(key);
            if (el.tagName === 'INPUT' || el.tagName === 'TEXTAREA') {
                // For form elements, check if it should be placeholder
                if (el.getAttribute('data-i18n-attr') === 'placeholder') {
                    el.placeholder = translated;
                } else {
                    el.value = translated;
                }
            } else {
                // Use innerHTML to support HTML tags like <br> in translations
                el.innerHTML = translated;
            }
        });

        document.querySelectorAll('[data-i18n-placeholder]').forEach(el => {
            const key = el.getAttribute('data-i18n-placeholder');
            el.placeholder = this.t(key);
        });

        document.querySelectorAll('[data-i18n-title]').forEach(el => {
            const key = el.getAttribute('data-i18n-title');
            el.title = this.t(key);
        });

        document.querySelectorAll('[data-i18n-aria]').forEach(el => {
            const key = el.getAttribute('data-i18n-aria');
            el.setAttribute('aria-label', this.t(key));
        });
    },

    /**
     * Initialize
     */
    init() {
        // Get saved language or default
        const defaultLang = window.Config ? Config.DEFAULT_LANG : 'en';
        const savedLang = localStorage.getItem('lang') || defaultLang;
        this.currentLang = savedLang;

        // Apply language settings
        document.documentElement.lang = this.currentLang;
        document.documentElement.dir = this.currentLang === 'ar' ? 'rtl' : 'ltr';

        // Update page content
        this.updatePage();
        this.updateToggleButton();

        // Setup language toggle button
        const toggle = document.getElementById('lang-toggle');
        if (toggle) {
            toggle.addEventListener('click', () => this.toggle());
        }
    }
};

// Auto-init when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => i18n.init());
} else {
    i18n.init();
}

window.i18n = i18n;
