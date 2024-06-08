document.addEventListener('DOMContentLoaded', function () {
    var deleteModal = document.getElementById('deleteModal');
    var confirmDeleteButton = document.getElementById('confirmDeleteButton');
    var articleId;

    deleteModal.addEventListener('show.bs.modal', function (event) {
        var button = event.relatedTarget; // Кнопка, которая открыла модальное окно
        articleId = button.getAttribute('data-article-id'); // Получение ID статьи из data-атрибута
    });

    confirmDeleteButton.addEventListener('click', function () {
        var csrfTokenElement = document.querySelector('[name=csrfmiddlewaretoken]');
        if (!csrfTokenElement) {
            console.error('CSRF token not found');
            return;
        }
        var csrfToken = csrfTokenElement.value;

        fetch(`/articles/${articleId}/delete/`, {
            method: 'DELETE',
            headers: {
                'X-CSRFToken': csrfToken,
                'Content-Type': 'application/json'
            }
        })
        .then(response => {
            if (response.ok) {
                // Успешное удаление, скрыть модальное окно и удалить карточку
                deleteModal.querySelector('.btn-close').click();
                document.querySelector(`[data-article-id="${articleId}"]`).closest('.card').remove();
            } else {
                // Обработка ошибок
                alert('Ошибка при удалении статьи.');
            }
        });
    });
});
