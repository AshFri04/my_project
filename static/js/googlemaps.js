"use strict";  


let sanFrancisco = {lat: 37.758129, lng:-122.439012};

let neighborhood_lat = document.querySelector(".hood_lat").value;
let neighborhood_lng = document.querySelector(".hood_lng").value;

let map = new google.maps.Map(document.querySelector('#map'), {
      center: {lat: parseFloat(neighborhood_lat), lng: parseFloat(neighborhood_lng)},
      zoom:15,
      mapTypeId: 'roadmap'

});

let coordinates = document.querySelectorAll(".coordinates");
let restaurantNames = document.querySelectorAll(".rest_name");
let restaurantTypes = document.querySelectorAll(".rest_type");

let locationDetails = [];
let restaurantNameDetails = [];
let restaurantTypeDetails = [];

for (let coordinate of coordinates) {
    // append is push in js
    // locationDeatail is a list of all coordinates of restaurants in that given neighborhood 
    locationDetails.push(coordinate.value);
}

for (let restaurantName of restaurantNames) {
    restaurantNameDetails.push(restaurantName.value);

}

for (let restaurantType of restaurantTypes) {
    restaurantTypeDetails.push(restaurantType.value);

}
    

for (let i = 0; i < (locationDetails.length); i++) {
    let locationDetail = locationDetails[i].split(' ');
    let latitude = parseFloat(locationDetail[0]);
    let longitude = parseFloat(locationDetail[1]);
    let restName = restaurantNameDetails[i]
    let restType = restaurantTypeDetails[i]


    let restaurant = new google.maps.LatLng(latitude,longitude);

    let marker = new google.maps.Marker({
        position: restaurant,
        map: map,
        title: restName,
        icon: '/static/images/icon.png'
    });

    
    let contentString = '<div id="content">' +
    '<h3>'+ restName + '</h3>' +
    '<h3>'+ restType + '</h3>' +
    '</div>';

    let infoWindow = new google.maps.InfoWindow({
    content: contentString,
    maxWidth: 200
    });

    marker.addListener('click', function() {
    infoWindow.open(map, marker);
    });



}



