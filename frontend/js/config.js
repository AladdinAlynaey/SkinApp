/**
 * Configuration - Must be loaded first
 */

const Config = {
    API_BASE_URL: window.location.origin + '/api',
    DEFAULT_LANG: 'en',
    SUPPORTED_LANGS: ['en', 'ar'],
    TOKEN_KEY: 'skin_diagnosis_token',
    USER_KEY: 'skin_diagnosis_user',
    THEME_KEY: 'skin_diagnosis_theme',
    DEFAULT_THEME: 'dark'  // Dark theme is now default
};

// Make it available globally immediately
window.Config = Config;

// Apply theme immediately to prevent flash
(function () {
    const savedTheme = localStorage.getItem(Config.THEME_KEY);
    const theme = savedTheme || Config.DEFAULT_THEME;
    document.documentElement.setAttribute('data-theme', theme);

    // Also apply language direction immediately
    const savedLang = localStorage.getItem('lang') || Config.DEFAULT_LANG;
    document.documentElement.lang = savedLang;
    document.documentElement.dir = savedLang === 'ar' ? 'rtl' : 'ltr';
})();
