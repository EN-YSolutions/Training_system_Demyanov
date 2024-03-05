export const show = (message, timeout) =>
{
    const alert = document.createElement('div');
    alert.classList.add('alert', 'alert-danger', 'alert-dismissible', 'mb-4');
    alert.innerText = message;

    const button_close = document.createElement('button');
    button_close.type = 'button';
    button_close.classList.add('btn-close');
    button_close.dataset.bsDismiss = 'alert';
    alert.append(button_close);

    setTimeout(() => {
        alert.remove();
    }, timeout);

    document.getElementById('alerts').prepend(alert);
};
