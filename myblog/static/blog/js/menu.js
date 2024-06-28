document.addEventListener('DOMContentLoaded', () => {
    const dropdownMenu = document.getElementById('notificationDropdown');
    const notificationCount = document.getElementById('notificationCount');
    const csrfToken = getCSRFToken();

    if (dropdownMenu && notificationCount) {
        // Функция для добавления нового уведомления в меню
        function addNotification(notification) {
            const li = document.createElement('li');
            li.classList.add('notification-item');
            li.innerHTML = `
                <a class="dropdown-item  ${notification.read ? 'read' : ''}" href="#" data-id="${notification.id}">${notification.message}</a>
            `;
            dropdownMenu.insertBefore(li, dropdownMenu.lastElementChild); // Добавляем уведомление перед кнопкой "Показать больше"

            // Добавляем обработчик клика для отметки уведомления как прочитанного
            li.querySelector('a').addEventListener('click', function (event) {
                event.preventDefault();
                const notificationId = this.getAttribute('data-id');
                markNotificationAsRead(notificationId, this);
            });
        }

        // Получение уведомлений через AJAX
        function fetchNotifications() {
            fetch('/api/notifications/', {
                headers: {
                    'X-CSRFToken': csrfToken // Вставляем CSRF-токен в заголовок запроса
                }
            })
            .then(response => {
                if (response.ok) {
                    return response.json();
                } else {
                    throw new Error('Network response was not ok');
                }
            })
            .then(data => {
                if (data.length > 0) {
                    const notificationsToShow = data.slice(0, 5); // Отображаем только первые 5 уведомлений
                    notificationCount.textContent = notificationsToShow.length;
                    notificationsToShow.forEach(notification => {
                        addNotification(notification);
                    });
                } else {
                    notificationCount.textContent = 0;
                }
                restoreReadNotifications(); // Восстанавливаем состояние прочитанных уведомлений
            })
            .catch(error => console.error('Error fetching notifications:', error));
        }

        // Отметить уведомление как прочитанное
        function markNotificationAsRead(notificationId, element) {
            fetch(`/api/notifications/${notificationId}/mark-read/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken
                }
            })
            .then(response => {
                if (response.ok) {
                    element.classList.add('read');
                    updateNotificationCount();
                    saveReadNotification(notificationId); // Сохраняем прочитанное уведомление в localStorage
                } else {
                    return response.json().then(data => { throw new Error(data.message); });
                }
            })
            .catch(error => console.error('Error marking notification as read:', error));
        }

        // Сохраняем прочитанное уведомление в localStorage
        function saveReadNotification(notificationId) {
            const readNotifications = JSON.parse(localStorage.getItem('readNotifications')) || [];
            if (!readNotifications.includes(notificationId)) {
                readNotifications.push(notificationId);
                localStorage.setItem('readNotifications', JSON.stringify(readNotifications));
            }
        }

        // Восстанавливаем состояние прочитанных уведомлений из localStorage
        function restoreReadNotifications() {
            const readNotifications = JSON.parse(localStorage.getItem('readNotifications')) || [];
            const notificationItems = dropdownMenu.querySelectorAll('.notification-item .dropdown-item');
            notificationItems.forEach(item => {
                const notificationId = item.getAttribute('data-id');
                if (readNotifications.includes(notificationId)) {
                    item.classList.add('read');
                }
            });
            updateNotificationCount(); // Обновляем счетчик прочитанных уведомлений
        }

        // Обновить счетчик уведомлений
        function updateNotificationCount() {
            const unreadCount = dropdownMenu.querySelectorAll('.notification-item .dropdown-item:not(.read)').length;
            notificationCount.textContent = unreadCount;
        }

        // Вызываем функцию для получения уведомлений при загрузке страницы
        fetchNotifications();
    } else {
        console.error('One or more required elements not found.');
    }

    // Функция для получения CSRF-токена из куки
    function getCSRFToken() {
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            const [name, value] = cookie.split('=');
            if (name.trim() === 'csrftoken') {
                return decodeURIComponent(value);
            }
        }
        return '';
    }
});
