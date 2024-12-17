var map;
var markers = [];
var autocomplete;
var selectedPlace;
var currentLocationMarker;

// Hàm khởi tạo bản đồ
function initMap() {
    map = new google.maps.Map(document.getElementById('map'), {
        center: { lat: 22.1544448, lng: 105.84064 }, // Tọa độ trung tâm bản đồ
        zoom: 9.5 // Mức thu phóng ban đầu
    });

    var locations = window.locations; // Sử dụng biến locations từ window

    // Tạo các điểm đánh dấu cho mỗi vị trí trong danh sách locations
    locations.forEach(function(location) {
        var marker = new google.maps.Marker({
            position: { lat: location.latitude, lng: location.longitude }, // Tọa độ của điểm đánh dấu
            map: map,
            title: location.name // Tiêu đề của điểm đánh dấu
        });

        var infowindow = new google.maps.InfoWindow({
            content: `<h3>${location.name}</h3><p>${location.description}</p>` // Nội dung của cửa sổ thông tin
        });

        // Thêm sự kiện click cho điểm đánh dấu để mở cửa sổ thông tin
        marker.addListener('click', function() {
            infowindow.open(map, marker);
        });

        markers.push(marker); // Thêm điểm đánh dấu vào mảng markers
    });

    // Sự kiện click trên bản đồ để lấy tọa độ
    map.addListener('click', function(event) {
        const latitude = event.latLng.lat();
        const longitude = event.latLng.lng();

        // Điền tọa độ vào form
        document.getElementById('id_latitude').value = latitude;
        document.getElementById('id_longitude').value = longitude;

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
        document.getElementById('id_latitude').value = place.geometry.location.lat();
        document.getElementById('id_longitude').value = place.geometry.location.lng();
        if (currentLocationMarker) currentLocationMarker.setMap(null);
        currentLocationMarker = new google.maps.Marker({
            position: place.geometry.location,
            map: map
        });
        map.setCenter(place.geometry.location);
        map.setZoom(12);
    });
}

// Hàm đi đến vị trí đã tìm kiếm
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

// Hàm lấy vị trí hiện tại của người dùng
function getCurrentLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition((position) => {
            const lat = position.coords.latitude;
            const lng = position.coords.longitude;
            document.getElementById('id_latitude').value = lat;
            document.getElementById('id_longitude').value = lng;
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

// Sự kiện khi DOMContentLoaded
document.addEventListener('DOMContentLoaded', () => {
    const formContainer = document.getElementById("form-container");
    const toggleButton = document.getElementById("toggle-form-btn");
    formContainer.style.display = "none";
    toggleButton.addEventListener("click", () => {
        if (formContainer.style.display === "none") {
            formContainer.style.display = "block";
            toggleButton.style.display = "none";
            document.querySelector('.map-container').style.width = '70%';
            document.querySelector('.form-container').style.width = '35%';
        } else {
            formContainer.style.display = "none";
            toggleButton.style.display = "block";
            document.querySelector('.map-container').style.width = '100%';
        }
    });
});
