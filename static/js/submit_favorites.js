"use strict"


// AJAX call to confirm favorites are stored to user.
function showFavoriteResults (result) {
    alert(result);

}

function submitFavorites(evt) {
    evt.preventDefault();

    let rest_id = evt.currentTarget.id

    let formValues = {
        "restaurant_name": $("#restaurant-name-" + rest_id).val(),
        "restaurant_id": $("#restaurant-id-" + rest_id).val(),

    };

    $.post("/favorite", formValues, showFavoriteResults);
}

$(".favorite_form_rest").on("submit", submitFavorites);






