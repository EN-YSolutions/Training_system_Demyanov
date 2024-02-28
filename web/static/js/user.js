import * as api from './api.js';
import * as alert from './alert.js';


document.addEventListener('DOMContentLoaded', () =>
{
    const spinner = document.querySelector('#spinner');
    const empty_warn = document.querySelector('#empty_warn');
    const list = document.querySelector('#user');

    const user = document.querySelector('#user');
    const user_name = document.querySelector('#user_name');
    const user_login = document.querySelector('#user_login');
    const user_role = document.querySelector('#user_role');
    const user_balance = document.querySelector('#user_balance');
    const user_scoring_system = document.querySelector('#user_scoring_system');
    const user_id = document.querySelector('#user_id');

    const params = new URLSearchParams(window.location.search);
    const data = new FormData();
    data.append('id', params.get('id'));

    api.make_request(api.GET_USER, data)
        .then(result =>
        {
            user.removeAttribute('style');
            user_name.innerText = result.user.name;
            user_login.innerText = result.user.login;
            user_role.innerText = result.user.role == 'student'? 'студент' : result.user.role == 'teacher'? 'преподаватель' : result.user.role == 'curator'? 'куратор' : result.user.role == 'admin'? 'администратор' : 'неизвестно'

            if (result.user.balance)
                user_balance.innerText = result.user.balance;
            else
                user_balance.parentElement.setAttribute('style', 'display: none !important');

            if (result.user.scoring_system)
                user_scoring_system.innerText = result.user.scoring_system;
            else
                user_scoring_system.parentElement.setAttribute('style', 'display : none !important');

            user_id.innerText = result.user.id;
        })
        .catch(error => {
            alert.show(error.api? `Ошибка API: ${error.description}` : error.http? `Ошибка HTTP: ${error.code} ${error.text}` : 'Неизвестная ошибка', 10000);
        })
        .finally(() => {
            spinner.setAttribute('style', 'display: none !important;');
        });
});
