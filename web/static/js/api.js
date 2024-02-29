export const LOGIN = 'login';

export const GET_USERS = 'get_users';
export const GET_USER = 'get_user';
export const GET_USER_GROUPS = 'get_user_groups';
export const DELETE_USER_GROUP = 'delete_user_group';

export const GET_GROUPS = 'get_groups';
export const GET_GROUP = 'get_group';
export const GET_GROUP_MEMBERS = 'get_group_members';

export const GET_COURSES = 'get_courses';
export const GET_COURSE = 'get_course';


export const make_request = (method, args) => new Promise((resolve, reject) =>
{
    fetch(`/api/${method}`, {method: 'POST', body: args})
    .then(response =>
    {
        response.json()
        .then(json_response =>
        {
            if (!json_response.ok) {
                reject({http: true, api: true, description: json_response.description});
                return;
            }

            resolve(json_response.result);
            return;
        })
        .catch(_  => {
            reject({http: true, api: false, code: response.status, text: response.statusText});
            return;
        });
    })
    .catch(error => {
        reject({http: false, api: false, error: error});
        return;
    });
});
