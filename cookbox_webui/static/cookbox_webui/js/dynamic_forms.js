// Created by Oleksandr Sorochynskyi
// On 17/11/2019
"use strict";

// Add an inline form to a formset
function add_inline_form(prefix, prefix_str='__prefix__', focus_new=true) {
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

    if (focus_new) {
        new_form.find("input:visible").first().focus();
    }

    return new_form
}

function delete_inline_form(delete_checkbox_selector, inline_form_selector) {
    var del_checkbox = $(delete_checkbox_selector);

    // Mark the inline form for deletion
    del_checkbox.prop('checked', true);
    
    // Hide the inline from view (it will still be submitted).
    del_checkbox.closest(inline_form_selector).hide();
}
