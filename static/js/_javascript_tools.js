window.messages_tag_id = "#django-messages-div";
//window.messages_url = null;

function load_html_from_url(url, elem) {
    $.get(url, function(data, status) {
        elem.html(data);
    });   
}

function set_arrow_curvature(value)
{
    $("#arrow-curvature-input").val(value);
}

function set_arrow_offset(value)
{
    $("#arrow-offset-input").val(value);
}

function set_arrow_label_position(value)
{
    $("#arrow-label-position-input").val(value);
}

function set_diagram_name(name)
{
    const name_elem = $("#diagram-name");
    name_elem.text(name);
    render_element_in_katex(name_elem[0]);
}

function set_enabled_arrow_edit_button(en)
{
    if (en) {
        $("#arrow-gear-button").css("visibility", "visible");
    }
    else {
        $("#arrow-gear-button").css("visibility", "hidden");
    }
}

function render_element_in_katex(element)
{
    renderMathInElement(element, {
          delimiters: [
              {left: "$$", right: "$$", display: true},
              {left: "$", right: "$", display: false}
          ],
          throwOnError : false
        });
}


function display_django_messages() {
    messagesDiv = $(window.messages_tag_id);
    messagesDiv.empty();
    load_html_from_url(window.messages_url, messagesDiv);
}

function post_string_to_url(data, url)
{
    $.ajax({
        type: 'POST',
        url: url,
        data: data,
        success: function(data, status, xhr) {         // Function( Anything data, String textStatus, jqXHR jqXHR )
            if ('msg' in data) {
                const msg = data['msg'];
                console.log(msg);
                display_django_messages();
            }
        },
        error : function(xhr, errmsg, err) {
            // Provide a bit more info about the error to the console:
            if (errmsg) {
                console.log('ERROR: ' + errmsg);
                display_django_messages();
            }
            console.log(xhr.status + ": " + xhr.responseText);             
        }
    });
}

function csrf_safe_method(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function setup_ajax_csrf_token(csrf_token) { 
    // BUGFIX.  This took hours to get to work!  
    // And remember the csrf_token line at the top of template
    window.csrf_token = csrf_token;
    
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrf_safe_method(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrf_token);
            }
        }
    });
}