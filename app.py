import streamlit as st
import streamlit.components.v1 as components

# 1. Cấu hình trang (Phải là dòng đầu tiên)
st.set_page_config(page_title="Plantrees Game", layout="wide")

# 2. Xóa bỏ các khoảng cách thừa của Streamlit để giao diện đẹp hơn
st.markdown("""
    <style>
    .main > div { padding-top: 0rem; }
    iframe { border: none !important; }
    </style>
""", unsafe_allow_html=True)

# 3. Nội dung HTML (Đã làm sạch các ký tự đặc biệt)
html_content = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <script src="https://www.gstatic.com/firebasejs/8.10.0/firebase-app.js"></script>
    <script src="https://www.gstatic.com/firebasejs/8.10.0/firebase-auth.js"></script>
    <script src="https://www.gstatic.com/firebasejs/8.10.0/firebase-database.js"></script>
    <style>
        body { 
            background-color: #e8f5e9; 
            font-family: 'Segoe UI', sans-serif;
            display: flex; justify-content: center; align-items: center;
            height: 100vh; margin: 0;
        }
        .login-card {
            background: white; padding: 40px; border-radius: 25px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.1);
            width: 320px; text-align: center;
        }
        h1 { color: #2e7d32; margin-bottom: 20px; }
        input { 
            width: 100%; padding: 12px; margin: 8px 0;
            border: 1px solid #ddd; border-radius: 10px; outline: none;
        }
        button {
            width: 100%; padding: 12px; background: #2e7d32;
            color: white; border: none; border-radius: 10px;
            font-weight: bold; cursor: pointer; margin-top: 10px;
        }
        .toggle { color: #2e7d32; font-size: 13px; margin-top: 15px; cursor: pointer; }
    </style>
</head>
<body>
    <div class="login-card">
        <h1>Plantrees</h1>
        <div id="stat">ĐĂNG NHẬP</div>
        <input type="text" id="user" placeholder="Tên hiển thị" style="display:none">
        <input type="email" id="mail" placeholder="Email">
        <input type="password" id="pw" placeholder="Mật khẩu">
        <button onclick="authAction()" id="btn">XÁC NHẬN</button>
        <div class="toggle" onclick="swap()">Chưa có tài khoản? Đăng ký</div>
        <div id="msg" style="color:red; font-size:12px; margin-top:10px"></div>
    </div>

    <script>
        const config = {
            apiKey: "AIzaSyAASOFywyAkx2G7ubR_XsODI1U2x7mSMpE",
            authDomain: "plantrees-b1d99.firebaseapp.com",
            databaseURL: "https://plantrees-b1d99-default-rtdb.asia-southeast1.firebasedatabase.app",
            projectId: "plantrees-b1d99",
            storageBucket: "plantrees-b1d99.firebasestorage.app",
            messagingSenderId: "208821406000",
            appId: "1:208821406000:web:b4fac89c9a2f65d739e0f5"
        };
        firebase.initializeApp(config);
        
        let mode = "login";
        function swap() {
            mode = (mode === "login") ? "reg" : "login";
            document.getElementById("user").style.display = (mode === "reg") ? "block" : "none";
            document.getElementById("stat").innerText = (mode === "reg") ? "ĐĂNG KÝ" : "ĐĂNG NHẬP";
        }

        async function authAction() {
            const e = document.getElementById("mail").value;
            const p = document.getElementById("pw").value;
            const n = document.getElementById("user").value;
            const m = document.getElementById("msg");
            m.innerText = "Đang xử lý...";

            try {
                if(mode === "login") {
                    await firebase.auth().signInWithEmailAndPassword(e, p);
                    alert("Chào mừng bạn quay lại!");
                } else {
                    const r = await firebase.auth().createUserWithEmailAndPassword(e, p);
                    await firebase.database().ref('users/' + r.user.uid).set({ name: n, water: 0 });
                    alert("Đăng ký xong! Hãy đăng nhập.");
                    location.reload();
                }
            } catch(err) { m.innerText = err.message; }
        }
    </script>
</body>
</html>
"""

# 4. Hiển thị với chiều cao lớn
components.html(html_content, height=800)
