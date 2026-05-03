import streamlit as st
import streamlit.components.v1 as components

# Cấu hình trang Streamlit
st.set_page_config(page_title="Plantrees Auth", layout="centered")

# Nhúng CSS để ẩn các thành phần thừa của Streamlit
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    iframe {border-radius: 15px;}
    </style>
""", unsafe_allow_html=True)

html_code = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Xác thực - Plantrees</title>
    <script src="https://www.gstatic.com/firebasejs/8.10.0/firebase-app.js"></script>
    <script src="https://www.gstatic.com/firebasejs/8.10.0/firebase-auth.js"></script>
    <script src="https://www.gstatic.com/firebasejs/8.10.0/firebase-database.js"></script>
    <style>
        :root { --primary: #2e7d32; --accent: #81c784; --bg: #f1f8e9; }
        body { 
            font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; 
            background: var(--bg); 
            display: flex; justify-content: center; align-items: center; 
            height: 95vh; margin: 0; 
        }
        .box { 
            background: #ffffff; padding: 40px; border-radius: 24px; 
            box-shadow: 0 10px 40px rgba(0,0,0,0.08); 
            width: 340px; text-align: center; color: #333;
            transition: all 0.3s ease;
        }
        .brand-name { 
            font-size: 38px; font-weight: 900; margin-bottom: 5px; 
            background: linear-gradient(45deg, #2e7d32, #66bb6a); 
            -webkit-background-clip: text; -webkit-text-fill-color: transparent; 
            letter-spacing: -1px; 
        }
        #title { margin-top: 0; margin-bottom: 25px; font-size: 14px; color: #888; text-transform: uppercase; letter-spacing: 2px; }
        .input-group { position: relative; margin: 10px 0; }
        input { 
            width: 100%; padding: 14px; border: 2px solid #edf2f4; 
            border-radius: 12px; box-sizing: border-box; outline: none; 
            background: #f8faf9; color: #333; margin-bottom: 10px; 
            transition: 0.3s; font-size: 15px;
        }
        input:focus { border-color: var(--accent); background: #fff; box-shadow: 0 0 0 4px rgba(129, 199, 132, 0.1); }
        .show-btn { 
            position: absolute; right: 12px; top: 12px; background: #e8f5e9; 
            border: none; padding: 6px 10px; border-radius: 8px; 
            font-size: 10px; cursor: pointer; color: var(--primary); font-weight: bold;
        }
        button.main { 
            width: 100%; padding: 14px; background: var(--primary); color: #fff; 
            border: none; border-radius: 12px; cursor: pointer; 
            font-weight: bold; margin-top: 15px; font-size: 16px;
            box-shadow: 0 4px 12px rgba(46, 125, 50, 0.2); transition: 0.3s;
        }
        button.main:hover { background: #1b5e20; transform: translateY(-2px); }
        .link { margin-top: 20px; font-size: 14px; color: var(--primary); cursor: pointer; font-weight: 600; }
        .forgot { display: block; text-align: right; font-size: 12px; color: #999; margin-bottom: 12px; text-decoration: none; cursor: pointer; transition: 0.3s; }
        .forgot:hover { color: var(--primary); }
        #error { color: #e53935; font-size: 13px; margin-top: 15px; font-weight: 500; min-height: 18px; }
    </style>
</head>
<body>
<div class="box">
    <div class="brand-name">Plantrees</div>
    <h2 id="title">ĐĂNG NHẬP</h2>
    
    <input type="text" id="username" placeholder="Tên hiển thị (Duy nhất)" style="display: none;">
    <input type="email" id="email" placeholder="Email của bạn">
    
    <div class="input-group">
        <input type="password" id="pass" placeholder="Mật khẩu">
        <button class="show-btn" onclick="togglePass()">HIỆN</button>
    </div>

    <a class="forgot" id="forgotBtn" onclick="forgotPass()">Quên mật khẩu?</a>

    <button class="main" onclick="handleAuth()" id="btnSubmit">ĐĂNG NHẬP</button>
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

function togglePass() {
    const p = document.getElementById("pass");
    p.type = p.type === "password" ? "text" : "password";
    event.target.innerText = p.type === "password" ? "HIỆN" : "ẨN";
}

function switchMode() {
    isLogin = !isLogin;
    const box = document.querySelector('.box');
    document.getElementById("title").innerText = isLogin ? "ĐĂNG NHẬP" : "ĐĂNG KÝ";
    document.getElementById("btnSubmit").innerText = isLogin ? "ĐĂNG NHẬP" : "ĐĂNG KÝ";
    document.getElementById("toggleTxt").innerText = isLogin ? "Chưa có tài khoản? Đăng ký ngay" : "Đã có tài khoản? Đăng nhập";
    document.getElementById("username").style.display = isLogin ? "none" : "block";
    document.getElementById("forgotBtn").style.display = isLogin ? "block" : "none";
    document.getElementById("error").innerText = "";
}

async function forgotPass() {
    const email = document.getElementById("email").value;
    if (!email) return alert("Vui lòng nhập Email!");
    try {
        await auth.sendPasswordResetEmail(email);
        alert("Link đặt lại mật khẩu đã được gửi vào Email!");
    } catch (e) { alert("Lỗi: " + e.message); }
}

async function handleAuth() {
    const email = document.getElementById("email").value.trim();
    const pass = document.getElementById("pass").value;
    const nickname = document.getElementById("username").value.trim();
    const err = document.getElementById("error");
    
    if(!email || !pass || (!isLogin && !nickname)) return err.innerText = "Vui lòng điền đủ thông tin!";
    err.innerText = "Đang xử lý...";

    try {
        if (isLogin) {
            await auth.signInWithEmailAndPassword(email, pass);
            alert("Đăng nhập thành công!");
            // window.location.href = "game.html"; 
        } else {
            if (nickname.length < 3) return err.innerText = "Tên phải từ 3 ký tự!";

            // 1. Tạo tài khoản
            const res = await auth.createUserWithEmailAndPassword(email, pass);
            
            // 2. Kiểm tra tên trùng trong database
            const nameCheck = await db.ref('users').orderByChild('name').equalTo(nickname).once('value');
            if (nameCheck.exists()) {
                await res.user.delete();
                return err.innerText = "Tên này đã có người sử dụng!";
            }

            // 3. Lưu thông tin
            await res.user.updateProfile({ displayName: nickname });
            await db.ref('users/' + res.user.uid).set({
                name: nickname,
                email: email,
                waterLevel: 0,
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

components.html(html_code, height=650)
