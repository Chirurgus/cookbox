// Created by Oleksandr Sorochynskyi
// On 11/09/2019

// Selectors for the lists with position field, together
// with the class of position field selectors
const ordered_forms = {
    '.ing-grp-form-list' : '.ing-grp-form-pos',
    '.ins-form-list' : '.ins-form-pos',
    '.ing-grp-ing-form-list' : '.ing-form-pos'
}

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
}

make_sortable = function(selector) {
    var sortables = sortable(selector, {
        handle: 'span.sortable-handle',
        forcePlaceholderSize: true
    });
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
});

// Handle "Add ingrediennt/instruction/note" button click.
on_add_click = function(prefix, prefix_str) {
    // Add the inline form
    add_inline_form(prefix, prefix_str)
    // Make the new element sortable
    Object.keys(ordered_forms).forEach(make_sortable);
}