var cd_editor_window;

function set_diagram_name(name)
{
    $('#diagram-name').text(name);
}

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
        const json_data = cd_editor_window.ui.load_diagram_action();
        set_diagram_name(json_data['diagram_name']);
    });    
});

