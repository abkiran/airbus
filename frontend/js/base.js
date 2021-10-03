API_URL = "http://"+location.hostname + ":8000/"

function do_login(params) {
    username = $('#username').val()
    pass = $('#pass').val()
    if (username == '' || pass == '') {
        alert("Username/Password can't empity!")
        return false
    }
    $.ajax({
        type: "POST",
        url: API_URL +"api/token/",
        // contentType: "application/json",
        data: {
            "username": username,
            "password": pass
        },
        success: function (result) {
            reset_access_token(result.access)
            location.href = "index.html"
        }
    });
}

function do_logout(params) {
    // unset localStorage and cookies
    redirect_login()
}

function is_loggedin(params) {
    
}

function get_inventory(params) {
    $.ajax({
        type: "GET",
        url: API_URL + "inventory/",
        data: {
            
        },
        success: function (result) {
            // console.log(result)
            render_inventory_list(result)
        }
    });
}

function render_inventory_list(result_json) {
    i = 0
    tr = ""
    result_json.forEach(item => {
        tr += "<tr id='row-"+item['id']+"'>"
        tr += "<td>"+i+"</td>"
        tr += "<td>"+item['product_id']+"</td>"
        tr += "<td>"+item['product_category']+"</td>"
        tr += "<td>"+item['product_name']+"</td>"
        tr += "<td>"+item['product_description']+"</td>"
        tr += "<td>"+item['units']+"</td>"
        tr += "<td><button class='btn btn-sm btn-success update' onclick='update_inventory("+item['id']+")'> Update </button> <button class='btn btn-sm btn-danger' onclick='delete_inventory("+item['id']+")'> Delete </button></td>"
        tr += "</tr>"
        i++
    });
    $('#inventory_list').html(tr)
}
function update_inventory(id) {
    $.ajax({
        type: "GET",
        url: API_URL + "inventory/" + id + "/",
        success: function (result, textStatus, jqXHR) {
            if (jqXHR.status == 200) {
                $('#update_inventory').modal("toggle")
                setTimeout(() => {
                    $('#update-btn').removeAttr('onclick')
                    $('#uproduct_id').val(result['product_id'])
                    $('#uproduct_category').val(result['product_category'])
                    $('#uproduct_name').val(result['product_name'])
                    $('#uproduct_description').val(result['product_description'])
                    $('#uunits').val(result['units'])
                    
                    $('#update-btn').attr('onclick', 'save_inventory('+id+')')
                }, 100);
            }
        }
    });
}

function save_inventory(id = 0) {
    if (!$('#inventory_form').valid()) {
        alert("please fix errors and resubmit!")
        return false
    }
    product_id = $('#product_id').val()
    product_category = $('#product_category').val()
    product_name = $('#product_name').val()
    product_description = $('#product_description').val()
    units = $('#units').val()
    url = API_URL + "inventory/"
    type = "POST"
    if (id != 0) {
        // update the existing product
        type = "PUT"
        url += id + "/"
        product_id = $('#uproduct_id').val()
        product_category = $('#uproduct_category').val()
        product_name = $('#uproduct_name').val()
        product_description = $('#uproduct_description').val()
        units = $('#uunits').val()
    }
    data = {
        "product_id": product_id,
        "product_category": product_category,
        "product_name": product_name,
        "product_description": product_description,
        "units": units
    }
    $.ajax({
        type: type,
        url: url,
        data: JSON.stringify(data),
        success: function (result) {
            alert("Product id = "+product_id+" is saved!")
            location.href = "index.html"
        },
        error: function(params, status, jqXHR) {
            if (params.status == 409) {
                alert(params.responseJSON['detail'])
                return false
            }
            alert("There was an error saving Product info")
        }
    });
}

function delete_inventory(id) {
    if (id=='') {
        alert("wrong inventory selected")
        return false
    }
    $.ajax({
        type: "DELETE",
        url: API_URL + "inventory/"+id+"/",
        success: function (result, textStatus, jqXHR) {
            console.log(textStatus + ": " + jqXHR.status);
            if (jqXHR.status == 204) {
                alert("Product deleted successfully!")
                $('#row-'+id).fadeOut()
            }
        }
    });
}







$(document).ready(function (e) {
    if (window.location.href.indexOf("login") > -1) {
        return false
    }
    token = get_token()
    console.log(token)
    if (token == undefined || token == '') {
        redirect_login()
    }
    $.ajaxSetup({
        beforeSend: function (xhr) {
            if (token != '') {
                xhr.setRequestHeader("Authorization", "Bearer " + token);
            }
        }
    });
    $(document).ajaxError(function (event, xhr, options, exc) {
        if (xhr.status == 401) {
            redirect_login()
        }
    });
    get_inventory()
})
function redirect_login() {
    localStorage.setItem("is_logged_in", 0);
    eraseCookie('access_token')
    location.href = "login.html"
}

function get_token() {

    var access_token = getCookie('access_token');
    if (access_token) {
        return access_token
    }
    redirect_login()
}

function reset_access_token(access_token) {
    setCookie('access_token', access_token)
    // tokenData = getTokenData(access_token)
    localStorage.setItem("is_logged_in", 1);
    return access_token
}


function setCookie(name, value, seconds) {
    var expires = "";
    if (seconds) {
        var date = new Date();
        date.setTime(date.getTime() + (seconds * 1000));
        expires = "; expires=" + date.toGMTString();
    }
    document.cookie = name + "=" + (value || "") + expires + "; path=/";
}
function getCookie(name) {
    var nameEQ = name + "=";
    var ca = document.cookie.split(';');
    for (var i = 0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') c = c.substring(1, c.length);
        if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length, c.length);
    }
    return null;
}
function eraseCookie(name) {
    document.cookie = name + '=; Path=/; Expires=Thu, 01 Jan 1970 00:00:01 GMT;';
}

