document.getElementById('cancelButton').addEventListener('click', function () {
    // Установить значение статуса на "Черновик"
    document.getElementById('statusField').value = 'draft';
    // Отправить форму
    document.getElementById('articleForm').submit();
});