var cd_editor_window;


document.addEventListener("DOMContentLoaded", () => {
    $('#centre-view-button').on('click', () => {
        cd_editor_window.ui.centre_view_action();
    });    
    $('#save-button').on('click', () => {
        cd_editor_window.ui.save_diagram_action();
    });
    $('#select-all-button').on('click', () => {
        cd_editor_window.ui.select_all_action();
    });
    $('#select-none-button').on('click', () => {
        cd_editor_window.ui.deselect_all_action();
    });
    $('#delete-button').on('click', () => {
        cd_editor_window.ui.delete_action();
    });
    $('#undo-button').on('click', () => {
        cd_editor_window.ui.undo_action();
    });
    $('#redo-button').on('click', () => {
        cd_editor_window.ui.redo_action();
    });
    $('#center-view-button').on('click', () => {
        cd_editor_window.ui.center_view_action(); 
    });
    $('#zoom-out-button').on('click', () => {
        cd_editor_window.ui.zoom_out_action(); 
    });
    $('#zoom-in-button').on('click', () => {
        cd_editor_window.ui.zoom_in_action(); 
    });
    $('#reset-zoom-button').on('click', () => {
        cd_editor_window.ui.reset_zoom_action();
    });
    $('#show-hints-switch').on('change', () => {
        if ($('#show-hints-switch').is(':checked'))
        {
            cd_editor_window.ui.show_hints_action();
            $('#show-hints-switch-label').text('Hide Hints');
        } 
        else {
            cd_editor_window.ui.show_hints_action();
            $('#show-hints-switch-label').text('Show Hints');
        }
    });
    $('#show-grid-switch').on('change', () => {
        if ($('#show-grid-switch').is(':checked'))
        {
            cd_editor_window.ui.show_grid_action();
            $('#show-grid-switch-label').text('Hide Grid');
        } 
        else {
            cd_editor_window.ui.show_grid_action();
            $('#show-grid-switch-label').text('Show Grid');
        }
    });
    $('#show-queue-switch').on('change', () => {
        if ($('#show-queue-switch').is(':checked'))
        {
            cd_editor_window.ui.show_queue_action();
            $('#show-queue-switch-label').text('Hide Queue');
        } 
        else {
            cd_editor_window.ui.show_queue_action();
            $('#show-queue-switch-label').text('Show Queue');
        }
    });        
    $("#arrow-position-button").on('click', () => {
        // Close the current modal:
        $('#arrow-settings-modal').modal('toggle');        
    });    
    $("#reverse-arrows-button").on('click', () => {        
        cd_editor_window.ui.reverse_arrows_action();
    });
    $("#flip-arrows-button").on('click', () => {
        cd_editor_window.ui.flip_arrows_action();
    });    
    $("#arrow-label-position-input").on('input', () => {
        cd_editor_window.ui.label_position_action($("#arrow-label-position-input").val());
    });
    $("#arrow-offset-input").on('input', () => {
        cd_editor_window.ui.arrow_offset_action($("#arrow-offset-input").val());
    });
    $("#arrow-tail-shorten").on('change', () => {
        var current_val = parseInt($("#arrow-tail-shorten").val());
        const head_val = parseInt($("#arrow-head-shorten").val());
        
        if (current_val + 20 > head_val) {
            current_val = parseInt($("#arrow-tail-shorten").val(Math.max(head_val - 20, 0)));
        }
        
        $("#arrow-head-shorten").attr({
            "min" : Math.min(current_val + 20, 100)
        });        
        cd_editor_window.ui.arrow_tail_shorten_action(current_val, head_val);
    });
    $("#arrow-head-shorten").on('change', () => {
        var current_val = parseInt($("#arrow-head-shorten").val());
        const tail_val = parseInt($("#arrow-tail-shorten").val());
        
        if (current_val - 20 < tail_val) {
            current_val = parseInt($("#arrow-head-shorten").val(Math.min(tail_val + 20, 100)));
        }
        
        $("#arrow-tail-shorten").attr({
            "max" : Math.max(current_val - 20, 0)
        });
        
        cd_editor_window.ui.arrow_tail_shorten_action(tail_val, current_val);
    });
    $("#arrow-curvature-input").on('input', () => {
        cd_editor_window.ui.arrow_curvature_action($("#arrow-curvature-input").val());
    });
    $("#flip-arrow-labels-button").on('click', () => {
        cd_editor_window.ui.flip_arrow_labels_action(); 
    });   
    $("#left-align-radio").change(() => {
        if ($("#left-align-radio").is(":checked"))
            cd_editor_window.ui.label_align_action("left");
    });    
    $("#center-align-clear-radio").change(() => {
        if ($("#center-align-clear-radio").is(":checked"))
            cd_editor_window.ui.label_align_action("centre");
    });
    $("#center-align-over-radio").change(() => {
        if ($("#center-align-over-radio").is(":checked"))
            cd_editor_window.ui.label_align_action("over");
    });    
    $("#right-align-radio").change(() => {
        if ($("#right-align-radio").is(":checked"))
            cd_editor_window.ui.label_align_action("right");
    });    
      
    $(window).on('load', () => {        
        cd_editor_window.ui.load_diagram_action();
        set_enabled_arrow_edit_button(false);
    });    
});

