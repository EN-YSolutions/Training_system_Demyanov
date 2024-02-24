const API_GET_USERS = 'get_users';
const API_GET_GROUPS = 'get_groups';
const API_GET_COURSES = 'get_courses';


const make_request = (method, args) => new Promise((resolve, reject) =>
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
