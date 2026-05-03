import streamlit as st
import streamlit.components.v1 as components

# Cấu hình trang tối giản
st.set_page_config(page_title="Plantrees", layout="centered")

# Nhúng HTML trực tiếp vào một khung cố định
html_code = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Plantrees</title>
    <!-- Tải Firebase từ CDN đáng tin cậy -->
    <script src="https://www.gstatic.com/firebasejs/8.10.0/firebase-app.js"></script>
    <script src="https://www.gstatic.com/firebasejs/8.10.0/firebase-auth.js"></script>
    <script src="https://www.gstatic.com/firebasejs/8.10.0/firebase-database.js"></script>
    
    <style>
        body { background: #e8f5e9; font-family: sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
        .card { background: white; padding: 30px; border-radius: 15px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); width: 280px; text-align: center; }
        input { width: 100%; padding: 10px; margin: 5px 0; border: 1px solid #ddd; border-radius: 5px; box-sizing: border-box; }
        button { width: 100%; padding: 10px; background: #2e7d32; color: white; border: none; border-radius: 5px; cursor: pointer; margin-top: 10px; font-weight: bold; }
        .msg { color: red; font-size: 11px; margin-top: 10px; }
    </style>
</head>
<body>
    <div class="card">
        <h2 style="color: #2e7d32; margin-top: 0;">Plantrees</h2>
        <div id="mode-text" style="font-size: 14px; color: #666; margin-bottom: 10px;">ĐĂNG NHẬP</div>
        <input type="text" id="nickname" placeholder="Tên của bạn" style="display:none">
        <input type="email" id="email" placeholder="Email">
        <input type="password" id="pass" placeholder="Mật khẩu">
        <button onclick="doAuth()" id="btnSubmit">XÁC NHẬN</button>
        <div style="font-size: 12px; margin-top: 15px; cursor: pointer; color: #2e7d32;" onclick="toggle()">Chưa có tài khoản? Đăng ký</div>
        <div id="error-msg" class="msg"></div>
    </div>

    <script>
        // Cấu hình Firebase của bạn
        const firebaseConfig = {
            apiKey: "AIzaSyAASOFywyAkx2G7ubR_XsODI1U2x7mSMpE",
            authDomain: "plantrees-b1d99.firebaseapp.com",
            databaseURL: "https://plantrees-b1d99-default-rtdb.asia-southeast1.firebasedatabase.app",
            projectId: "plantrees-b1d99",
            storageBucket: "plantrees-b1d99.firebasestorage.app",
            messagingSenderId: "208821406000",
            appId: "1:208821406000:web:b4fac89c9a2f65d739e0f5"
        };
        
        // Khởi tạo
        if (!firebase.apps.length) firebase.initializeApp(firebaseConfig);
        
        let isLoginMode = true;

        function toggle() {
            isLoginMode = !isLoginMode;
            document.getElementById("mode-text").innerText = isLoginMode ? "ĐĂNG NHẬP" : "ĐĂNG KÝ";
            document.getElementById("nickname").style.display = isLoginMode ? "none" : "block";
        }

        async function doAuth() {
            const email = document.getElementById("email").value;
            const pass = document.getElementById("pass").value;
            const nickname = document.getElementById("nickname").value;
            const err = document.getElementById("error-msg");
            err.innerText = "Đang xử lý...";

            try {
                if(isLoginMode) {
                    await firebase.auth().signInWithEmailAndPassword(email, pass);
                    alert("Đăng nhập thành công!");
                } else {
                    const res = await firebase.auth().createUserWithEmailAndPassword(email, pass);
                    await firebase.database().ref('users/' + res.user.uid).set({ name: nickname, points: 0 });
                    alert("Đăng ký thành công!");
                }
            } catch(e) {
                err.innerText = e.message;
            }
        }
    </script>
</body>
</html>
"""

# HIỂN THỊ: Sử dụng height đủ lớn và cho phép render scripts
components.html(html_code, height=600, scrolling=False)
