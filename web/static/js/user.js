import * as api from './api.js';
import * as alert from './alert.js';


document.addEventListener('DOMContentLoaded', () =>
{
    const spinner = document.querySelector('#spinner');
    const empty_warn = document.querySelector('#empty_warn');

    const user = document.querySelector('#user');

    const user_name = document.querySelector('#user_name');
    const user_login = document.querySelector('#user_login');
    const user_role = document.querySelector('#user_role');
    const user_balance = document.querySelector('#user_balance');
    const user_scoring_system = document.querySelector('#user_scoring_system');
    const user_id = document.querySelector('#user_id');

    const params = new URLSearchParams(window.location.search);


    let data = new FormData();
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
        user.setAttribute('style', 'display: none !important');
    })
    .finally(() => {
        spinner.setAttribute('style', 'display: none !important;');
    });


    const user_groups = document.querySelector('#user_groups');

    const user_groups_empty = document.querySelector('#user_groups_empty');
    const user_groups_table = document.querySelector('#user_groups_table');
    const user_groups_table_body = document.querySelector('#user_groups_table_body');

    data = new FormData();
    data.append('id', params.get('id'));
    data.append('depth', 1);

    api.make_request(api.GET_USER_GROUPS, data)
    .then(result =>
    {
        user_groups.removeAttribute('style');

        if (result.groups.length == 0) {
            user_groups_empty.removeAttribute('style');
            return;
        }

        user_groups_table.removeAttribute('style');

        result.groups.forEach(e =>
        {
            user_groups_table_body.append(make_group_list_item(e, params.get('id'), () => {
                if (user_groups_table_body.childElementCount == 0) {
                    user_groups_table.setAttribute('style', 'display: none !important');
                    user_groups_empty.removeAttribute('style');
                }
            }));
        });
    })
    .catch(error => {
        alert.show(error.api? `Ошибка API: ${error.description}` : error.http? `Ошибка HTTP: ${error.code} ${error.text}` : 'Неизвестная ошибка', 10000);
        user_groups.setAttribute('style', 'display: none !important');
    });
});


const make_group_list_item = (e, user_id, on_delete) =>
{
    const tr = document.createElement('tr');

    const td_group = document.createElement('td');
    td_group.innerText = e.title;

    const td_course = document.createElement('td');
    td_course.innerText = e.course.title;

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
