$(document).ready(function () {
    $('.chat-input input').keyup(function (e) {
        if ($(this).val() == '')
            $(this).removeAttr('good');
        else
            $(this).attr('good', '');
    });
    $(".chat-input input").keypress(function (event) {
        var keycode = (event.keyCode ? event.keyCode : event.which);
        if (keycode == '13') {
            res();
        }
    });
});


function get_msg_user(msg) {
    let templet =
        `
        <article class="msg-container msg-self" id="msg-0">
            <div class="msg-box">
                <div class="flr">
                    <div class="messages">
                        <p class="msg" id="msg-1">
                            ${msg}
                        </p>
                    </div>
                </div>
                <img class="user-img" id="user-0" src="https://gravatar.com/avatar/56234674574535734573000000000001?d=retro" />
            </div>
        </article>
    `
    return templet;
}

function get_msg_bot(msg) {
    let templet =
        `
        <article class="msg-container msg-remote" id="msg-0">
            <div class="msg-box">
                <img class="user-img" id="user-0" src="https://gravatar.com/avatar/00034587632094500000000000000000?d=retro" />
                <div class="flr">
                    <div class="messages">
                        <p class="msg" id="msg-0">
                           ${msg}
                        </p>
                    </div>
                </div>
            </div>
        </article>
    `
    return templet;
}



let boturl = 'http://127.0.0.1:8080/bot/api'

var cnt = 1;

function res() {
    let box = document.getElementById('msgtext');
    let msg = $("#msgtext").val();
    if (msg.length <= 0)
        return;
    $("#msgtext").prop("disabled", true);
    //sndbtn
    $("#sndbtn").prop("disabled", true);
    $("#msgtext").val('');
    $('.chat-input input').removeAttr('good');
    $("#window").append(get_msg_user(msg));
    $("#window").animate({ scrollTop: $("#window").height() + cnt * 1000 }, 1000);
    cnt++;
    let formData = {
        'data': msg
    };
    $.ajax({
        type: "POST",
        url: boturl,
        contentType: 'application/x-www-form-urlencoded',
        data: formData,
        crossDomain: true,
        credentials: 'same-origin',
        success: function (data, textStatus, xmLHttpRequest) {
            console.log(data);
            let rep = data['data']['reply']
            $("#window").append(get_msg_bot(rep));
            $("#window").animate({ scrollTop: $("#window").height() + cnt * 1000 }, 1000);
            cnt++;
            $("#msgtext").prop("disabled", false);
            $("#sndbtn").prop("disabled", false);
            $('.chat-input input').removeAttr('good');
            $("#msgtext").val('');
            $("#msgtext").focus();
        },
        error: function (xhr, ajaxOptions, thrownError) {
            console.log(thrownError);
            toastr.error('Somthing is wrong', 'Error');
            $("#window").append(get_msg_bot('Somthing is wrong at the server side'));
            $("#window").animate({ scrollTop: $("#window").height() + cnt * 1000 }, 1000);
            cnt++;
            $("#msgtext").prop("disabled", false);
            $("#sndbtn").prop("disabled", false);
            $('.chat-input input').removeAttr('good');
            $("#msgtext").val('');
            $("#msgtext").focus();
        },
    });

    console.log(msg);
}