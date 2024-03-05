import * as api from './api.js';
import * as alert from './alert.js';


document.addEventListener('DOMContentLoaded', () =>
{
    const spinner = document.getElementById('spinner');
    const empty_warn = document.getElementById('empty_warn');
    const list = document.getElementById('list');

    const data = new FormData();
    data.append('depth', 1);

    api.make_request(api.GET_GROUPS, data)
    .then(result =>
    {
        if (result.entries.length == 0) {
            empty_warn.dataset.eduHide = false;
            return;
        }

        result.entries.forEach(e => {
            list.append(make_list_item(e));
        });
    })
    .catch(error => {
        alert.show(error.api? `Ошибка API: ${error.description}` : error.http? `Ошибка HTTP: ${error.code} ${error.text}` : 'Неизвестная ошибка', 10000);
    })
    .finally(() => {
        spinner.dataset.eduHide = true;
    });
});


const make_list_item = (e) =>
{
    console.log(e);

    const card = document.createElement('div');
    card.classList.add('card', 'my-3');


    const card_header = document.createElement('div');
    card_header.classList.add('card-header');
    card_header.innerHTML = `<a href="/group?id=${e.group.id}">${e.group.title}</a>`;


    const card_body = document.createElement('div');
    card_body.classList.add('card-body');

    card_body.innerHTML = `Курс: <a href="/course?id=${e.group.course.id}">${e.group.course.title}</a>`;
    card_body.innerHTML += `<br>Куратор: <a href="/user?id=${e.group.curator.id}">${e.group.curator.name}</a>`;
    card_body.innerHTML += `<br>Студентов: ${e.members}`;
    card_body.innerHTML += `<br>ID: ${e.group.id}`;


    const card_footer = document.createElement('div');
    card_footer.classList.add('card-footer');

    const button = document.createElement('button');
    button.classList.add('btn', 'btn-outline-primary');
    button.innerText = 'Выбрать';
    button.addEventListener('click', () => {
        sessionStorage.setItem('selected_group_id', e.group.id);
    });
    card_footer.append(button);


    card.append(card_header, card_body, card_footer);

    return card;
}
