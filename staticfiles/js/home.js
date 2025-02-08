document.addEventListener("DOMContentLoaded", function() {
    AOS.init();
    const notificationElement = document.getElementById('notification');
    const closeButton = document.getElementById('close-notification');
    const detailsButton = document.getElementById('details-notification');
    const pendingPointsElement = document.getElementById('pending-points');
    const closePendingPointsButton = document.getElementById('close-pending-points');
    const detailsPendingPointsButton = document.getElementById('details-pending-points');
    const approvedPointsElement = document.getElementById('approved-points');
    const closeApprovedPointsButton = document.getElementById('close-approved-points');
    const detailsApprovedPointsButton = document.getElementById('details-approved-points');

    // Kết nối WebSocket
    const socket = new WebSocket('wss://' + window.location.host + '/ws/notifications/');

    socket.onopen = function(event) {
        console.log("WebSocket connection opened:", event);
    };

    socket.onerror = function(error) {
        console.error("WebSocket error:", error);
    };

    socket.onclose = function(event) {
        console.log("WebSocket connection closed:", event);
    };

    // Sự kiện khi nhận được thông điệp từ server qua WebSocket
    socket.onmessage = function(event) {
        console.log("Received data:", event.data);
        const data = JSON.parse(event.data);
        notificationElement.querySelector('span').innerText = data.message;
        notificationElement.style.display = 'block';
        notificationElement.style.opacity = '1';
        notificationElement.dataset.incidentId = data.incident_id; // Lưu ID vụ việc trong thuộc tính data

        // Tự động ẩn thông báo sau 10 giây
        setTimeout(() => {
            notificationElement.style.opacity = '0';
            setTimeout(() => {
                notificationElement.style.display = 'none';
            }, 500); // Thời gian chờ để hoàn thành hiệu ứng mờ đi
        }, 10000);
    };

    // Sự kiện click để chuyển hướng đến trang chi tiết điểm cứu trợ
    notificationElement.addEventListener('click', function() {
        const incidentId = notificationElement.dataset.incidentId;
        if (incidentId) {
            // Chuyển hướng đến trang chi tiết điểm cứu trợ
            window.location.href = `/incidents/${incidentId}/`;
        }
    });

    // Hiển thị thông báo điểm chờ duyệt và điểm đang giải quyết
    pendingPointsElement.style.display = 'block';
    pendingPointsElement.style.opacity = '1';
});