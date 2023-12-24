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
    $('#deselect-all-button').on('click', () => {
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
      
    $(window).on('load', () => {
        cd_editor_window.ui.load_diagram_action();    
    });    
});

