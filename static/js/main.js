window.addEventListener('load', function() {
    const loadingScreen = document.getElementById('loading-screen');
    if (loadingScreen) {
        loadingScreen.classList.add('hidden');
    }
    
    if (typeof AOS !== 'undefined') {
        AOS.init({
            duration: 800,
            once: true,
            offset: 100
        });
    }
});

document.addEventListener('DOMContentLoaded', function() {
    setTimeout(() => {
        const loadingScreen = document.getElementById('loading-screen');
        if (loadingScreen) {
            loadingScreen.classList.add('hidden');
        }
    }, 1500);

    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.classList.remove('show');
            setTimeout(() => alert.remove(), 300);
        }, 5000);
    });
});

function addToCart(accountId) {
    fetch(`/add_to_cart/${accountId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showToast(data.message, 'success');
            setTimeout(() => {
                window.location.reload();
            }, 1000);
        } else {
            showToast(data.message, 'error');
        }
    })
    .catch(error => {
        showToast('Có lỗi xảy ra', 'error');
    });
}

function removeFromCart(itemId) {
    if (!confirm('Bạn có chắc muốn xóa tài khoản này khỏi giỏ hàng?')) {
        return;
    }
    
    fetch(`/remove_from_cart/${itemId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showToast(data.message, 'success');
            setTimeout(() => {
                window.location.reload();
            }, 1000);
        } else {
            showToast(data.message, 'error');
        }
    })
    .catch(error => {
        showToast('Có lỗi xảy ra', 'error');
    });
}

function deleteAccount(accountId) {
    if (!confirm('Bạn có chắc muốn xóa tài khoản này?')) {
        return;
    }
    
    fetch(`/admin/account/delete/${accountId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showToast(data.message, 'success');
            setTimeout(() => {
                window.location.reload();
            }, 1000);
        } else {
            showToast(data.message, 'error');
        }
    })
    .catch(error => {
        showToast('Có lỗi xảy ra', 'error');
    });
}

function updateOrderStatus(orderId, status) {
    fetch(`/admin/order/${orderId}/update_status`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ status: status })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showToast(data.message, 'success');
            setTimeout(() => {
                window.location.reload();
            }, 1000);
        } else {
            showToast(data.message, 'error');
        }
    })
    .catch(error => {
        showToast('Có lỗi xảy ra', 'error');
    });
}

function showToast(message, type) {
    const toast = document.createElement('div');
    toast.className = `modern-toast toast-${type}`;
    
    const icon = type === 'success' ? 'fa-check-circle' : type === 'error' ? 'fa-exclamation-circle' : 'fa-info-circle';
    const iconColor = type === 'success' ? '#28A745' : type === 'error' ? '#DC3545' : '#00D4FF';
    
    toast.innerHTML = `
        <div class="toast-icon" style="color: ${iconColor}">
            <i class="fas ${icon}"></i>
        </div>
        <div class="toast-content">
            <div class="toast-message">${message}</div>
        </div>
        <button class="toast-close" onclick="this.parentElement.remove()">
            <i class="fas fa-times"></i>
        </button>
    `;
    
    document.body.appendChild(toast);
    
    setTimeout(() => {
        toast.classList.add('show');
    }, 100);
    
    setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => toast.remove(), 400);
    }, 4000);
}

function addToWishlist(accountId) {
    fetch(`/wishlist/add/${accountId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showToast(data.message, 'success');
            const heartIcon = document.querySelector(`button[onclick="addToWishlist(${accountId})"] i`);
            if (heartIcon) {
                heartIcon.classList.replace('fa-heart-o', 'fa-heart');
                heartIcon.style.color = '#FF6600';
            }
        } else {
            showToast(data.message, 'error');
        }
    })
    .catch(error => {
        showToast('Có lỗi xảy ra', 'error');
    });
}

function removeFromWishlist(accountId) {
    fetch(`/wishlist/remove/${accountId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showToast(data.message, 'success');
            setTimeout(() => {
                window.location.reload();
            }, 1000);
        } else {
            showToast(data.message, 'error');
        }
    })
    .catch(error => {
        showToast('Có lỗi xảy ra', 'error');
    });
}
