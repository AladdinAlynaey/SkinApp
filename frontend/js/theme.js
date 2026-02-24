/**
 * Theme Manager - Premium Dark/Light Theme Support
 */

const Theme = {
    /**
     * Get current theme
     */
    get() {
        return localStorage.getItem(Config.THEME_KEY) || Config.DEFAULT_THEME;
    },

    /**
     * Set theme
     */
    set(theme) {
        localStorage.setItem(Config.THEME_KEY, theme);
        document.documentElement.setAttribute('data-theme', theme);
        this.updateToggleIcon();

        // Dispatch event for components that need to react
        window.dispatchEvent(new CustomEvent('themechange', { detail: { theme } }));
    },

    /**
     * Toggle between light and dark
     */
    toggle() {
        const current = this.get();
        const newTheme = current === 'light' ? 'dark' : 'light';
        this.set(newTheme);
    },

    /**
     * Update toggle button icon
     */
    updateToggleIcon() {
        const toggle = document.getElementById('theme-toggle');
        if (toggle) {
            const theme = this.get();
            const sunIcon = toggle.querySelector('.icon-sun');
            const moonIcon = toggle.querySelector('.icon-moon');

            if (sunIcon && moonIcon) {
                if (theme === 'dark') {
                    sunIcon.style.display = 'inline';
                    moonIcon.style.display = 'none';
                } else {
                    sunIcon.style.display = 'none';
                    moonIcon.style.display = 'inline';
                }
            }
        }
    },

    /**
     * Initialize theme
     */
    init() {
        // Apply saved theme or default (dark)
        const saved = localStorage.getItem(Config.THEME_KEY);
        if (saved) {
            this.set(saved);
        } else {
            // Default to dark theme
            this.set(Config.DEFAULT_THEME);
        }

        // Setup toggle button
        const toggle = document.getElementById('theme-toggle');
        if (toggle) {
            toggle.addEventListener('click', () => this.toggle());
        }

        this.updateToggleIcon();
    }
};

// Auto-init when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => Theme.init());
} else {
    Theme.init();
}

window.Theme = Theme;
