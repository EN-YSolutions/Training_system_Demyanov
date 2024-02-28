import * as api from './api.js';
import * as alert from './alert.js';


document.addEventListener('DOMContentLoaded', () =>
{
    const form = document.querySelector('#form');

    form.addEventListener('submit', event =>
    {
        event.preventDefault();

        const data = new FormData(event.target);
        api.make_request(api.LOGIN, data)
        .then(response => {
            window.location.replace('/users');
        })
        .catch(error => {
            alert.show(error.api? `Ошибка API: ${error.description}` : error.http? `Ошибка HTTP: ${error.code} ${error.text}` : 'Неизвестная ошибка', 10000);
        });
    })
});
