import 'https://cdn.jsdelivr.net/npm/dompurify@3.0.9/dist/purify.min.js'
import { marked } from "https://cdn.jsdelivr.net/npm/marked/lib/marked.esm.js";

import * as api from './api.js';
import * as alert from './alert.js';


document.addEventListener('DOMContentLoaded', () =>
{
    const spinner = document.getElementById('spinner');

    const params = new URLSearchParams(window.location.search);


    // Карточка #1. Информация о курсе и Карточка #2. Описание
    {
        const course = document.getElementById('course');
        const course_title = document.getElementById('course_title');
        const course_author_name = document.getElementById('course_author_name');
        const course_price = document.getElementById('course_price');
        const course_description = document.getElementById('course_description');
        const course_id = document.getElementById('course_id');

        const data = new FormData();
        data.append('id', params.get('id'));
        data.append('depth', 1);

        api.make_request(api.GET_COURSE, data)
        .then(result =>
        {
            course.dataset.eduHide = false;
            course_description.dataset.eduHide = false;

            course_title.innerText = result.course.title;
            course_author_name.innerHTML = `<a href="/user?id=${result.course.author.id}">${result.course.author.name}</a>`;
            course_price.innerText = result.course.price? result.course.price : 'бесплатно';
            course_description.lastElementChild.innerHTML = DOMPurify.sanitize(marked.parse(result.course.description));
            course_id.innerText = result.course.id;
        })
        .catch(error => {
            alert.show(error.api? `Ошибка API: ${error.description}` : error.http? `Ошибка HTTP: ${error.code} ${error.text}` : 'Неизвестная ошибка', 10000);
        })
        .finally(() => {
            spinner.dataset.eduHide = true;
        })
    }


    // Карточка #3. Занятия
    {
        const lessons = document.getElementById('lessons');
        const lessons_empty = document.getElementById('lessons_empty');

        const lessons_form = document.getElementById('lessons_form');

        const lessons_table = document.getElementById('lessons_table');
        const lessons_table_body = document.getElementById('lessons_table_body');

        const data = new FormData();
        data.append('course_id', params.get('id'));
        data.append('depth', 0);

        api.make_request(api.GET_LESSONS, data)
        .then(result =>
        {
            lessons.dataset.eduHide = false;

            if (result.lessons.length == 0) {
                lessons_table.dataset.eduHide = true;
                lessons_empty.dataset.eduHide = false;
                return;
            }

            result.lessons.forEach(e => {
                lessons_table_body.append(`<tr></tr>`);
            });
        })
        .catch(error => {
            alert.show(error.api? `Ошибка API: ${error.description}` : error.http? `Ошибка HTTP: ${error.code} ${error.text}` : 'Неизвестная ошибка', 10000);
        })
        .finally(() => {

        });
    }
});
