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

    var locations = window.locations; // Sử dụng biến locations từ window

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

    // Sự kiện click trên bản đồ để lấy tọa độ
    map.addListener('click', function(event) {
        const latitude = event.latLng.lat();
        const longitude = event.latLng.lng();

        // Điền tọa độ vào form
        document.getElementById('id_coordinates').value = `${latitude}, ${longitude}`;

        // Xóa marker trước đó nếu có
        if (currentLocationMarker) {
            currentLocationMarker.setMap(null);
        }

        // Tạo marker mới tại vị trí người dùng click
        currentLocationMarker = new google.maps.Marker({
            position: event.latLng,
            map: map,
            title: 'Vị trí đã chọn'
        });
    });

    // Tìm kiếm vị trí
    const input = document.getElementById('searchInput');
    autocomplete = new google.maps.places.Autocomplete(input);
    autocomplete.bindTo('bounds', map);
    autocomplete.addListener('place_changed', () => {
        const place = autocomplete.getPlace();
        if (!place.geometry) {
            alert("Không tìm thấy vị trí nào.");
            return;
        }
        selectedPlace = place;
        document.getElementById('id_coordinates').value = `${place.geometry.location.lat()}, ${place.geometry.location.lng()}`;
        if (currentLocationMarker) currentLocationMarker.setMap(null);
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
        if (currentLocationMarker) currentLocationMarker.setMap(null);
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
        navigator.geolocation.getCurrentPosition((position) => {
            const lat = position.coords.latitude;
            const lng = position.coords.longitude;
            document.getElementById('id_coordinates').value = `${lat}, ${lng}`;
            map.setCenter({ lat, lng });
            map.setZoom(12);
            if (currentLocationMarker) currentLocationMarker.setMap(null);
            currentLocationMarker = new google.maps.Marker({
                position: { lat, lng },
                map: map,
                title: 'Bạn ở đây'
            });
            const infoWindow = new google.maps.InfoWindow({ content: '<p style="color: black; font-size: 12.5px; padding: 0px; line-height: 1.3;">Bạn ở đây</p>' });
            currentLocationMarker.addListener('click', () => infoWindow.open(map, currentLocationMarker));
        }, () => alert('Không thể lấy vị trí của bạn.'));
    } else {
        alert('Trình duyệt của bạn không hỗ trợ Geolocation.');
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const formContainer = document.getElementById("form-container");
    formContainer.style.display = "none";
    document.getElementById("toggle-form-btn").addEventListener("click", () => {
        if (formContainer.style.display === "none") {
            formContainer.style.display = "block";
            document.querySelector('.map-container').style.width = '65%';
            document.querySelector('.form-container').style.display = 'block';
        } else {
            formContainer.style.display = "none";
            document.querySelector('.map-container').style.width = '100%';
        }
    });
});
