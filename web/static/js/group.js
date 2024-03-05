import * as api from './api.js'
import * as alert from './alert.js';


document.addEventListener('DOMContentLoaded', () =>
{
    const spinner = document.getElementById('spinner');

    const params = new URLSearchParams(window.location.search);


    // Карточка #1. Информация о группе
    const group = document.getElementById('group');
    const group_title = document.getElementById('group_title');
    const group_curator_name = document.getElementById('group_curator_name');
    const group_course_title = document.getElementById('group_course_title');
    const group_id = document.getElementById('group_id');

    let data = new FormData();
    data.append('id', params.get('id'));
    data.append('depth', 1);

    api.make_request(api.GET_GROUP, data)
    .then(result =>
    {
        group.dataset.eduHide = false;

        group_title.innerText = result.group.title;
        group_curator_name.innerHTML = `<a href="/user?id=${result.group.curator.id}">${result.group.curator.name}</a>`;
        group_course_title.innerHTML = `<a href="/course?id=${result.group.course.id}">${result.group.course.title}</a>`;
        group_id.innerText = result.group.id;
    })
    .catch(error => {
        alert.show(error.api? `Ошибка API: ${error.description}` : error.http? `Ошибка HTTP: ${error.code} ${error.text}` : 'Неизвестная ошибка', 10000);
    })
    .finally(() => {
        spinner.dataset.eduHide = true;
    });


    // Карточка #2. Участники группы
    const members = document.getElementById('members');
    const members_empty = document.getElementById('members_empty');
    const members_form = document.getElementById('members_form');
    const members_form_user_id = document.getElementById('members_form_user_id');
    const members_table = document.getElementById('members_table');
    const members_table_body = document.getElementById('members_table_body');

    const members_on_delete = () =>
    {
        if (members_table_body.childElementCount == 0) {
            members_table.dataset.eduHide = true;
            members_empty.dataset.eduHide = false;
        }
    }

    data = new FormData();
    data.append('id', params.get('id'));

    api.make_request(api.GET_GROUP_MEMBERS, data)
    .then(result =>
    {
        members.dataset.eduHide = false;

        if (result.users.length == 0) {
            members_empty.dataset.eduHide = false;
            return;
        }

        members_table.dataset.eduHide = false;

        result.users.forEach(e => {
            members_table_body.append(make_members_list_item(e, params.get('id'), members_on_delete));
        });
    })
    .catch(error => {
        alert.show(error.api? `Ошибка API: ${error.description}` : error.http? `Ошибка HTTP: ${error.code} ${error.text}` : 'Неизвестная ошибка', 10000);
    });


    // Форма добавление участника группы
    members_form_user_id.value = sessionStorage.getItem('selected_user_id');

    members_form.addEventListener('submit', event =>
    {
        event.preventDefault();

        const data = new FormData(event.target);
        data.append('group_id', params.get('id'));

        api.make_request(api.ADD_GROUP_MEMBER, data)
        .then(result =>
        {
            members_empty.dataset.eduHide = true;
            members_table.dataset.eduHide = false;

            members_table_body.append(make_members_list_item(result.user, params.get('id'), members_on_delete));
        })
        .catch(error => {
            alert.show(error.api? `Ошибка API: ${error.description}` : error.http? `Ошибка HTTP: ${error.code} ${error.text}` : 'Неизвестная ошибка', 10000);
        });
    });
});


const make_members_list_item = (e, group_id, on_delete) =>
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

    tr.append(td_user_name, td_user_login, td_delete);

    return tr;
}
