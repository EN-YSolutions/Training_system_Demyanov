document.addEventListener('DOMContentLoaded', () =>
{
    const spinner = document.querySelector('#spinner');
    const empty_warn = document.querySelector('#empty_warn');
    const list = document.querySelector('#list');

    make_request(API_GET_USERS)
        .then(result =>
        {
            if (result.length == 0) {
                empty_warn.removeAttribute('style');
                return;
            }

            result.users.forEach(e => {
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
    card.classList.add('card', 'mt-3');


    const card_header = document.createElement('div');
    card_header.classList.add('card-header');
    card_header.innerText = e.name;


    const card_body = document.createElement('div');
    card_body.classList.add('card-body');
    card_body.innerHTML = `Логин: ${e.login}`;
    card_body.innerHTML += `<br>Роль: ${e.role == 'student'? 'студент' : e.role == 'teacher'? 'преподаватель' : e.role == 'curator'? 'куратор' : e.role == 'admin'? 'администратор' : 'неизвестно'}`;
    if (e.balance)
        card_body.innerHTML += `<br>Баланс: ${e.balance}`;
    if (e.scoring_system)
        card_body.innerHTML += `<br>Система оценивания: ${e.scoring_system}`;
    card_body.innerHTML += `<br>ID: ${e.id}`;


    const card_footer = document.createElement('div');
    card_footer.classList.add('card-footer');

    const button = document.createElement('button');
    button.classList.add('btn', 'btn-outline-primary');
    button.innerText = 'Выбрать';
    button.addEventListener('click', () => {
        sessionStorage.setItem('selected_user_id', e.id);
    });
    card_footer.append(button);


    card.append(card_header, card_body, card_footer);

    return card;
}
