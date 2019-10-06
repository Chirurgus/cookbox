// Created by Oleksandr Sorochynskyi
// On 11/09/2019

// Selectors for the lists with position field, together
// with the class of position field selectors
const ordered_forms = {
    '.ing-grp-form-list' : '.ing-grp-form-pos',
    '.ins-form-list' : '.ins-form-pos',
    '.ing-grp-ing-form-list' : '.ing-form-pos'
};

const enter_handler_args = [
    [".ing-grp-form-name input", ".ing-grp-add-ing-grp-btn"],
    [".ins-form-desc input", ".ins-add-ins-btn"],
    [".recipe-note-form .note-form-desc input", ".recipe-note-add-note-btn"],
    [".ing-form-qty input, .ing-form-unit input, .ing-form-desc input", ".ing-grp-add-ing-btn", ".ing-grp-form"],
    [".ing-note-form-list .note-form-desc input", ".ing-form-add-note-btn", ".ing-form"],
    [".ins-note-form-list .note-form-desc input", ".ins-form-add-note-btn", ".ins-form"],
];

// Helper functions

// Add an inline form to a formset
add_inline_form = function(prefix, prefix_str) {
    // Get the index of the new form
    var form_idx = $('#id_' + prefix + '-TOTAL_FORMS').val();

    // Generate the html for the new form from empty_form
    var new_form_html = $('#' + prefix + '_empty_form').html().replace(
        new RegExp(prefix_str, 'g'), form_idx
    );
    new_form_html = "<li>" + new_form_html + "</li>"

    // Generate the new form, and wrap it in <li>
    var new_form = jQuery(new_form_html);

    // Append new form to the form set
    new_form.appendTo('#' + prefix);
    // Increment TOTAL_FORMS counter
    $('#id_' + prefix + '-TOTAL_FORMS').val(parseInt(form_idx) + 1);

    return new_form
}

delete_inline_form = function(delete_checkbox_selector, inline_form_selector) {
    var del_checkbox = $(delete_checkbox_selector);

    // Mark the inline form for deletion
    del_checkbox.prop('checked', true);
    
    // Hide the inline from view (it will still be submitted).
    del_checkbox.closest(inline_form_selector).addClass("hide");
}

function reload_page(){
    window.location.reload();
}

function set_enter_key_handler(
    event_source_selector,
    button_selector,
    via_selector=null)
{
    $('#recipe-edit-form').on(
        "keydown",
        event_source_selector,
        function(event) {
            if (event.key == "Enter") {
                if (via_selector === null) {
                    $(button_selector).click();
                }
                else {
                    $(this)
                        .parents(via_selector)
                        .find(button_selector)
                        .click();
                }
                event.stopPropagation();
                event.preventDefault();
            }
        }
    );
}

// Fill the position field (found using pos_field_selector)
// for the list (found using list_selector).
// The values are determined by the order in the <ol> of the DOM
fill_position_fields = function(list_selector, pos_field_selector) {
    // There may be multipole lists that match to a list_selector
    $(list_selector).each(function(list_idx, ol) {
        $(ol).find(pos_field_selector).each(
            function(field_idx, field) { 
                // Set the value to the index (i.e. the position
                // in the list)
                $(field).find("input").val(field_idx);
            }
        );
    });
};

make_sortable = function(selector) {
    var sortables = sortable(selector, {
        handle: 'span.sortable-handle',
        forcePlaceholderSize: true
    });
};


// Set contextual behavior for the Enter key
// If were in a inline form list Enter should add
// another form to the list
function setup_enter_handlers() {
    // By default ignore Enter key
    $(document).on("keydown", function(event) {
        if (event.key == "Enter") {
            event.stopPropagation();
            event.preventDefault();
        }
    })

    // But allow it for buttons
    $(document).on("keydown", "button", function(event) {
        if (event.key == "Enter") {
            event.stopPropagation();
        }
    })

    // If inside a list of inline forms Enter adds new form.
    // If inside nested list the deepest item is added, for 
    // this to work these have to be called in order from
    // outside inside.
    enter_handler_args.forEach(function(args) {
        // ... spread operator (like * in Python)
        set_enter_key_handler(...args);
    })
}


// On submit fill in the position fields
$('#recipe-edit-form').submit(function(event) {
    // For every ordered list
    Object.keys(ordered_forms).forEach(
        (list_selector, index) => {
            fill_position_fields(
                list_selector,
                ordered_forms[list_selector]
            )
        }
    );
    return true;
});

// Call function on DOM Ready:
$(document).ready(function() {
    Object.keys(ordered_forms).forEach(make_sortable);
    //formUnloadPrompt('form');

    setup_enter_handlers();
});

// Handle "Add ingrediennt/instruction/note" button click.
on_add_click = function(prefix, prefix_str) {
    // Add the inline form
    add_inline_form(prefix, prefix_str)
    // Make the new element sortable
    Object.keys(ordered_forms).forEach(make_sortable);
}



