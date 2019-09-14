// Created by Oleksandr Sorochynskyi
// On 11/09/2019

// Add an inline form to a formset
add_inline_form = function(prefix) {
    // Get the index of the new form
    var form_idx = $('#id_' + prefix + '-TOTAL_FORMS').val();

    // Generate the html for the new form from empty_form
    var new_form_html = $('#' + prefix + '_empty_form').html().replace(/__prefix__/g, form_idx);
    new_form_html = "<li>" + new_form_html + "</li>"

    // Generate the new form, and wrap it in <li>
    var new_form = jQuery(new_form_html);

    // Append new form to the form set
    new_form.appendTo('#' + prefix);
    // Increment TOTAL_FORMS counter
    $('#id_' + prefix + '-TOTAL_FORMS').val(parseInt(form_idx) + 1);

    // Add default value for the position
    // new_form.find("input[id$='position']").val(form_idx)
}

make_sortable = function(selector) {
    var sortables = sortable(selector, {
        handle: 'h2'
    });
    // When an item is drag'n'dropped, update the position field automatically
    sortables[0].addEventListener('sortupdate', function(e) {
        $(e.detail.destination.container)
            .find('[id$=position]')
            .each(function(index) { 
                $(this).val(index);
        });
    });
}
