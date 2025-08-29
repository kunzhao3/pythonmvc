// 删除确认功能
function confirmDelete() {
    return confirm('确定要删除该商品吗？');
}
// 自动提交数量更新表单
document.querySelectorAll('.quantity-input').forEach(input => {
    input.addEventListener('change', function() {
        this.closest('form').submit();
    });
});

document.querySelectorAll('.quantity-input').forEach(input => {
    input.addEventListener('active', function() {
        this.closest('form').submit();
    });
});