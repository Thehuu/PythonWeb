var map;
var markers = [];
var autocomplete;
var selectedPlace;
var currentLocationMarker;

function initMap() {
    map = new google.maps.Map(document.getElementById('map'), {
        center: { lat: 22.1544448, lng: 105.84064 },
        zoom: 9.5
    });

    var locations = {{ locations|safe }};
    locations.forEach(function(location) {
        var marker = new google.maps.Marker({
            position: { lat: location.latitude, lng: location.longitude },
            map: map,
            title: location.name
        });

        var infowindow = new google.maps.InfoWindow({
            content: `<h3>${location.name}</h3><p>${location.description}</p>`
        });

        marker.addListener('click', function() {
            infowindow.open(map, marker);
        });

        markers.push(marker);
    });

    var input = document.getElementById('searchInput');
    autocomplete = new google.maps.places.Autocomplete(input);
    autocomplete.bindTo('bounds', map);

    autocomplete.addListener('place_changed', function() {
        var place = autocomplete.getPlace();
        if (!place.geometry) {
            alert("Không tìm thấy vị trí nào.");
            return;
        }

        selectedPlace = place;

        document.getElementById('id_latitude').value = place.geometry.location.lat();
        document.getElementById('id_longitude').value = place.geometry.location.lng();

        if (currentLocationMarker) {
            currentLocationMarker.setMap(null);
        }

        currentLocationMarker = new google.maps.Marker({
            position: place.geometry.location,
            map: map
        });

        map.setCenter(place.geometry.location);
        map.setZoom(12);
    });
}

function goToLocation() {
    if (selectedPlace && selectedPlace.geometry) {
        map.setCenter(selectedPlace.geometry.location);
        map.setZoom(12);

        if (currentLocationMarker) {
            currentLocationMarker.setMap(null);
        }

        currentLocationMarker = new google.maps.Marker({
            position: selectedPlace.geometry.location,
            map: map
        });
    } else {
        alert('Vui lòng tìm kiếm vị trí trước khi đi đến.');
    }
}

function getCurrentLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function(position) {
            var lat = position.coords.latitude;
            var lng = position.coords.longitude;

            document.getElementById('id_latitude').value = lat;
            document.getElementById('id_longitude').value = lng;

            map.setCenter({ lat: lat, lng: lng });
            map.setZoom(12);

            if (currentLocationMarker) {
                currentLocationMarker.setMap(null);
            }

            currentLocationMarker = new google.maps.Marker({
                position: { lat: lat, lng: lng },
                map: map,
                title: 'Bạn ở đây'
            });

            var infoWindow = new google.maps.InfoWindow({
                content: '<p>Bạn ở đây</p>'
            });

            currentLocationMarker.addListener('click', function() {
                infoWindow.open(map, currentLocationMarker);
            });

        }, function() {
            alert('Không thể lấy vị trí của bạn.');
        });
    } else {
        alert('Trình duyệt của bạn không hỗ trợ Geolocation.');
    }
}

document.addEventListener('DOMContentLoaded', function() {
    var formContainer = document.getElementById("form-container");
    formContainer.style.display = "none";

    document.getElementById("toggle-form-btn").addEventListener("click", function() {
        if (formContainer.style.display === "none") {
            formContainer.style.display = "block";
        } else {
            formContainer.style.display = "none";
        }
    });
});
