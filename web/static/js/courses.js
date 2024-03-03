import * as api from './api.js';
import * as alert from './alert.js';


document.addEventListener('DOMContentLoaded', () =>
{
    const spinner = document.querySelector('#spinner');
    const empty_warn = document.querySelector('#empty_warn');
    const list = document.querySelector('#list');

    const data = new FormData();
    data.append('depth', 1);

    api.make_request(api.GET_COURSES, data)
        .then(result =>
        {
            if (result.courses.length == 0) {
                empty_warn.removeAttribute('style');
                return;
            }

            result.courses.forEach(e => {
                list.append(make_list_item(e));
            });
        })
        .catch(error => {
            alert.show(error.api? `Ошибка API: ${error.description}` : error.http? `Ошибка HTTP: ${error.code} ${error.text}` : 'Неизвестная ошибка', 10000);
        })
        .finally(() => {
            spinner.setAttribute('style', 'display: none !important;');
        });
});


const make_list_item = (e) =>
{
    const card = document.createElement('div');
    card.classList.add('card', 'my-3');


    const card_header = document.createElement('div');
    card_header.classList.add('card-header');
    card_header.innerHTML = `<a href="/course?id=${e.id}">${e.title}</a>`;


    const card_body = document.createElement('div');
    card_body.classList.add('card-body');

    card_body.innerHTML = `Автор: <a href="/user?id=${e.author.id}">${e.author.name}</a>`;
    card_body.innerHTML += `<br>Цена: ${e.price? e.price : 'бесплатно'}`;
    card_body.innerHTML += `<br>ID: ${e.id}`;


    const card_footer = document.createElement('div');
    card_footer.classList.add('card-footer');

    const button = document.createElement('button');
    button.classList.add('btn', 'btn-outline-primary');
    button.innerText = 'Выбрать';
    button.addEventListener('click', () => {
        sessionStorage.setItem('selected_course_id', e.id);
    });
    card_footer.append(button);


    card.append(card_header, card_body, card_footer);

    return card;
}
