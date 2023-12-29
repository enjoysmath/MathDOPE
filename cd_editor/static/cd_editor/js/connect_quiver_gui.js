var cd_editor_window;


$(document).ready(() => {
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
        cd_editor_window.ui.label_position_spinner_action($("#arrow-label-position-input").val());
    });
      
    $(window).on('load', () => {        
        cd_editor_window.ui.load_diagram_action();
        set_enabled_arrow_edit_button(false);
    });    
});

