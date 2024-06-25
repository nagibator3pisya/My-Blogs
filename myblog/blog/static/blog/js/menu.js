document.addEventListener('DOMContentLoaded', () => {
    const dropdownMenu = document.getElementById('notificationDropdown');
    const notificationCount = document.getElementById('notificationCount');
    const notificationDropdown = document.getElementById('dropdownNotifications');
    const csrfToken = getCSRFToken();

    console.log('CSRF Token:', csrfToken);

    if (dropdownMenu && notificationCount && notificationDropdown) {
        // Функция для добавления нового уведомления в меню
        function addNotification(notification) {
            const li = document.createElement('li');
            li.classList.add('notification-item');
            li.innerHTML = `
                <a class="dropdown-item ${notification.read ? 'read' : ''}" href="#" data-id="${notification.id}">${notification.message}</a>
            `;
            dropdownMenu.prepend(li); // Добавляем уведомление в начало списка

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
                console.log('Notifications fetched:', data);
                if (data.length > 0) {
                    notificationCount.textContent = data.length;
                    const existingIds = Array.from(dropdownMenu.children).map(item => item.querySelector('a').getAttribute('data-id'));
                    data.forEach(notification => {
                        if (!existingIds.includes(notification.id.toString())) {
                            addNotification(notification);
                        }
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
                    console.log(`Notification ${notificationId} marked as read`);
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
            const notificationItems = dropdownMenu.querySelectorAll('.dropdown-item');
            notificationItems.forEach(item => {
                const notificationId = item.getAttribute('data-id');
                if (readNotifications.includes(notificationId)) {
                    item.classList.add('read');
                }
            });
            updateNotificationCount(); // Обновляем счетчик прочитанных уведомлений
        }

        // Отметить все уведомления как прочитанные
        notificationDropdown.addEventListener('click', () => {
            fetch('/api/notifications/mark-all-read/', {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken
                }
            })
            .then(response => {
                if (response.ok) {
                    console.log('All notifications marked as read');
                    notificationCount.textContent = 0;
                    dropdownMenu.querySelectorAll('.dropdown-item').forEach(item => item.classList.add('read'));
                    localStorage.setItem('readNotifications', JSON.stringify([])); // Очищаем localStorage
                } else {
                    return response.json().then(data => { throw new Error(data.message); });
                }
            })
            .catch(error => console.error('Error marking notifications as read:', error));
        });

        // Обновить счетчик уведомлений
        function updateNotificationCount() {
            const unreadCount = dropdownMenu.querySelectorAll('.dropdown-item:not(.read)').length;
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
//fff