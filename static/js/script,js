// This script dynamically updates the form choices when the page loads
$(document).ready(function() {
    var seatsInput = $('#id_seats');
    var seatChoices = JSON.parse('{{ form.seats.choices|escapejs }}');

    // For each choice, create an option element and add it to the select element
    seatChoices.forEach(function(choice) {
        // Create the option element
        var option = $('<option>').attr({
            value: choice[0]
        }).text(choice[1]);

        // Select the option if the seat is already selected
        if (seatsInput.val() === choice[0]) {
            option.prop('selected', true);
        }

        // Add the option to the select element
        seatsInput.append(option);
    });
});







