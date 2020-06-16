// Created by Oleksandr Sorochynskyi
// On 11/09/2019
"use strict";

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
function fill_position_fields(list_selector, pos_field_selector) {
    $(list_selector)
        .find(pos_field_selector)
        .each((index, field) => {
            $(field).find("input").val(index)
        });
};

function make_sortable(list_selector, pos_field_selector) {
    var sortables = sortable(list_selector, {
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



// Call function on DOM Ready:
$(document).ready(function() {
    // Prompt the user if he tries to leave the page
    // without saving the form
    $('#recipe-edit-form').areYouSure();

    // On submit fill in the position fields
    $('#recipe-edit-form').submit((event) => {
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

    Object.keys(ordered_forms).forEach((key, idx) => {
        make_sortable(key, ordered_forms[key]);
    });

    // Handle Enter key
    setup_enter_handlers();
});

// Handle "Add ingrediennt/instruction/note" button click.
function on_add_click(prefix, prefix_str) {
    // Add the inline form
    add_inline_form(prefix, prefix_str)
    // Make the new element sortable
    Object.keys(ordered_forms).forEach((key, idx) => {
        make_sortable(key, ordered_forms[key]);
    });
    // Track new forms for changes (to ask for confirmation) 
    $('#recipe-edit-form').trigger('rescan.areYouSure');
}
