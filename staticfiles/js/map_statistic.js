var map, markers = [], infoWindows = [];

// Hàm khởi tạo bản đồ
function initMap() {
    // Tạo đối tượng bản đồ Google Maps
    map = new google.maps.Map(document.getElementById('map'), {
        center: { lat: 22.1261475, lng: 105.8329401 }, // Tọa độ trung tâm bản đồ
        zoom: 9.6, // Mức độ phóng to của bản đồ
        mapTypeControl: false, // Loại bỏ nút Map/Satellite
        streetViewControl: false, // Loại bỏ hình người (Street View)
        zoomControl: false, // Loại bỏ nút phóng to/thu nhỏ
        fullscreenControl: false // Loại bỏ nút toàn màn hình
    });

    // Kiểm tra xem locations có phải là mảng không
    if (!Array.isArray(locations)) {
        console.error("Lỗi: Dữ liệu locations không phải là mảng!", locations);
        return;
    }

    // Định nghĩa các biểu tượng cho các loại sự cố
    const icons = {
        'fire': '/static/images/fire_icon.png',
        'drowning': '/static/images/drowning_icon.jpg',
        'natural_disaster': '/static/images/natural_disaster_icon.png',
        'traffic_accident': '/static/images/traffic_accident_icon.png',
        'default': '/static/images/SOS.jpg'
    };

    // Định nghĩa các loại sự cố và ánh xạ sang tiếng Việt
    const incidentTypeMap = {
        'traffic_accident': 'Tai nạn giao thông',
        'drowning': 'Đuối nước',
        'fire': 'Cháy',
        'natural_disaster': 'Thiên tai'
    };

    // Tạo các marker cho từng địa điểm trong mảng locations
    locations.forEach((location) => {
        const iconUrl = icons[location.incident_type] || icons['default'];
        const marker = new google.maps.Marker({
            position: { lat: location.latitude, lng: location.longitude },
            icon: {
                url: iconUrl,
                scaledSize: new google.maps.Size(40, 40)
            },
            title: location.name
        });

        // Lưu trữ marker trong đối tượng location
        location.marker = marker;

        // Sử dụng địa chỉ từ cơ sở dữ liệu
        const address = location.address;
        const incidentType = incidentTypeMap[location.incident_type] || location.incident_type;
        let infoContent = `
            <div style="color: black; font-size: 12.5px;">
                <strong style="display: block; margin-bottom: 5px;">Họ tên: ${location.name}</strong>
                <p style="margin-bottom: 5px;">Đi động: ${location.mobile}</p>
                <p style="margin-bottom: 5px;">Sự cố: ${incidentType}</p>
                <p style="margin-bottom: 5px;">Điạ điểm: ${address}</p>
                <p style="margin-bottom: 5px;"><a href="https://www.google.com/maps/search/?api=1&query=${location.latitude},${location.longitude}" target="_blank">Xem trên Google Maps</a></p>
        `;

        // Kiểm tra quyền và trạng thái của sự cố để hiển thị nút "Đã giải quyết"
        console.log('userHasPermission:', userHasPermission);
        console.log('location.status:', location.status);

        if (userHasPermission) {
            infoContent += `
                <button class="btn btn-success" onclick="markAsResolved(${location.id})">Giải quyết xong</button>
            `;
        }

        console.log('infoContent:', infoContent);

        infoContent += `</div>`;
        marker.infoContent = infoContent;

        // Thêm mã để hiển thị infoContent trên bản đồ
        // click để hiện thông tin marker
        marker.addListener('click', () => {
            closeAllInfoWindows();
            const infoWindow = new google.maps.InfoWindow({ content: marker.infoContent });
            infoWindow.open(map, marker);
            infoWindows.push(infoWindow);
        });

        markers.push(marker);
    });

    // Sử dụng MarkerClusterer để nhóm các marker lại với nhau
    const markerCluster = new MarkerClusterer(map, markers, {
      imagePath: "/static/images/markerclusterer/m",
      gridSize: 1, // Điều chỉnh giá trị này để tăng hoặc giảm khoảng cách nhóm các marker
      maxZoom: 1500, // Mức độ phóng to tối đa mà các marker sẽ được nhóm lại với nhau
      minimumClusterSize: 2, // Số lượng marker tối thiểu cần thiết để tạo thành một cụm
    });
}

// Hàm đóng tất cả các InfoWindow
function closeAllInfoWindows() {
    infoWindows.forEach(infoWindow => infoWindow.close());
    infoWindows = [];
}

// Hàm hiển thị thông tin tất cả các marker theo loại sự cố
function showAllMarkersInfo(type) {
    closeAllInfoWindows();
    markers.forEach(marker => {
        if (marker.icon.url.includes(type)) {
            const infoWindow = new google.maps.InfoWindow({ content: marker.infoContent });
            infoWindow.open(map, marker);
            infoWindows.push(infoWindow);
        }
    });

    if (infoWindows.length === 0) {
        alert('Không có.');
    }
}

// Hàm bật/tắt menu SOS
function toggleSOSMenu() {
    document.getElementById('sosMenu').classList.toggle('show');
}

// Hàm đánh dấu sự cố là đã giải quyết
function markAsResolved(locationId) {
    // Gửi yêu cầu AJAX để cập nhật trạng thái của sự cố
    fetch(`/resolve_incident/${locationId}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({ status: 'rescued' })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Sự cố được đánh dấu giải quyết xong!');
            // Ẩn marker tương ứng
            const location = locations.find(loc => loc.id === locationId);
            if (location && location.marker) {
                location.marker.setMap(null);
            }
        } else {
            alert('Có lỗi xảy ra.');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Có lỗi xảy ra.');
    });
}

// Hàm lấy giá trị của cookie
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
