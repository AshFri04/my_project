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




function showFavoriteResults (result) {
    alert(result);

}

function submitFavoritesBakery(evt) {
    evt.preventDefault();

    let bake_id = evt.currentTarget.id

    console.log(bake_id)

    let formValues = {
        "restaurant_name": $("#bakery-name-" + bake_id).val(),
        "restaurant_id": $("#bakery-id-" + bake_id).val(),

    }

    $.post("/favorite", formValues, showFavoriteResults);
}

$(".favorite_form_bake").on("submit", submitFavoritesBakery);


