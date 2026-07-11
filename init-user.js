/**
 * File: init-user.js
 * Chức năng: Tự động kiểm tra và khởi tạo dữ liệu 3 bình nước cho người dùng mới.
 */

// Lắng nghe trạng thái đăng nhập của Firebase
firebase.auth().onAuthStateChanged((user) => {
    if (user) {
        const uid = user.uid;
        const dbRef = firebase.database().ref('users/' + uid);

        // Kiểm tra xem dữ liệu user đã tồn tại trên Database chưa
        dbRef.once('value').then((snapshot) => {
            if (!snapshot.exists()) {
                console.log("Phát hiện người dùng mới! Đang khởi tạo 3 bình nước...");
                
                // Khởi tạo các thông số mặc định cho tài khoản mới tinh
                dbRef.set({
                    name: user.displayName || "Người làm vườn mới",
                    email: user.email || "",
                    avatarUrl: user.photoURL || "https://cdn-icons-png.flaticon.com/512/4333/4333609.png",
                    coins: 0,
                    
                    // Cấu hình nước ban đầu theo yêu cầu
                    currentWater: 3, 
                    maxWater: 3,     
                    
                    // Cấu hình cấp độ và tốc độ hồi nước (1 tiếng/giọt)
                    regenSpeed: 3600,
                    speedLevel: 1,
                    storageLevel: 1,
                    waterLevel: 0,
                    
                    // Đồng bộ thời gian server Firebase để kích hoạt bộ đếm ngay
                    lastRegenTime: firebase.database.ServerValue.TIMESTAMP
                }).then(() => {
                    console.log("Khởi tạo tài khoản thành công! Sẵn sàng chơi.");
                }).catch((error) => {
                    console.error("Lỗi khi ghi dữ liệu người dùng mới:", error);
                });
            } else {
                console.log("Người dùng cũ đã có dữ liệu. Bỏ qua bước khởi tạo.");
            }
        });
    }
});
