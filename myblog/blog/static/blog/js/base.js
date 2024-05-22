

document.getElementById('accept-cookies').addEventListener('click', function () {
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/accept-cookies/');
    xhr.setRequestHeader('X-CSRFToken', getCSRFToken());
    xhr.onload = function () {
        if (xhr.status === 200) {
            document.querySelector('.wrapper').classList.add('hide');
        }
    };
    xhr.send();
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



// форма 
$(document).ready(function () {
    // Обработка отправки формы
    $("#RegisterForm").on("submit", function (e) {
        e.preventDefault();

        // Сброс состояния валидации
        let form = this;
        let isValid = true;
        $(form).addClass('was-validated');

        // Проверка каждого поля формы
        $(form).find('input[required]').each(function () {
            if (!this.checkValidity()) {
                isValid = false;
                $(this).addClass('is-invalid').removeClass('is-valid');
            } else {
                $(this).addClass('is-valid').removeClass('is-invalid');
            }
        });

        // Проверка паролей на совпадение
        let password = $('#registerPassword').val();
        let confirmPassword = $('#confirmPassword').val();
        if (password !== confirmPassword || password === '') {
            isValid = false;
            $('#confirmPassword').addClass('is-invalid').removeClass('is-valid');
        } else {
            $('#confirmPassword').addClass('is-valid').removeClass('is-invalid');
        }

        // Если форма валидна, выполнить регистрацию
        if (isValid) {
            alert("Форма отправлена успешно!");
            form.submit(); // или заменить на ajax-запрос
        }
    });

    // Обработка снятия фокуса с полей
    $('input[required]').on('blur', function () {
        if (!this.checkValidity()) {
            $(this).addClass('is-invalid').removeClass('is-valid');
        } else {
            $(this).addClass('is-valid').removeClass('is-invalid');
        }
    });

    // Активация кнопки только при заполнении всех полей
    $('input').on('input', function () {
        let allFilled = true;
        $('#RegisterForm').find('input[required]').each(function () {
            if ($(this).val() === '') {
                allFilled = false;
            }
        });

        if (allFilled) {
            $('.btn-registration-button').prop('disabled', false);
        } else {
            $('.btn-registration-button').prop('disabled', true);
        }
    });
});


// форма

document.addEventListener("DOMContentLoaded", function () {
    var showModalLinks = document.querySelectorAll('.show-registration-modal');

    showModalLinks.forEach(function (link) {
        link.addEventListener('click', function (event) {
            event.preventDefault();
            var modal = new bootstrap.Modal(document.getElementById('registrationModal'));
            modal.show();
        });
    });
});


    document.addEventListener('DOMContentLoaded', function() {
        // Проверяем, существует ли сообщение об успешной смене пароля в localStorage
        var successMessage = localStorage.getItem('success_password_change');
        if (successMessage) {
            // Показываем модальное окно
            var successModal = new bootstrap.Modal(document.getElementById('successModal'));
            successModal.show();
            // Удаляем сообщение об успешной смене пароля из localStorage
            localStorage.removeItem('success_password_change');
        }
    });

