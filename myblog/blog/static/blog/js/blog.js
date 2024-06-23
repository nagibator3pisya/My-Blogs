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


const likeButtons = document.querySelectorAll('.like-container');

likeButtons.forEach(button => {
    button.addEventListener('click', event => {
        const articleId = button.dataset.articleId;
        const likeCount = button.querySelector('.like-count');

        const formData = new FormData();
        formData.append('article_id', articleId);

        fetch("/like/", {
            method: "POST",
            headers: {
                "X-CSRFToken": getCSRFToken(),  // Получаем CSRF токен с помощью функции
                "X-Requested-With": "XMLHttpRequest",
            },
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'liked' || data.status === 'unliked') {
                likeCount.textContent = data.like_count;
                button.classList.toggle('active', data.status === 'liked');
            } else {
                console.error('Error:', data.message);
            }
        })
        .catch(error => console.error(error));
    });
});

function getCSRFToken() {
    var cookieValue = null;
    var name = 'csrftoken';
    var cookies = document.cookie.split(';');
    for (var i = 0; i < cookies.length; i++) {
        var cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === (name + '=')) {
            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
            break;
        }
    }
    return cookieValue;
}



