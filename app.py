import streamlit as st
import streamlit.components.v1 as components

# Cấu hình trang - Đặt ngay đầu file
st.set_page_config(page_title="Plantrees - Login", layout="centered")

# CSS để fix lỗi khoảng trắng của Streamlit
st.markdown("""
    <style>
    iframe {border-radius: 15px;}
    .main {background-color: #e8f5e9;}
    </style>
""", unsafe_allow_html=True)

# Code HTML chuẩn đã được làm sạch
html_code = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <script src="https://www.gstatic.com/firebasejs/8.10.0/firebase-app.js"></script>
    <script src="https://www.gstatic.com/firebasejs/8.10.0/firebase-auth.js"></script>
    <script src="https://www.gstatic.com/firebasejs/8.10.0/firebase-database.js"></script>
    <style>
        :root { --primary: #2e7d32; --bg: #e8f5e9; }
        body { 
            font-family: sans-serif; 
            background: #e8f5e9;
            display: flex; justify-content: center; align-items: center; 
            margin: 0; padding: 20px;
        }
        .box { 
            background: white; padding: 30px; border-radius: 20px; 
            box-shadow: 0 4px 15px rgba(0,0,0,0.1); 
            width: 300px; text-align: center;
        }
        .brand { font-size: 32px; font-weight: bold; color: var(--primary); margin-bottom: 10px; }
        input { 
            width: 100%; padding: 12px; margin: 5px 0;
            border: 1px solid #ddd; border-radius: 8px; box-sizing: border-box;
        }
        button { 
            width: 100%; padding: 12px; background: var(--primary); 
            color: white; border: none; border-radius: 8px; cursor: pointer; font-weight: bold;
        }
        .link { color: var(--primary); font-size: 13px; cursor: pointer; margin-top: 15px; display: block; }
        #error { color: red; font-size: 12px; margin-top: 10px; }
    </style>
</head>
<body>
    <div class="box">
        <div class="brand">Plantrees</div>
        <div id="title" style="margin-bottom: 15px; color: #666;">ĐĂNG NHẬP</div>
        
        <input type="text" id="username" placeholder="Tên tài khoản" style="display: none;">
        <input type="email" id="email" placeholder="Email">
        <input type="password" id="pass" placeholder="Mật khẩu">
        
        <button onclick="handleAuth()" id="btnSubmit" style="margin-top: 10px;">ĐĂNG NHẬP</button>
        <div id="error"></div>
        <div class="link" onclick="switchMode()" id="toggleTxt">Chưa có tài khoản? Đăng ký ngay</div>
    </div>

    <script>
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
        const name = document.getElementById("username").value.trim();
        const err = document.getElementById("error");

        if(!email || !pass) { err.innerText = "Điền đủ Email và Pass!"; return; }
        err.innerText = "Đang xử lý...";

        try {
            if (isLogin) {
                await auth.signInWithEmailAndPassword(email, pass);
                alert("Đăng nhập thành công!");
            } else {
                if(!name) { err.innerText = "Điền tên tài khoản!"; return; }
                const res = await auth.createUserWithEmailAndPassword(email, pass);
                await res.user.updateProfile({ displayName: name });
                await db.ref('users/' + res.user.uid).set({
                    name: name,
                    waterCount: 0,
                    createdAt: Date.now()
                });
                alert("Đăng ký thành công!");
                switchMode();
            }
        } catch (e) { err.innerText = e.message; }
    }
    </script>
</body>
</html>
"""

# Hiển thị ứng dụng
components.html(html_code, height=700, scrolling=False)
