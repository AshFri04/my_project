"use strict";  


let sanFrancisco = {lat: 37.758129, lng:-122.439012}

let neighborhood_lat = document.querySelector(".hood_lat").value;
let neighborhood_lng = document.querySelector(".hood_lng").value;

console.log(neighborhood_lat)
console.log(neighborhood_lng)

let map = new google.maps.Map(document.querySelector('#map'), {
      center: {lat: parseFloat(neighborhood_lat), lng: parseFloat(neighborhood_lng)},
      zoom:15,
      mapTypeId: 'roadmap'

});

let coordinates = document.querySelectorAll(".coordinates");

let locationDetails = [];

for (let coordinate of coordinates){
    // append is push in js
    // locationDeatail is a list of all coordinates of restaurants in that given neighborhood 
    locationDetails.push(coordinate.value);
}
    

for (let i =0; i < (locationDetails.length); i++) {
    // Change myImageURL to an icon involving eating
    let myImageURL = 'https://developers.google.com/maps/documentation/javascript/examples/full/images/beachflag.png';
    let locationDetail = locationDetails[i].split(' ');
    let latitude = parseFloat(locationDetail[0]);
    let longitude = parseFloat(locationDetail[1]);

    let restaurant = new google.maps.LatLng(latitude,longitude);

    let marker = new google.maps.Marker({
        position: restaurant,
        map: map,
        title: 'Hover text',
        icon: myImageURL
    });
 
    let contentString = '<div id="content">' +
    '<h1>All my custom content</h1>' +
    '</div>';

    let infoWindow = new google.maps.InfoWindow({
    content: contentString,
    maxWidth: 200
    });

    marker.addListener('click', function() {
    infoWindow.open(map, marker);
    });



}



