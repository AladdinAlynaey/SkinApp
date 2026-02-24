/**
 * Authentication Module
 */

const Auth = {
    /**
     * Register new user
     */
    async register(userType, data) {
        const endpoint = userType === 'patient'
            ? '/auth/register/patient'
            : '/auth/register/doctor';

        return await API.post(endpoint, data);
    },

    /**
     * Login user
     */
    async login(email, password, userType) {
        const result = await API.post('/auth/login', { email, password, user_type: userType });

        if (result.success && result.data.token) {
            localStorage.setItem(Config.TOKEN_KEY, result.data.token);
            localStorage.setItem(Config.USER_KEY, JSON.stringify({
                ...result.data.user,
                user_type: userType
            }));
        }

        return result;
    },

    /**
     * Logout user
     */
    logout() {
        localStorage.removeItem(Config.TOKEN_KEY);
        localStorage.removeItem(Config.USER_KEY);
        window.location.href = '/login.html';
    },

    /**
     * Get current user
     */
    getUser() {
        const user = localStorage.getItem(Config.USER_KEY);
        return user ? JSON.parse(user) : null;
    },

    /**
     * Check if logged in
     */
    isLoggedIn() {
        return !!localStorage.getItem(Config.TOKEN_KEY);
    },

    /**
     * Get user type
     */
    getUserType() {
        const user = this.getUser();
        return user ? user.user_type : null;
    },

    /**
     * Require authentication (redirect if not logged in)
     */
    requireAuth(allowedTypes = null) {
        if (!this.isLoggedIn()) {
            window.location.href = '/login.html';
            return false;
        }

        if (allowedTypes && !allowedTypes.includes(this.getUserType())) {
            window.location.href = '/login.html';
            return false;
        }

        return true;
    },

    /**
     * Request password reset
     */
    async requestPasswordReset(email, userType) {
        return await API.post('/auth/recover', { email, user_type: userType });
    }
};

window.Auth = Auth;
