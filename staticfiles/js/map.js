// Biến toàn cục để lưu trữ bản đồ, các marker, và các trạng thái liên quan
var map;
var markers = []; // Danh sách các marker trên bản đồ
var autocomplete; // Tự động hoàn thành tìm kiếm vị trí
var selectedPlace; // Vị trí đã được chọn từ autocomplete
var currentLocationMarker; // Marker đại diện cho vị trí hiện tại của người dùng

// Hàm khởi tạo bản đồ
function initMap() {
    map = new google.maps.Map(document.getElementById('map'), {
        center: { lat: 22.1544448, lng: 105.84064 }, // Tọa độ trung tâm của bản đồ
        zoom: 9.5 // Độ phóng ban đầu
    });

    // Lấy danh sách các vị trí từ biến toàn cục
    var locations = window.locations; // Sử dụng biến locations từ window

    // Thêm các marker lên bản đồ từ danh sách vị trí
    locations.forEach(function(location) {
        var marker = new google.maps.Marker({
            position: { lat: location.latitude, lng: location.longitude }, // Tọa độ của marker
            map: map,
            title: location.name // Tiêu đề hiển thị khi rê chuột vào marker
        });

        // Tạo một cửa sổ thông tin khi người dùng nhấp vào marker
        var infowindow = new google.maps.InfoWindow({
            content: `<h3>${location.name}</h3><p>${location.description}</p>`
        });

        // Lắng nghe sự kiện click vào marker để hiển thị thông tin
        marker.addListener('click', function() {
            infowindow.open(map, marker);
        });

        markers.push(marker); // Lưu marker vào danh sách markers
    });

    // Tìm kiếm địa điểm với input autocomplete
    var input = document.getElementById('searchInput');
    autocomplete = new google.maps.places.Autocomplete(input);
    autocomplete.bindTo('bounds', map);

    // Xử lý sự kiện khi người dùng chọn địa điểm từ autocomplete
    autocomplete.addListener('place_changed', function() {
        var place = autocomplete.getPlace();
        if (!place.geometry) {
            alert("Không tìm thấy vị trí nào.");
            return;
        }

        selectedPlace = place; // Lưu thông tin địa điểm đã chọn

        // Cập nhật giá trị tọa độ vào form
        document.getElementById('id_latitude').value = place.geometry.location.lat();
        document.getElementById('id_longitude').value = place.geometry.location.lng();

        // Xóa marker hiện tại nếu có
        if (currentLocationMarker) {
            currentLocationMarker.setMap(null);
        }

        // Tạo marker mới cho địa điểm đã chọn
        currentLocationMarker = new google.maps.Marker({
            position: place.geometry.location,
            map: map
        });

        map.setCenter(place.geometry.location); // Di chuyển bản đồ đến vị trí mới
        map.setZoom(12); // Phóng to bản đồ
    });
}

// Hàm đi đến vị trí đã chọn
function goToLocation() {
    if (selectedPlace && selectedPlace.geometry) {
        map.setCenter(selectedPlace.geometry.location);
        map.setZoom(12);

        // Xóa marker hiện tại nếu có
        if (currentLocationMarker) {
            currentLocationMarker.setMap(null);
        }

        // Tạo marker mới tại vị trí đã chọn
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
        navigator.geolocation.getCurrentPosition(function(position) {
            var lat = position.coords.latitude; // Vĩ độ hiện tại
            var lng = position.coords.longitude; // Kinh độ hiện tại

            // Cập nhật giá trị tọa độ vào form
            document.getElementById('id_latitude').value = lat;
            document.getElementById('id_longitude').value = lng;

            map.setCenter({ lat: lat, lng: lng }); // Di chuyển bản đồ đến vị trí hiện tại
            map.setZoom(12);

            // Xóa marker hiện tại nếu có
            if (currentLocationMarker) {
                currentLocationMarker.setMap(null);
            }

            // Tạo marker mới tại vị trí hiện tại
            currentLocationMarker = new google.maps.Marker({
                position: { lat: lat, lng: lng },
                map: map,
                title: 'Bạn ở đây'
            });

            // Hiển thị cửa sổ thông tin trên marker
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

// Hàm xử lý sự kiện khi DOM đã tải xong
document.addEventListener('DOMContentLoaded', function() {
    var formContainer = document.getElementById("form-container");
    formContainer.style.display = "none"; // Ẩn form ban đầu

    // Lắng nghe sự kiện click vào nút chuyển đổi hiển thị form
    document.getElementById("toggle-form-btn").addEventListener("click", function() {
        if (formContainer.style.display === "none") {
            formContainer.style.display = "block";
        } else {
            formContainer.style.display = "none";
        }
    });
});
