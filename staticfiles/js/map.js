var map, markers = [], autocomplete, selectedPlace, currentLocationMarker;

function initMap() {
    map = new google.maps.Map(document.getElementById('map'), {
        center: { lat: 22.1261475, lng: 105.8329401 },
        zoom: 9.6,
        mapTypeControl: false,
        streetViewControl: false,
        zoomControl: false,
        fullscreenControl: false
    });

    // Thêm tên huyện lên bản đồ
    const districts = [
        { name: 'Ba Bể', lat: 22.4099, lng: 105.7200 },
        { name: 'Bắc Kạn', lat: 22.1470, lng: 105.8342 },
        { name: 'Bạch Thông', lat: 22.2461, lng: 105.8329 },
        { name: 'Chợ Đồn', lat: 22.1456, lng: 105.5852 },
        { name: 'Chợ Mới', lat: 21.9784, lng: 105.8487 },
        { name: 'Na Rì', lat: 22.2633, lng: 106.1145 },
        { name: 'Ngân Sơn', lat: 22.4928, lng: 105.9475 },
        { name: 'Pác Nặm', lat: 22.5863, lng: 105.6655 }
    ];

    districts.forEach(district => {
        new google.maps.Marker({
            position: { lat: district.lat, lng: district.lng },
            map: map,
            label: { text: district.name, color: '#4682B4', fontSize: '16px', fontWeight: 'bold' },
            icon: { path: google.maps.SymbolPath.CIRCLE, scale: 0 }
        });
    });

    // // Bắt sự kiện click trên bản đồ
    // map.addListener('click', function(event) {
    //     updateLocation(event.latLng.lat(), event.latLng.lng());
    // });

    // // Tìm kiếm địa điểm
    // const input = document.getElementById('searchInput');
    // autocomplete = new google.maps.places.Autocomplete(input);
    // autocomplete.bindTo('bounds', map);
    // autocomplete.addListener('place_changed', handlePlaceSelect);
}

function updateLocation(lat, lng) {
    document.getElementById('id_latitude').value = lat;
    document.getElementById('id_longitude').value = lng;

    if (currentLocationMarker) currentLocationMarker.setMap(null);
    currentLocationMarker = new google.maps.Marker({ position: { lat, lng }, map: map, title: 'Vị trí đã chọn' });
}

function handlePlaceSelect() {
    const place = autocomplete.getPlace();
    if (!place.geometry) return alert("Không tìm thấy vị trí nào.");

    selectedPlace = place;
    updateLocation(place.geometry.location.lat(), place.geometry.location.lng());
    map.setCenter(place.geometry.location);
    map.setZoom(12);
}

function getCurrentLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(position => {
            updateLocation(position.coords.latitude, position.coords.longitude);
            map.setCenter({ lat: position.coords.latitude, lng: position.coords.longitude });
            map.setZoom(12);
        }, () => alert('Không thể lấy vị trí của bạn.'));
    } else {
        alert('Trình duyệt của bạn không hỗ trợ Geolocation.');
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const formContainer = document.getElementById("form-container");
    const toggleButton = document.getElementById("toggle-form-btn");

    formContainer.style.display = "none";

    toggleButton.addEventListener("click", () => {
        formContainer.style.display = formContainer.style.display === "none" ? "block" : "none";
        toggleButton.style.display = formContainer.style.display === "block" ? "none" : "block";
        document.querySelector('.map-container').style.width = formContainer.style.display === "block" ? '45%' : '100%';
    });

    document.querySelector('.btn-secondary').addEventListener("click", () => {
        formContainer.style.display = "none";
        toggleButton.style.display = "block";
        document.querySelector('.map-container').style.width = '100%';
    });
});
