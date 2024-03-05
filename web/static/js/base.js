import * as api from './api.js';


document.addEventListener('DOMContentLoaded', () =>
{
    if (window.matchMedia)
    {
        const html = document.querySelector('html');
        const prefersColorScheme = window.matchMedia('(prefers-color-scheme: dark)');

        if (prefersColorScheme.matches)
            html.dataset.bsTheme = 'dark';

        prefersColorScheme.addEventListener('change', event => {
            html.dataset.bsTheme = event.matches? 'dark' : 'light';
        });
    }


    document.querySelectorAll('#logout').forEach(e =>
    {
        e.addEventListener('click', event =>
        {
            event.preventDefault();

            api.make_request(api.LOGOUT)
            .then(result => {
                window.location.replace('/');
            });
        });
    });


    const sidebar_users = document.querySelectorAll('#sidebar_users');
    const sidebar_groups = document.querySelectorAll('#sidebar_groups');
    const sidebar_courses = document.querySelectorAll('#sidebar_courses');

    const sidebar_course_edit = document.querySelectorAll('#sidebar_course_edit');
    const sidebar_tasks_info = document.querySelectorAll('#sidebar_tasks_info');


    const breadcrumb_users = document.querySelectorAll('#breadcrumb_users');
    const breadcrumb_groups = document.querySelectorAll('#breadcrumb_groups');
    const breadcrumb_courses = document.querySelectorAll('#breadcrumb_courses');

    const breadcrumb_course_edit = document.querySelectorAll('#breadcrumb_course_edit');
    const breadcrumb_tasks_info = document.querySelectorAll('#breadcrumb_tasks_info');


    switch (document.location.pathname)
    {
        case '/users':
        case '/user':
            sidebar_users.forEach(e => { e.classList.add('active'); });
            breadcrumb_users.forEach(e => { e.dataset.eduHide = false; });
            break;
        case '/groups':
        case '/group':
            sidebar_groups.forEach(e => { e.classList.add('active'); });
            breadcrumb_groups.forEach(e => { e.dataset.eduHide = false; });
            break;
        case '/courses':
        case '/course':
            sidebar_courses.forEach(e => { e.classList.add('active'); });
            breadcrumb_courses.forEach(e => { e.dataset.eduHide = false; });
            break;
        case '/course_edit':
            sidebar_course_edit.forEach(e => { e.classList.add('active') });
            breadcrumb_course_edit.forEach(e => { e.dataset.eduHide = false; });
            break;
        case '/tasks_info':
            sidebar_tasks_info.forEach(e => { e.classList.add('active'); });
            breadcrumb_tasks_info.forEach(e => { e.dataset.eduHide = false; });
            break;
    }
});
