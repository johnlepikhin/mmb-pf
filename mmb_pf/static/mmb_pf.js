// Hello friend, nice that you are here and hope with good intentions.
// This whole system (frontend, backend) is invented, written and tested by me - fzeulf =)
// It was a hard work during 2021 year, hope there is not so many bugs and this system will be usefull.
/******************************************************************************
                                TOOLS
******************************************************************************/
// Set infinity cookie
// setCookie('adminMenuCurrent', menu_btn);
function setCookie(name, value, days) {
    let expires = "";
    if (days) {
        let date = new Date();
        date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
        expires = "; expires=" + date.toUTCString();
    }
    document.cookie = name + "=" + value + expires + "; path=/; SameSite=Strict";
}
// Get cookie by name
// getCookie('adminMenuCurrent')
function getCookie(name) {
    let nameEQ = name + "=";
    let ca = document.cookie.split(';');
    for (let i = 0; i < ca.length; i++) {
        let c = ca[i];
        while (c.charAt(0) == ' ') c = c.substring(1, c.length);
        if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length, c.length);
    }
    return null;
}

function delCookie(name) {
    document.cookie = name + '=; expires=Thu, 01 Jan 1970 00:00:01 GMT;';
}

// Capitalizes first letter of defined string
function capitalizeFirstLetter(string) {
    return string.charAt(0).toUpperCase() + string.slice(1);
}

/* get all url vars as hash
TAKE:
{
    params: [], // optional, set param names to get,
}
RETURN: {
    'param': 'val'
}
*/
function getUrlParams(args = {}) {
    let result = {};
    let page_url = decodeURIComponent(window.location.search.substring(1));
    let url_variables = page_url.split('&');

    for (let i = 0; i < url_variables.length; i++) {
        let param_name = url_variables[i].split('=');
        if (param_name.length === 1 && param_name[0] === "") {
            continue;
        }
        if (args.params && args.params.length) {
            if (args.params.indexOf(param_name[0]) !== -1) {
                result[param_name[0]] = param_name[1];
            }
        } else {
            result[param_name[0]] = param_name[1];
        }
    }

    return result;
}
// Download file from backend response in browser
// TAKE: {
//     data: data, # object from responseResolver
//     filename: custom_filename, # if not set, filename from content-disposition will be taken
// }
function downloadFile(args = {}) {
    if (!args.data) {
        return;
    }
    let filename = "file";
    if (args.filename) {
        filename = args.filename;
    } else {
        let disposition = args.data.headers.get("content-disposition");
        let filenameRegex = /filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/;
        let matches = filenameRegex.exec(disposition);
        if (matches != null && matches[1]) {
            filename = matches[1].replace(/['"]/g, '');
        }
    }
    saveAs(args.data.url, filename);
}

/*
Convert string to object
Sorry i have no time (or little bit lazy) to write complex format support
TAKE:
{
    str: "", // string for parse
    format: standard    // [optional]
}
RETURN: Date object, if something wrong too
*/
function getDateObj(args = {}) {
    let format = 'DD.MM.YYYY HH:mm';
    if (args.format) {
        format = args.format;
    }
    let formats = {
        'DD.MM.YYYY HH:mm': {
            're': /(\d{2})\.(\d{2})\.(\d{4})\s+(\d{2}):(\d{2})/,
            'order': '$3-$2-$1T$4:$5',
        }
    };
    let dateObj = null;
    if (format in formats && args.str) {
        dateObj = new Date(args.str.replace(formats[format].re, formats[format].order));
    } else { // just return date obj
        dateObj = new Date();
    }

    return dateObj;
}


/*
Inupt fields validator
TAKE: {
    form_checks:{
        event_name: {
            type: 'check', // will be checked anytime by regexp
            re: '^.{0,1024}$',
            err_msg: 'Обязательное поле',
            valid_0: true, // [Optional] make 0 value is valid
        },
        date_of_event: {
            type: 'check_if_filled', // will be checked only if filled, by regexp
            re: '^\\d{4}\\-\\d{2}\\-\\d{2}$',
            err_msg: 'Неверный формат, допускается ГГГГ-ММ-ДД',
        },
    },
    data_to_check:  { (structure used for sending data)
        event_name: 'value',
        date_of_event: 'another value',
    },
    validation: { (structure used for colorizing form elements)
        event_name: true,
        date_of_event: true,
    }
}
RETURN: true if all fields valid or false if not
*/
function checkFormFields(args = {}) {
    let all_checked = true;
    for (checked_field in args.data_to_check) {
        if (!(checked_field in args.form_checks)) {
            continue;
        }
        const re_field = new RegExp(args.form_checks[checked_field].re, "");
        if (args.form_checks[checked_field].type === 'check') {
            if (! check_field_defined({val: args.data_to_check[checked_field], valid_0: args.form_checks[checked_field].valid_0})) {
                args.validation[checked_field] = false;
                all_checked = false;
            } else {
                if (args.form_checks[checked_field].re) {
                    if (args.data_to_check[checked_field].toString().search(re_field) === -1) {
                        args.validation[checked_field] = false;
                        all_checked = false;
                    } else {
                        args.validation[checked_field] = true;
                    }
                } else {
                    args.validation[checked_field] = true;
                }
            }
        } else if (args.form_checks[checked_field].type === 'check_if_filled') {
            if (check_field_defined({val: args.data_to_check[checked_field], valid_0: args.form_checks[checked_field].valid_0})) {
                if (args.data_to_check[checked_field].toString().search(re_field) === -1) {
                    args.validation[checked_field] = false;
                    all_checked = false;
                } else {
                    args.validation[checked_field] = true;
                }
            } else {
                args.validation[checked_field] = true;
            }
        } else if (args.form_checks[checked_field].type === 'object_not_empty') {
            if (typeof args.data_to_check[checked_field] === 'object') {
                if (!$.isEmptyObject(args.data_to_check[checked_field])) {
                    args.validation[checked_field] = true;
                } else {
                    args.validation[checked_field] = false;
                    all_checked = false;
                }
            } else {
                args.validation[checked_field] = false;
                all_checked = false;
            }
        }
    }
    return all_checked;
}
// Exclude 0 from false values
// TAKE
// {
//    val: value, // checked val
//    valid_0: false, // set true is 0 is valid value
// }
function check_field_defined(args) {
    let result = true;
    if (! args.val) {
        result = false;
        if (typeof args.val == 'number' && args.val == 0 && args.valid_0) {
            result = true;
        }
    }
    return result;
}
/*
Transliterate cyrrilic
TAKE: {
    "string": "чтото",
    "lower": true, // [optional] false by default
}
RETURN: ready string
*/
function transliterate(args) {
    const cyrrilic_map = { "Ё": "YO", "Й": "I", "Ц": "TS", "У": "U", "К": "K", "Е": "E", "Н": "N", "Г": "G", "Ш": "SH", "Щ": "SCH", "З": "Z", "Х": "H", "Ъ": "_", "ё": "yo", "й": "i", "ц": "ts", "у": "u", "к": "k", "е": "e", "н": "n", "г": "g", "ш": "sh", "щ": "sch", "з": "z", "х": "h", "ъ": "_", "Ф": "F", "Ы": "I", "В": "V", "А": "a", "П": "P", "Р": "R", "О": "O", "Л": "L", "Д": "D", "Ж": "ZH", "Э": "E", "ф": "f", "ы": "i", "в": "v", "а": "a", "п": "p", "р": "r", "о": "o", "л": "l", "д": "d", "ж": "zh", "э": "e", "Я": "Ya", "Ч": "CH", "С": "S", "М": "M", "И": "I", "Т": "T", "Ь": "_", "Б": "B", "Ю": "YU", "я": "ya", "ч": "ch", "с": "s", "м": "m", "и": "i", "т": "t", "ь": "_", "б": "b", "ю": "yu" };
    let result = args.string.split('').map(function (char) {
        return cyrrilic_map[char] || char;
    }).join("");

    if (args.lower) {
        return result.toLowerCase();
    } else {
        return result;
    }
}

function get_rand_from_array(array) {
    return array[Math.floor(Math.random() * array.length)];
}
/******************************************************************************
                        Data Getters / Senders
******************************************************************************/
/*
Can send json data with files at one request

TAKE:{
    method: POST, PATCH, PUT,
    type: json / form, // json for json sending only, form - for comlex data with files and json
    url: endpoint url for post request
    jsondata: {
    },
    files: [
        {
            key: "user_photo_"+i, // file key - used for catch this file obj at server side
            obj: file_obj, // event file object event.target.files[0]
        },
    }
}

RETURN:
promise
*/
function sendDataV2(args) {
    if (!args.type) {
        args.type = 'json';
    }

    let json_data;
    let body_data;
    let headers = {
        'X-CSRFToken': getCookie('csrftoken')
    };
    if (args.type === 'json') {
        body_data = JSON.stringify(args.jsondata);
        headers['Content-Type'] = 'application/json;charset=utf-8';
    } else if (args.type === 'form') {
        body_data = new FormData();
        json_data = JSON.stringify(args.jsondata);
        body_data.append('jsondata', json_data);
        if (args.files && args.files.length) {
            for (file_obj of args.files) {
                body_data.append(file_obj.key, file_obj.obj);
            }
        }
    }

    return new Promise((resolve, reject) => {
        fetch(args.url, {
            method: args.method,
            headers: headers,
            body: body_data
        })
        .then(function (response) {
            if (response.status.toString().search('^20\\d$') === -1) {
                responseResolver(response, args).then((data) => reject(data));
            } else {
                responseResolver(response, args).then((data) => resolve(data));
            }
        });
    });
}

/* TAKE:
url: /api/v1/events/ // some backend url
args: {
    ok_404: true, false // False by default; return empty object as resolve {} if 404 happens, or return its data
    ok_403: true, false // False by default; return empty object as resolve {} if 403 happens, or return its data
    ok_string_err: true, false // False by default; if string got - it will be converted to json {'msg': 'Status status text'}, if true string returned

    // Use this if you need change behaviour depending from status at final app
    status: true, false // False by default; return {data: backend data, status: 200}, as RESOLVE, or return its data
}
RETURN:
promise
*/
function getDataV2(url, args = {}) {
    return new Promise((resolve, reject) => {
        fetch(url)
        .then(response => {
            if (args.status) {
                return responseResolver(response, args).then((data) => resolve({ 'data': data, 'status': response.status }));
            }
            if (response.status === 404) {
                return args.ok_404 ? resolve({}) : responseResolver(response, args).then((data) => reject(data));
            } else if (response.status === 403) {
                return args.ok_403 ? resolve({}) : responseResolver(response, args).then((data) => reject(data));
            } else if (response.status.toString().search('^20\\d$') === -1) {
                return responseResolver(response, args).then((data) => reject(data));
            } else {
                return responseResolver(response, args).then((data) => resolve(data));
            }
        })
    });
}

// Helper function for processing response object
// TAKE:
// response object,
// {
//      no_modify_response: true, # if no modifications with answer is need
//      ok_string_err: true, # if string response allowed
//      blob_reponse: true, # if blob reponse expected - data url will be returned
// }
function responseResolver(response, args = {}) {
    return new Promise((resolve, reject) => {
        if (args.blob_reponse && (response.status === 200)) { // get blob only if 200 response
            response.blob()
                .then(function (myBlob) {
                    let result = {
                        url: URL.createObjectURL(myBlob),
                        headers: response.headers,
                    };
                    resolve(result);
                });
        } else {
            response.text()
                .then((text_data) => {
                    try {
                        return JSON.parse(text_data);
                    } catch (err) {
                        return text_data;
                    }
                })
                .then((result) => {
                    if (!args.no_modify_response) {
                        if (!result) {
                            result = { 'msg': response.status + ' ' + response.statusText };
                        }
                        if (typeof result === "string" && !(args.ok_string_err)) {
                            result = { 'msg': response.status + ' ' + response.statusText };
                        }
                    }
                    resolve(result);
                });
        }
    });
}
/*
    Load data to defined fields
    do not use for load big data endpoints, due long load time

    Loader stops if error occured
    TAKE: {
        load: [{url: '', var: '', dict: ''}, {}],
        self: self,
        sync: true, // if sync mode is false - err_msg or info_msg will not be checked
    }

    if loaded object is list - it could be converted to dict, id used as key
    RETURN: promise

    USAGE:
    loadItems({'load': loadable_fields, 'self': self}).then(() => {
        // do next things
    });
*/
function loadItems(args) {
    return new Promise((resolve, reject) => {
        if (args.sync) {
            async function loopLoader(self, array) {
                for (const obj of array) {
                    await getDataV2(obj.url, { status: true }).then(data => {
                        if (data.status === 403) {
                            self.info_msg = data.data.msg;
                            self.appLoading = false;
                        } else if (data.status !== 200) {
                            self.err_msg = data.data.msg;
                            self.appLoading = false;
                        } else {
                            Vue.set(self, obj.var, data.data);
                            if (obj.dict) {
                                if (Array.isArray(data.data)) {
                                    let dict = {};
                                    for (const array_obj of data.data) {
                                        if (array_obj.id) {
                                            dict[array_obj.id] = array_obj;
                                        }
                                    }
                                    Vue.set(self, obj.dict, dict);
                                }
                            }
                        }
                    }).catch(err => {
                    });
                    if (self.info_msg || self.err_msg) {
                        break;
                    }
                }
                resolve();
            }
            loopLoader(args.self, args.load);
        } else {
            for (const obj of args.load) {
                getDataV2(obj.url, { status: true }).then(data => {
                    if (data.status === 403) {
                        args.self.info_msg = data.data.msg;
                        args.self.appLoading = false;
                    } else if (data.status !== 200) {
                        args.self.err_msg = data.data.msg;
                        args.self.appLoading = false;
                    } else {
                        Vue.set(args.self, obj.var, data.data);
                        if (obj.dict) {
                            if (Array.isArray(data.data)) {
                                let dict = {};
                                for (const array_obj of data.data) {
                                    if (array_obj.id) {
                                        dict[array_obj.id] = array_obj;
                                    }
                                }
                                Vue.set(args.self, obj.dict, dict);
                            }
                        }
                    }
                }).catch(err => {
                });
            }
            resolve();
        }
    });
}

/*
    IMAGE PROCESSING
*/
// Used for return some default image src or custom if defined
// TAKE: {
//  mediaimg: user_photo.jpg,               // any image from media directory
//  default: 'some type from common images',   // some default image from dictionary
//  custom: blob/url, // returned if defined
// }

// RETURN:
// image url
function getImageUrl(obj) {
    const commonImages = {
        user_photo: '/media/user_photo.jpg',
    };

    if (obj['custom']) {
        return obj['custom'];
    } else if (obj['default']) {
        return commonImages[obj['default']];
    } else if (obj['mediaimg']) {
        return '/media/' + obj['mediaimg'];
    }
}

/******************************************************************************
                                CLASS CHANGERS
******************************************************************************/

/*
Used for colorizing text input fields
TAKE: {
    classes: [],
    size: 'sm', # by default
    type: 'check' or undefined
    valid: true or false
}

RETURN:
class object {}
*/
function fieldBorderClass(args) {
    let returnedClass = {
        'form-control': true,
        'form-control-sm': true,
        'border': true,
    };
    if (args.size && args.size !== 'sm') {
        returnedClass['form-control-sm'] = false;
    }
    for (idx in args.classes) {
        returnedClass[args.classes[idx]] = true;
    }
    if (args.type === 'check') {
        returnedClass['border-dark'] = true;
    }
    if (!args.valid) {
        returnedClass['border-dark'] = false;
        returnedClass['border-danger'] = true;
        returnedClass['is-invalid'] = true;
    }
    return returnedClass;
}

/*
Used for colorizing div border around some element
TAKE: {
    classes: [],
    valid: true or false
}

RETURN:
class object {}
*/
function divBorderClass(args) {
    let returnedClass = {};
    for (idx in args.classes) {
        returnedClass[args.classes[idx]] = true;
    }

    if (!args.valid) {
        returnedClass['border'] = true;
        returnedClass['border-danger'] = true;
        returnedClass['is-invalid'] = true;
        returnedClass['rounded'] = true;
    }
    return returnedClass;
}

/*
Used for colorizing forms statuses badges
TAKE: {
    classes: [],
    true: ''
}

RETURN:
class object {}
*/
function formBadgeClass(args) {
    let returnedClass = {
        'badge': true,
        'badge-pill': true,
    };
    for (idx in args.classes) {
        returnedClass[args.classes[idx]] = true;
    }

    returnedClass[args.true] = true;

    return returnedClass;
}

/*
Used for colorizing forms statuses buttons (usually in tables)
TAKE: {
    classes: [],
    true: ''
}

RETURN:
class object {}
*/
function formStatusBtnClass(args) {
    let returnedClass = {
        'btn': true,
        'btn-sm': true,
        'w-100': true,
    };
    for (idx in args.classes) {
        returnedClass[args.classes[idx]] = true;
    }
    returnedClass[args.true] = true;

    return returnedClass;
}

/*
Used for colorizing event difficulty statuses badges
TAKE: {
    classes: [],
    cat: '', # letter A, B, C
}

RETURN:
class object {}
*/
function eventDifficultyClass(args) {
    let colors = {
        'A': ['red', 'lighten-3'],
        'B': ['yellow', 'lighten-3'],
        'C': ['green', 'lighten-3'],
    };

    let returnedClass = {
    };
    for (idx in args.classes) {
        returnedClass[args.classes[idx]] = true;
    }
    for (idx in colors[args.cat]) {
        returnedClass[colors[args.cat][idx]] = true;
    }
    return returnedClass;
}

/*
Used for colorizing event difficulty statuses badges
TAKE: {
    classes: [],
    indxes: [], # indexes for colorizing
    cur_idx: 1, # current index
    color: ['green', 'lighten-5'], # [OPTIONAL] by default
}

RETURN:
class object {}
*/
function colorRowClass(args) {
    let returnedClass = {
    };
    for (idx in args.classes) {
        returnedClass[args.classes[idx]] = true;
    }
    let color = args.color && args.color.length ? args.color : ['green', 'lighten-5'];

    if (args.indxes.includes(args.cur_idx)) {
        for (idx in color) {
            returnedClass[color[idx]] = true;
        }
    }
    return returnedClass;
}
/* Subfunction for colorizing role tables
TAKE: {
    idx: 0,
    role_obj: {},
    role_reserve_id: 14,
    classes: ['text-small', 'text-gray', 'text-center'], // default
}

RETURN:
class object {}
*/
function role_table_colorizer(args) {
    let returnedClass = {};
    let default_classes = ['text-small', 'text-gray', 'text-center'];
    if (args.classes && args.classes.length) {
        default_classes = args.classes;
    }

    if (args.idx === 0) {
        returnedClass = colorRowClass({classes: default_classes, indxes:[0], cur_idx: args.idx});
    } else if (args.role_obj.event_role_id == args.role_reserve_id) {
        returnedClass = colorRowClass({
            classes: default_classes,
            indxes:[args.idx],
            cur_idx: args.idx,
            color: ['lime', 'lighten-5'],
        });
    } else {
        returnedClass = colorRowClass({classes: default_classes, indxes:[], cur_idx: args.idx});
    }
    return returnedClass;
}

/* Subfunction for colorizing role tables
TAKE: {
    event: obj,
}

RETURN:
obj {total: 100, reg: 50}; // total - total required, reg - registered
*/
function event_participants_calc(args) {
    let result = {
        total: 0,
        reg: 0,
    };
    if (args.event.cfg.roles) {
        for (role_obj of args.event.cfg.roles) {
            result.total += Number(role_obj.amount);
            result.reg += Object.keys(role_obj.users).length;
        }
    }
    return result;
}

/*
Used for colorizing buttons according they object key state
TAKE: {
    key: obj.key, # 'key in object for check',
    me: true, # [OPTIONAL] define initial state true/false for two state buttons YES NO, if this is one button, skip this key
    classes: {}, # [OPTIONAL] overwrite default classes
    color_classes: [], # [OPTIONAL] classes used for colorization, first elem is for true value, second for false
}

RETURN:
class object {}
*/
function universalBtnClass(args) {
    let returnedClass = Object.assign(
        {
            'btn': true, 'btn-md': true, 'm-0': true, 'px-3': true, 'py-2': false, 'z-depth-0': true, 'waves-effect': true, 'rounded': true,
        },
        args.classes
    );
    let color_classes = ['btn-outline-success', 'btn-outline-light'];
    if ('color_classes' in args && args.color_classes.length) {
        color_classes = args.color_classes;
    }
    if (args.hasOwnProperty("me")) {
        if (args.key) {
            if (args.me) {
                returnedClass[color_classes[0]] = true;
            } else {
                returnedClass[color_classes[1]] = true;
            }
        } else {
            if (args.me) {
                returnedClass[color_classes[1]] = true;
            } else {
                returnedClass[color_classes[0]] = true;
            }
        }
    } else {
        if (args.key) {
            returnedClass[color_classes[0]] = true;
        } else {
            returnedClass[color_classes[1]] = true;
        }
    }

    return returnedClass;
};

/******************************************************************************
                                OTHER
******************************************************************************/
/*
Used for colorizing progress bar
TAKE: {
    complex: {
        data: [], # all data
        id: '', # index of object in the data for calculation
    },
    simple: {
        all: 10,
        curr: 2,
    }
    type: 'get_class', # for return style width or 'get_pct' for string pct return
}

RETURN:
class object {}

EXAMPLE:
return style
:style="calc_pb({'complex': {id': idx, 'data': loaded_data.form_statuses}, 'type': 'get_class'})">

return str
-* calc_pb({'complex': {'id': idx, 'data': loaded_data.form_statuses}, 'type': 'get_pct'}) *-
*/
function calc_pb(args) {
    let returnedWidth = "width: ";
    let all_data = 1;
    let pct = 0;
    if (args.complex) {
        args.complex.data.forEach(function (obj, i, arr) {
            all_data += obj.val;
        });
        if (all_data <= 0)
            all_data = 1;
        pct = Math.ceil(args.complex.data[args.complex.id].val * 100 / all_data);
    } else if (args.simple) {
        if (args.simple.all <= 0) {
            all_data = 1;
        } else {
            all_data = args.simple.all;
        }
        pct = Math.ceil(args.simple.curr * 100 / all_data);
    }
    if (args.type === 'get_class') {
        returnedWidth += pct + "%";
        return returnedWidth;
    } else if (args.type === 'get_pct') {
        return pct + "%";
    }
}

/*
Used show or close card by cookie
TAKE: {
    'key': 'pc_main_events', # cookie key for check and set current card state
    'change': true, # should it be toggle
}

RETURN:
class object {}
*/
function card_show_close(args) {
    let returnedClass = {
        'collapse': true,
        'show': true,
    };
    let key_state = getCookie(args.key) ? getCookie(args.key) : 'open';
    if (args.change) {
        if (key_state === 'open') {
            returnedClass.show = false;
            setCookie(args.key, 'close');
        } else {
            returnedClass.show = true;
            setCookie(args.key, 'open');
        }
    } else {
        if (key_state === 'open') {
            returnedClass.show = true;
        } else {
            returnedClass.show = false;
        }
    }
    return returnedClass;
}

function page_up() {
    $('html, body').animate({ scrollTop: 0 }, 'fast');
};

/*
Close all other opened modals and show defined
TAKE: {
    'id': '#myModalId', # with selector! #
    'timeout': 2000, # Optional,
    'custom': false, # Optional, set true if custom modal windows should be opened, not from all_modals
}

RETURN:
*/
const all_modals = {
    '#modalResponseInfo': false,
    '#modalResponseSuccess': false,
    '#modalResponseWarn': false,
};
let modal_show_timer_id;
function modal_show(args) {
    if (modal_show_timer_id) {
        clearTimeout(modal_show_timer_id);
        modal_show_timer_id = undefined;
    }
    if (!args.custom) {
        args.custom = false;
        Object.entries(all_modals).forEach(([key, value]) => {
            if (value) {
                modal_hide({ id: key });
            }
            all_modals[key] = false;
        });
    }

    if (args.timeout) {
        $(args.id).on('shown.bs.modal', function () {
            modal_show_timer_id = setTimeout(function () {
                $(args.id).modal("hide").off('shown.bs.modal');
                if (!args.custom) {
                    all_modals[args.id] = false;
                }
            }, args.timeout);
        });
        $(args.id).modal('show');
    } else {
        $(args.id).modal('show').off('shown.bs.modal');
    }
    if (!args.custom) {
        all_modals[args.id] = true;
    }
}

// TAKE: {
//     'id': '#myModalId', # with selector! #
// }
function modal_hide(args) {
    $(args.id).on('shown.bs.modal', function () {
        $(args.id).modal('hide').off('shown.bs.modal');
    })
    $(args.id).modal('hide');
}

// TAKE: {
//   add_site: true, // add http://site.name to string
//   str: 'string to copy', // for copy to clipboard
// }
function copy_to_clipboard(args) {
    const el = document.createElement('textarea');
    if (! ('add_site' in args) || args.add_site) {
        el.value = location.protocol + '//' + location.host
    }
    el.value += args.str;
    el.setAttribute('readonly', '');
    el.style.position = 'absolute';
    el.style.left = '-9999px';
    document.body.appendChild(el);
    el.select();
    document.execCommand('copy');
    document.body.removeChild(el);
}
/*
TAKE: {
   obj: [], // array with objects for sum
   key: 'some_key_from_obj', // key from object from array to sum
}
RETURN: sum integer

USAGE: sumValues({'obj': loaded_data.form_statuses, 'key': 'val'})
*/
function sumValues(args) {
    let sum = 0;
    for (let el in args.obj) {
        if (args.obj.hasOwnProperty( el )) {
            sum += parseFloat(args.obj[el][args.key]);
        }
    }
    return sum;
}

/*
TAKE: {
   user_ranks_dict: {}, // dict with ranks id: name
   user_ranks: [],      // user ranks to convert
}
RETURN: string

USAGE: sumValues({'obj': loaded_data.form_statuses, 'key': 'val'})
*/
function user_ranks_to_str(args) {
    let ranks = [];
    for (const rank_id of args.user_ranks) {
        if (rank_id in args.user_ranks_dict) {
            ranks.push(args.user_ranks_dict[rank_id].name)
        }
    }
    return ranks.join("; ");
}