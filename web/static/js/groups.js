document.addEventListener('DOMContentLoaded', () =>
{
    const spinner = document.querySelector('#spinner');
    const empty_warn = document.querySelector('#empty_warn');
    const list = document.querySelector('#list');

    make_request(API_GET_GROUPS)
        .then(result =>
        {
            if (result.length == 0) {
                empty_warn.removeAttribute('style');
                return;
            }

            result.groups.forEach(e => {
                list.append(make_list_item(e));
            });
        })
        .catch(error => {
            make_alert(error.api? `Ошибка API: ${error.description}` : `Ошибка HTTP: ${error.code} ${error.text}`, 10000);
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
    card_header.innerText = e.title;


    const card_body = document.createElement('div');
    card_body.classList.add('card-body');

    card_body.innerHTML = `Курс: <a href="/course?id=${e.course.id}">${e.course.title}</a>`;
    card_body.innerHTML += `<br>Куратор: <a href="/user?id=${e.curator.id}">${e.curator.name}</a>`;
    card_body.innerHTML += `<br>Студентов: ${e.members.length}`;
    card_body.innerHTML += `<br>ID: ${e.id}`;

    const card_footer = document.createElement('div');
    card_footer.classList.add('card-footer');

    const button = document.createElement('button');
    button.classList.add('btn', 'btn-outline-primary');
    button.innerText = 'Выбрать';
    button.addEventListener('click', () => {
        sessionStorage.setItem('selected_group_id', e.id);
    });
    card_footer.append(button);


    card.append(card_header, card_body, card_footer);

    return card;
}
