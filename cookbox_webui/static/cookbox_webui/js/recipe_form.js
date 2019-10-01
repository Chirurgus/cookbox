// Created by Oleksandr Sorochynskyi
// On 11/09/2019

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

// Fill the position field
// The values are determined by the order in the
// <ol> of the DOM
fill_position = function(selector) {
    $(selector).find('[id$=position]').each(
        function(index) { 
            // Set the value to the index (i.e. the position
            // in the list)
            $(this).val(index);
        }
    );
}

make_sortable = function(selector) {
    var sortables = sortable(selector, {
        handle: 'span.sort-handle',
        forcePlaceholderSize: true
    });
}

// Selectors for the items that are sortable
sortables = [
    '.ingredient-group-form-list', '.ins-form-list',
    '.ing-grp-ing-form-list', '.ing-note-form-list'
]

// Selectors for the lists that are ordered
ordered = [
    '.ing-grp-form-list', '.ins-form-list',
    '.ing-grp-ing-form-list'
]

$('#recipe-edit-form').submit(function(event) {
    ordered.forEach(fill_position);
})

// Call function on DOM Ready:
$(document).ready(function() {
    sortables.forEach(make_sortable);
    //formUnloadPrompt('form');
});

// Handle "Add ingrediennt/instruction/note" button click.
on_add_click = function(prefix, prefix_str) {
    // Add the inline form
    add_inline_form(prefix, prefix_str)
    // Make the new element sortable
    sortables.forEach(element => {
        make_sortable(element)
    });
}