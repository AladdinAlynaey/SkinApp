/**
 * Main Application
 */

document.addEventListener('DOMContentLoaded', () => {
    // Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', (e) => {
            e.preventDefault();
            const target = document.querySelector(anchor.getAttribute('href'));
            if (target) {
                target.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        });
    });

    // Mobile menu toggle
    const sidebarToggle = document.querySelector('.sidebar-toggle');
    const sidebar = document.querySelector('.sidebar');

    if (sidebarToggle && sidebar) {
        sidebarToggle.addEventListener('click', () => {
            sidebar.classList.toggle('open');
        });
    }
});

/**
 * Toast Notifications
 */
const Toast = {
    container: null,

    init() {
        if (!this.container) {
            this.container = document.createElement('div');
            this.container.className = 'toast-container';
            document.body.appendChild(this.container);
        }
    },

    show(message, type = 'info', duration = 3000) {
        this.init();

        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        toast.innerHTML = `
            <span class="toast-icon">${this.getIcon(type)}</span>
            <span class="toast-message">${message}</span>
        `;

        this.container.appendChild(toast);

        setTimeout(() => {
            toast.style.opacity = '0';
            setTimeout(() => toast.remove(), 300);
        }, duration);
    },

    getIcon(type) {
        const icons = {
            success: '✓',
            error: '✕',
            warning: '⚠',
            info: 'ℹ'
        };
        return icons[type] || icons.info;
    },

    success(msg) { this.show(msg, 'success'); },
    error(msg) { this.show(msg, 'error'); },
    warning(msg) { this.show(msg, 'warning'); },
    info(msg) { this.show(msg, 'info'); }
};

window.Toast = Toast;

/**
 * File Upload Helper
 */
const FileUpload = {
    /**
     * Initialize upload area
     */
    init(selector, options = {}) {
        const area = document.querySelector(selector);
        if (!area) return;

        const input = area.querySelector('input[type="file"]');

        // Click to upload
        area.addEventListener('click', () => input?.click());

        // Drag and drop
        area.addEventListener('dragover', (e) => {
            e.preventDefault();
            area.classList.add('dragging');
        });

        area.addEventListener('dragleave', () => {
            area.classList.remove('dragging');
        });

        area.addEventListener('drop', (e) => {
            e.preventDefault();
            area.classList.remove('dragging');

            const files = e.dataTransfer.files;
            if (files.length && options.onFile) {
                options.onFile(files[0]);
            }
        });

        // File input change
        if (input) {
            input.addEventListener('change', () => {
                if (input.files.length && options.onFile) {
                    options.onFile(input.files[0]);
                }
            });
        }
    }
};

window.FileUpload = FileUpload;
