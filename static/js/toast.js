let toastTimeout;

function showToast(title, message, type = 'normal', duration = 3000) {
    const toast = document.getElementById('toast-component');
    const toastTitle = document.getElementById('toast-title');
    const toastMessage = document.getElementById('toast-message');
    const toastIcon = document.getElementById('toast-icon');
    const toastAccent = document.getElementById('toast-accent');
    
    if (!toast) return;

    // Clear existing timeout
    if (toastTimeout) clearTimeout(toastTimeout);

    // Set icon and accent color based on type
    if (type === 'success') {
        toastAccent.className = 'w-2 flex-shrink-0 bg-pink-500';
        toastIcon.innerHTML = `
            <svg class="w-5 h-5 text-pink-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
            </svg>
        `;
    } else if (type === 'error') {
        toastAccent.className = 'w-2 flex-shrink-0 bg-red-500';
        toastIcon.innerHTML = `
            <svg class="w-5 h-5 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
            </svg>
        `;
    } else {
        toastAccent.className = 'w-2 flex-shrink-0 bg-blue-500';
        toastIcon.innerHTML = `
            <svg class="w-5 h-5 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
            </svg>
        `;
    }

    // Set content - if title is empty, use type as title
    if (!title || title.trim() === '') {
        if (type === 'success') {
            toastTitle.textContent = 'Success';
        } else if (type === 'error') {
            toastTitle.textContent = 'Error';
        } else {
            toastTitle.textContent = 'Info';
        }
    } else {
        toastTitle.textContent = title;
    }
    
    toastMessage.textContent = message;

    // Show toast
    toast.classList.remove('opacity-0', 'translate-y-20');
    toast.classList.add('opacity-100', 'translate-y-0');

    // Auto hide
    toastTimeout = setTimeout(() => {
        hideToast();
    }, duration);
}

function hideToast() {
    const toast = document.getElementById('toast-component');
    if (!toast) return;

    toast.classList.remove('opacity-100', 'translate-y-0');
    toast.classList.add('opacity-0', 'translate-y-20');

    if (toastTimeout) clearTimeout(toastTimeout);
}