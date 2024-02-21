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

    const sidebar_users = document.querySelectorAll('#sidebar_users');
    const sidebar_groups = document.querySelectorAll('#sidebar_groups');
    const sidebar_courses = document.querySelectorAll('#sidebar_courses');

    const sidebar_add_to_group = document.querySelectorAll('#sidebar_add_to_group');
    const sidebar_course_edit = document.querySelectorAll('#sidebar_course_edit');
    const sidebar_group_info = document.querySelectorAll('#sidebar_group_info');
    const sidebar_tasks_info = document.querySelectorAll('#sidebar_tasks_info');

    const breadcrumb_users = document.querySelector('#breadcrumb_users');
    const breadcrumb_groups = document.querySelector('#breadcrumb_groups');
    const breadcrumb_courses = document.querySelector('#breadcrumb_courses');

    const breadcrumb_add_to_group = document.querySelector('#breadcrumb_add_to_group');
    const breadcrumb_course_edit = document.querySelector('#breadcrumb_course_edit');
    const breadcrumb_group_info = document.querySelector('#breadcrumb_group_info');
    const breadcrumb_tasks_info = document.querySelector('#breadcrumb_tasks_info');

    switch (document.location.pathname)
    {
        case '/':
            sidebar_users.forEach(e => e.classList.add('active'));
            breadcrumb_users.removeAttribute('style');
            break;
        case '/groups':
            sidebar_groups.forEach(e => e.classList.add('active'));
            breadcrumb_groups.removeAttribute('style');
            break;
        case '/courses':
            sidebar_courses.forEach(e => e.classList.add('active'));
            breadcrumb_courses.removeAttribute('style');
            break;
        case '/add_to_group':
            sidebar_add_to_group.forEach(e => e.classList.add('active'));
            breadcrumb_add_to_group.removeAttribute('style');
            break;
        case '/course_edit':
            sidebar_course_edit.forEach(e => e.classList.add('active'));
            breadcrumb_course_edit.removeAttribute('style');
            break;
        case '/group_info':
            sidebar_group_info.forEach(e => e.classList.add('active'));
            breadcrumb_group_info.removeAttribute('style');
            break;
        case '/tasks_info':
            sidebar_tasks_info.forEach(e => e.classList.add('active'));
            breadcrumb_tasks_info.removeAttribute('style');
            break;
    }
});