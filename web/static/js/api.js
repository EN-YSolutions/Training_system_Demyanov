export const LOGIN = 'login';
export const LOGOUT = 'logout';

export const GET_USERS = 'get_users';
export const GET_USER = 'get_user';
export const GET_USER_GROUPS = 'get_user_groups';

export const GET_GROUPS = 'get_groups';
export const GET_GROUP = 'get_group';
export const GET_GROUP_MEMBERS = 'get_group_members';
export const ADD_GROUP_MEMBER = 'add_group_member';
export const DELETE_GROUP_MEMBER = 'delete_group_member';

export const GET_COURSES = 'get_courses';
export const GET_COURSE = 'get_course';

export const GET_LESSONS = 'get_lessons';


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
