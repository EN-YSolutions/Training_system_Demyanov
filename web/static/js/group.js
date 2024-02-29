import * as api from './api.js'
import * as alert from './alert.js';


document.addEventListener('DOMContentLoaded', () =>
{
    const spinner = document.querySelector('#spinner');
    const empty_warn = document.querySelector('#empty_warn');

    const group = document.querySelector('#group');

    const group_title = document.querySelector('#group_title');
    const group_curator_name = document.querySelector('#group_curator_name');
    const group_course_title = document.querySelector('#group_course_title');
    const group_id = document.querySelector('#group_id');

    const params = new URLSearchParams(window.location.search);


    let data = new FormData();
    data.append('id', params.get('id'));
    data.append('depth', 1);

    api.make_request(api.GET_GROUP, data)
    .then(result =>
    {
        group.removeAttribute('style');

        group_title.innerText = result.group.title;
        group_curator_name.innerHTML = `<a href="/user?id=${result.group.curator.id}">${result.group.curator.name}</a>`;
        group_course_title.innerHTML = `<a href="/course?id=${result.group.course.id}">${result.group.course.title}</a>`;
        group_id.innerText = result.group.id;
    })
    .catch(error => {
        alert.show(error.api? `Ошибка API: ${error.description}` : error.http? `Ошибка HTTP: ${error.code} ${error.text}` : 'Неизвестная ошибка', 10000);
        group.setAttribute('style', 'display: none !important');
    })
    .finally(() => {
        spinner.setAttribute('style', 'display: none !important;');
    });


    const group_members = document.querySelector('#group_members');

    const group_members_empty = document.querySelector('#group_members_empty');
    const group_members_table = document.querySelector('#group_members_table');
    const group_members_table_body = document.querySelector('#group_members_table_body');

    data = new FormData();
    data.append('id', params.get('id'));

    api.make_request(api.GET_GROUP_MEMBERS, data)
    .then(result =>
    {
        group_members.removeAttribute('style');

        if (result.users.length == 0) {
            group_members_empty.removeAttribute('style');
            return;
        }

        group_members_table.removeAttribute('style');

        result.users.forEach(e => {
            group_members_table_body.append(make_members_list_item(e, params.get('id')));
        });
    })
    .catch(error => {
        alert.show(error.api? `Ошибка API: ${error.description}` : error.http? `Ошибка HTTP: ${error.code} ${error.text}` : 'Неизвестная ошибка', 10000);
        group_members.setAttribute('style', 'display: none !important');
    });
});


const make_members_list_item = (e, group_id) =>
{
    const tr = document.createElement('tr');

    const td_user_name = document.createElement('td');
    td_user_name.innerText = e.name;

    const td_user_login = document.createElement('td');
    td_user_login.innerText = e.login;

    const td_delete = document.createElement('td');

    const delete_button = document.createElement('button');
    delete_button.classList.add('btn', 'btn-outline-danger');
    delete_button.innerText = 'Удалить';
    delete_button.addEventListener('click', event =>
    {
        const data = new FormData();
        data.append('user_id', e.id);
        data.append('group_id', group_id);

        api.make_request(api.DELETE_USER_GROUP, data)
        .then(result => {
            tr.remove();
        })
        .catch(error => {
            alert.show(error.api? `Ошибка API: ${error.description}` : error.http? `Ошибка HTTP: ${error.code} ${error.text}` : 'Неизвестная ошибка', 10000);
        });
    });

    td_delete.append(delete_button);

    tr.append(td_user_name, td_user_login, td_delete);

    return tr;
}
