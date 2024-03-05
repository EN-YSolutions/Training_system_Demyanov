import * as api from './api.js';
import * as alert from './alert.js';


document.addEventListener('DOMContentLoaded', () =>
{
    const spinner = document.getElementById('spinner');

    const params = new URLSearchParams(window.location.search);


    // Карточка #1. Информация о пользователе
    const user = document.getElementById('user');
    const user_name = document.getElementById('user_name');
    const user_login = document.getElementById('user_login');
    const user_role = document.getElementById('user_role');
    const user_balance = document.getElementById('user_balance');
    const user_scoring_system = document.getElementById('user_scoring_system');
    const user_id = document.getElementById('user_id');

    let data = new FormData();
    data.append('id', params.get('id'));

    api.make_request(api.GET_USER, data)
    .then(result =>
    {
        user.dataset.eduHide = false;

        user_name.innerText = result.user.name;
        user_login.innerText = result.user.login;
        user_role.innerText = result.user.role == 'student'? 'студент' : result.user.role == 'teacher'? 'преподаватель' : result.user.role == 'curator'? 'куратор' : result.user.role == 'admin'? 'администратор' : 'неизвестно'

        if (result.user.balance)
            user_balance.innerText = result.user.balance;
        else
            user_balance.parentElement.dataset.eduHide = true;

        if (result.user.scoring_system)
            user_scoring_system.innerText = result.user.scoring_system;
        else
            user_scoring_system.parentElement.dataset.eduHide = true;

        user_id.innerText = result.user.id;
    })
    .catch(error => {
        alert.show(error.api? `Ошибка API: ${error.description}` : error.http? `Ошибка HTTP: ${error.code} ${error.text}` : 'Неизвестная ошибка', 10000);
        user.dataset.eduHide = true;
    })
    .finally(() => {
        spinner.setAttribute('style', 'display: none !important;');
    });


    // Карточка #2. Группы, в которых состоит пользователь
    const groups = document.getElementById('groups');
    const groups_empty = document.getElementById('groups_empty');
    const groups_table = document.getElementById('groups_table');
    const groups_table_body = document.getElementById('groups_table_body');

    data = new FormData();
    data.append('id', params.get('id'));
    data.append('depth', 1);

    api.make_request(api.GET_USER_GROUPS, data)
    .then(result =>
    {
        groups.dataset.eduHide = false;

        if (result.groups.length == 0) {
            groups_empty.dataset.eduHide = false;
            return;
        }

        groups_table.dataset.eduHide = false;

        result.groups.forEach(e =>
        {
            groups_table_body.append(make_group_list_item(e, params.get('id'), () => {
                if (groups_table_body.childElementCount == 0) {
                    groups_table.dataset.eduHide = true;
                    groups_empty.dataset.eduHide = false;
                }
            }));
        });
    })
    .catch(error => {
        alert.show(error.api? `Ошибка API: ${error.description}` : error.http? `Ошибка HTTP: ${error.code} ${error.text}` : 'Неизвестная ошибка', 10000);
        groups.dataset.eduHide = true;
    });
});


const make_group_list_item = (e, user_id, on_delete) =>
{
    const tr = document.createElement('tr');

    const td_group = document.createElement('td');
    td_group.innerHTML = `<a href="/group?id=${e.id}">${e.title}</a>`;

    const td_course = document.createElement('td');
    td_course.innerHTML = `<a href="/course?id=${e.course.id}">${e.course.title}</a>`;

    const td_delete = document.createElement('td');

    const delete_button = document.createElement('button');
    delete_button.classList.add('btn', 'btn-outline-danger');
    delete_button.innerText = 'Удалить';
    delete_button.addEventListener('click', event =>
    {
        const data = new FormData();
        data.append('group_id', e.id);
        data.append('user_id', user_id);

        api.make_request(api.DELETE_GROUP_MEMBER, data)
        .then(result => {
            tr.remove();
            on_delete();
        })
        .catch(error => {
            alert.show(error.api? `Ошибка API: ${error.description}` : error.http? `Ошибка HTTP: ${error.code} ${error.text}` : 'Неизвестная ошибка', 10000);
        });
    });

    td_delete.append(delete_button);

    tr.append(td_group, td_course, td_delete);

    return tr;
};
