"use strict"


// Excutes js after DOM is loaded
$(document).ready(function() {
//     console.log('hello ashley');

// document.getElementById('login').addEventListener('click', showSignOut());

// function showSignOut() {
//     let signout = document.querySelector(".signout");
//     signout.classList.remove("signout-hide");
//     signout.classList.add("signout-show");
//     }

let button = document.querySelector('my-button');


// <div id="map">

$.post('/restaurant', {latitude: restaurant.latitude, longitude: restaurant.longitude}, initMap)

var map;
var restaurant_location = {{ restaurant.latitude }}, {{ restaurant.longitude }};

function initMap() {
map = new google.maps.Map(document.getElementById('map'), 
{
zoom: 12,
center: restaurant_location
});



}) //end of document
    



















