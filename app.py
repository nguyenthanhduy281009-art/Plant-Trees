import streamlit as st
import streamlit.components.v1 as components

# Cấu hình trang Streamlit
st.set_page_config(page_title="Plantrees - Hệ thống xác thực", layout="centered")

# Đây là toàn bộ code HTML/JS của bạn
# Tôi đã tích hợp Firebase v8 để khớp với logic cũ của bạn
html_code = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Plantrees - Chăm sóc cây</title>
    <script src="https://www.gstatic.com/firebasejs/8.10.0/firebase-app.js"></script>
    <script src="https://www.gstatic.com/firebasejs/8.10.0/firebase-auth.js"></script>
    <script src="https://www.gstatic.com/firebasejs/8.10.0/firebase-database.js"></script>
    <style>
        :root { --primary: #2e7d32; --secondary: #81c784; --bg: #e8f5e9; }
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            background: linear-gradient(135deg, var(--bg) 0%, #dcedc8 100%); 
            display: flex; justify-content: center; align-items: center; 
            height: 90vh; margin: 0; overflow: hidden;
        }
        .box { 
            background: #ffffff; padding: 30px; border-radius: 20px; 
            box-shadow: 0 10px 30px rgba(0,0,0,0.1); width: 100%; max-width: 320px; 
            text-align: center; color: #333;
        }
        .brand-name { 
            font-size: 36px; font-weight: 800; margin-bottom: 5px; 
            background: linear-gradient(45deg, var(--primary), var(--secondary)); 
            -webkit-background-clip: text; -webkit-text-fill-color: transparent; 
        }
        #title { margin: 0 0 20px 0; font-size: 18px; color: #666; font-weight: 500; }
        input { 
            width: 100%; padding: 12px; border: 2px solid #f0f0f0; 
            border-radius: 10px; box-sizing: border-box; outline: none; 
            background: #f9f9f9; margin-bottom: 10px; transition: 0.3s;
        }
        input:focus { border-color: var(--primary); background: #fff; }
        button.main { 
            width: 100%; padding: 12px; background: var(--primary); color: #fff; 
            border: none; border-radius: 10px; cursor: pointer; font-weight: bold; 
            font-size: 16px; transition: 0.3s;
        }
        button.main:hover { background: #1b5e20; }
        .link { margin-top: 15px; font-size: 13px; color: var(--primary); cursor: pointer; font-weight: 600; }
        #error { color: #d32f2f; font-size: 12px; margin-top: 10px; min-height: 15px; }
    </style>
</head>
<body>
<div class="box">
    <div class="brand-name">Plantrees</div>
    <h2 id="title">ĐĂNG NHẬP</h2>
    <input type="text" id="username" placeholder="Tên tài khoản (Duy nhất)" style="display: none;">
    <input type="email" id="email" placeholder="Email của bạn">
    <input type="password" id="pass" placeholder="Mật khẩu">
    <button class="main" onclick="handleAuth()" id="btnSubmit">ĐĂNG NHẬP</button>
    <div id="error"></div>
    <div class="link" onclick="switchMode()" id="toggleTxt">Chưa có tài khoản? Đăng ký ngay</div>
</div>

<script>
// --- DÁN MÃ CẤU HÌNH CỦA BẠN VÀO ĐÂY ---
const firebaseConfig = {
  apiKey: "AIzaSyAASOFywyAkx2G7ubR_XsODI1U2x7mSMpE",
  authDomain: "plantrees-b1d99.firebaseapp.com",
  databaseURL: "https://plantrees-b1d99-default-rtdb.asia-southeast1.firebasedatabase.app",
  projectId: "plantrees-b1d99",
  storageBucket: "plantrees-b1d99.firebasestorage.app",
  messagingSenderId: "208821406000",
  appId: "1:208821406000:web:b4fac89c9a2f65d739e0f5"
};

if (!firebase.apps.length) firebase.initializeApp(firebaseConfig);
const auth = firebase.auth();
const db = firebase.database();

let isLogin = true;

function switchMode() {
    isLogin = !isLogin;
    document.getElementById("title").innerText = isLogin ? "ĐĂNG NHẬP" : "ĐĂNG KÝ";
    document.getElementById("btnSubmit").innerText = isLogin ? "ĐĂNG NHẬP" : "ĐĂNG KÝ";
    document.getElementById("toggleTxt").innerText = isLogin ? "Chưa có tài khoản? Đăng ký ngay" : "Đã có tài khoản? Đăng nhập";
    document.getElementById("username").style.display = isLogin ? "none" : "block";
}

async function handleAuth() {
    const email = document.getElementById("email").value.trim();
    const pass = document.getElementById("pass").value;
    const nickname = document.getElementById("username").value.trim();
    const err = document.getElementById("error");
    
    if(!email || !pass || (!isLogin && !nickname)) {
        err.innerText = "Vui lòng điền đủ thông tin!";
        return;
    }
    err.innerText = "Đang xử lý...";

    try {
        if (isLogin) {
            await auth.signInWithEmailAndPassword(email, pass);
            alert("Đăng nhập thành công! Hệ thống đang chuyển hướng...");
            // window.location.href = "game.html"; // Sau này bạn đổi link này
        } else {
            const res = await auth.createUserWithEmailAndPassword(email, pass);
            await res.user.updateProfile({ displayName: nickname });
            await db.ref('users/' + res.user.uid).set({
                name: nickname,
                email: email,
                waterCount: 0,
                createdAt: Date.now()
            });
            alert("Đăng ký thành công!");
            isLogin = true;
            switchMode();
        }
    } catch (e) { err.innerText = e.message; }
}
</script>
</body>
</html>
"""

# Hiển thị HTML trong Streamlit
components.html(html_code, height=600)
