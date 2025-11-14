// ==================== UTILITY FUNCTIONS ====================

// Auto-hide alerts after 5 seconds
document.addEventListener('DOMContentLoaded', function() {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.transition = 'opacity 0.3s ease';
            alert.style.opacity = '0';
            setTimeout(() => {
                alert.remove();
            }, 300);
        }, 5000);
    });
});

// Confirmation dialog for return book
function confirmReturn() {
    return confirm('Are you sure you want to return this book?');
}

// Confirmation dialog for borrow book
function confirmBorrow() {
    return confirm('Borrow this book for 14 days?');
}

// Form validation
function validateForm() {
    const username = document.getElementById('username')?.value.trim();
    const password = document.getElementById('password')?.value.trim();
    
    if (!username || !password) {
        alert('Please fill in all required fields');
        return false;
    }
    
    return true;
}

// Toggle password visibility
function togglePasswordVisibility(inputId) {
    const input = document.getElementById(inputId);
    if (input) {
        input.type = input.type === 'password' ? 'text' : 'password';
    }
}

// Format date
function formatDate(dateString) {
    const options = { year: 'numeric', month: 'short', day: 'numeric' };
    return new Date(dateString).toLocaleDateString('en-US', options);
}

// Search functionality with debounce
let searchTimeout;
const searchInput = document.getElementById('search');
if (searchInput) {
    searchInput.addEventListener('input', function() {
        clearTimeout(searchTimeout);
        searchTimeout = setTimeout(() => {
            // Auto-submit could be added here
        }, 500);
    });
}

// ==================== TABLE SORTING ====================
function sortTable(columnIndex) {
    const table = document.querySelector('.books-table');
    const tbody = table.querySelector('tbody');
    const rows = Array.from(tbody.querySelectorAll('tr'));
    
    rows.sort((a, b) => {
        const aValue = a.cells[columnIndex].textContent.trim();
        const bValue = b.cells[columnIndex].textContent.trim();
        
        // Try numeric sort first
        const aNum = parseFloat(aValue);
        const bNum = parseFloat(bValue);
        
        if (!isNaN(aNum) && !isNaN(bNum)) {
            return aNum - bNum;
        }
        
        // Fall back to string sort
        return aValue.localeCompare(bValue);
    });
    
    rows.forEach(row => tbody.appendChild(row));
}

// ==================== THEME SWITCHER ====================
function initThemeSwitcher() {
    const savedTheme = localStorage.getItem('theme') || 'light';
    document.documentElement.setAttribute('data-theme', savedTheme);
}

// ==================== NOTIFICATION SYSTEM ====================
function showNotification(message, type = 'info', duration = 3000) {
    const notification = document.createElement('div');
    notification.className = `alert alert-${type}`;
    notification.textContent = message;
    
    const container = document.querySelector('.container') || document.body;
    container.insertBefore(notification, container.firstChild);
    
    setTimeout(() => {
        notification.remove();
    }, duration);
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    initThemeSwitcher();
    console.log('Library Management System loaded successfully');
    initBookModal();
});


// ==================== BOOK DETAIL MODAL ====================
function initBookModal() {
    const modal = document.getElementById('book-modal');
    if (!modal) return;

    const modalClose = modal.querySelector('.modal-close');
    const overlay = modal.querySelector('.modal-overlay');

    function openModal(card) {
        modal.setAttribute('aria-hidden', 'false');
        const title = card.dataset.title;
        const author = card.dataset.author;
        const isbn = card.dataset.isbn;
        const year = card.dataset.year;
        const description = card.dataset.description || '';
        const image = card.dataset.image;
        const available = card.dataset.availableCount;
        const quantity = card.dataset.quantity;

        document.getElementById('modal-title').textContent = title;
        document.getElementById('modal-author').textContent = 'Author: ' + author;
        document.getElementById('modal-isbn').textContent = 'ISBN: ' + isbn;
        document.getElementById('modal-year').textContent = 'Year: ' + year;
        document.getElementById('modal-available-count').textContent = available + ' / ' + quantity;
        document.getElementById('modal-description').textContent = description;
        document.getElementById('modal-cover').src = image;

        // Show borrow button inside modal if available
        const actions = document.getElementById('modal-actions');
        actions.innerHTML = '';
        if (parseInt(available) > 0) {
            const borrowBtn = document.createElement('button');
            borrowBtn.className = 'btn btn-primary';
            borrowBtn.textContent = 'Borrow Book';
            borrowBtn.onclick = function() {
                // Find form on card and submit it if exists
                const form = card.querySelector('form');
                if (form) form.submit();
            };
            actions.appendChild(borrowBtn);
        } else {
            const span = document.createElement('span');
            span.className = 'text-muted';
            span.textContent = 'No copies available';
            actions.appendChild(span);
        }

        document.body.classList.add('modal-open');
    }

    function closeModal() {
        modal.setAttribute('aria-hidden', 'true');
        document.body.classList.remove('modal-open');
    }

    modalClose.addEventListener('click', closeModal);
    overlay.addEventListener('click', closeModal);

    // Open modal when clicking a book card or its cover
    document.querySelectorAll('.book-card').forEach(card => {
        card.addEventListener('click', function(e) {
            // Prevent opening modal when clicking on the borrow button inside card
            if (e.target.closest('form') || e.target.classList.contains('btn')) return;
            openModal(card);
        });
        // Also open on Enter key when focused
        card.querySelectorAll('.book-cover').forEach(img => {
            img.addEventListener('keydown', function(e) {
                if (e.key === 'Enter') openModal(card);
            });
        });
    });
}
