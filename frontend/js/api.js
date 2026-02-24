/**
 * API Client
 */

const API = {
    /**
     * Make HTTP request to API
     */
    async request(endpoint, options = {}) {
        const url = `${Config.API_BASE_URL}${endpoint}`;
        const token = localStorage.getItem(Config.TOKEN_KEY);

        const headers = {
            'Content-Type': 'application/json',
            ...options.headers
        };

        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }

        try {
            const response = await fetch(url, {
                ...options,
                headers
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || data.message || 'Request failed');
            }

            return { success: true, data };
        } catch (error) {
            console.error('API Error:', error);
            return { success: false, error: error.message };
        }
    },

    /**
     * GET request
     */
    get(endpoint) {
        return this.request(endpoint, { method: 'GET' });
    },

    /**
     * POST request
     */
    post(endpoint, data) {
        return this.request(endpoint, {
            method: 'POST',
            body: JSON.stringify(data)
        });
    },

    /**
     * PUT request
     */
    put(endpoint, data) {
        return this.request(endpoint, {
            method: 'PUT',
            body: JSON.stringify(data)
        });
    },

    /**
     * DELETE request
     */
    delete(endpoint) {
        return this.request(endpoint, { method: 'DELETE' });
    },

    /**
     * Upload file with multipart form data
     */
    async upload(endpoint, file, additionalData = {}) {
        const url = `${Config.API_BASE_URL}${endpoint}`;
        const token = localStorage.getItem(Config.TOKEN_KEY);

        const formData = new FormData();
        formData.append('image', file);

        for (const [key, value] of Object.entries(additionalData)) {
            formData.append(key, value);
        }

        const headers = {};
        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }

        try {
            const response = await fetch(url, {
                method: 'POST',
                headers,
                body: formData
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || 'Upload failed');
            }

            return { success: true, data };
        } catch (error) {
            console.error('Upload Error:', error);
            return { success: false, error: error.message };
        }
    }
};

window.API = API;
