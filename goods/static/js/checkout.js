// 支付按钮点击事件
document.querySelector('.checkout-btn').addEventListener('click', function() {
    if (confirm('确认支付吗？')) {
        window.location.href = '/system/cart/order_confirmation';
    }
});

// 自动提交数量更新表单
document.querySelectorAll('.quantity-input').forEach(input => {
    input.addEventListener('change', function() {
        this.closest('form').submit();
    });
});