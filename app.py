import streamlit as st
import streamlit.components.v1 as components

# Cấu hình trang
st.set_page_config(page_title="Plantrees Auth", layout="centered")

# Khởi tạo trạng thái đăng nhập
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_name" not in st.session_state:
    st.session_state.user_name = ""

# Ẩn các thành phần thừa
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    iframe {border-radius: 25px; border: none;}
    </style>
""", unsafe_allow_html=True)

# Giao diện HTML của Duy đã được sửa logic chuyển trang
html_auth = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <script src="https://www.gstatic.com/firebasejs/8.10.0/firebase-app.js"></script>
    <script src="https://www.gstatic.com/firebasejs/8.10.0/firebase-auth.js"></script>
    <script src="https://www.gstatic.com/firebasejs/8.10.0/firebase-database.js"></script>
    <style>
        :root { --primary: #2e7d32; --accent: #4caf50; --bg: #f4f7f4; }
        body { font-family: 'Segoe UI', sans-serif; background: var(--bg); display: flex; justify-content: center; align-items: center; height: 90vh; margin: 0; }
        .box { background: white; padding: 40px; border-radius: 30px; box-shadow: 0 15px 35px rgba(0,0,0,0.05); width: 320px; text-align: center; }
        .brand-name { font-size: 38px; font-weight: 900; color: var(--primary); letter-spacing: -1.5px; margin-bottom: 30px; }
        input { width: 100%; padding: 15px; border: 2px solid #f0f0f0; border-radius: 15px; margin-bottom: 12px; box-sizing: border-box; outline: none; transition: 0.3s; }
        input:focus { border-color: var(--accent); }
        button.main { width: 100%; padding: 16px; background: var(--primary); color: white; border: none; border-radius: 15px; cursor: pointer; font-weight: 800; font-size: 16px; margin-top: 10px; box-shadow: 0 8px 20px rgba(46,125,50,0.2); }
        .link { margin-top: 20px; font-size: 13px; color: var(--primary); cursor: pointer; font-weight: 700; }
        #error { color: #ff5252; font-size: 12px; margin-top: 15px; font-weight: 600; display: none; }
    </style>
</head>
<body>
<div class="box">
    <div class="brand-name">PLANTREES</div>
    <input type="text" id="username" placeholder="Tên người làm vườn" style="display: none;">
    <input type="email" id="email" placeholder="Email">
    <input type="password" id="pass" placeholder="Mật khẩu">
    <button class="main" onclick="handleAuth()" id="btnSubmit">ĐĂNG NHẬP</button>
    <div id="error"></div>
    <div class="link" onclick="switchMode()" id="toggleTxt">Chưa có tài khoản? Đăng ký</div>
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
    document.getElementById("btnSubmit").innerText = isLogin ? "ĐĂNG NHẬP" : "ĐĂNG KÝ";
    document.getElementById("username").style.display = isLogin ? "none" : "block";
}

async function handleAuth() {
    const email = document.getElementById("email").value;
    const pass = document.getElementById("pass").value;
    const nickname = document.getElementById("username").value;
    const err = document.getElementById("error");
    err.style.display = "block";
    err.innerText = "Đang kiểm tra...";

    try {
        let user;
        if (isLogin) {
            const res = await auth.signInWithEmailAndPassword(email, pass);
            user = res.user.displayName || res.user.email;
        } else {
            const res = await auth.createUserWithEmailAndPassword(email, pass);
            const nameCheck = await db.ref('users').orderByChild('name').equalTo(nickname).once('value');
            if (nameCheck.exists()) {
                await res.user.delete();
                err.innerText = "Tên này đã tồn tại!";
                return;
            }
            await res.user.updateProfile({ displayName: nickname });
            await db.ref('users/' + res.user.uid).set({ name: nickname, email: email, waterLevel: 0 });
            user = nickname;
        }
        
        // QUAN TRỌNG: Gửi tín hiệu về cho Streamlit thay vì chuyển trang bằng index.html
        window.parent.postMessage({
            type: "streamlit:auth_success",
            username: user
        }, "*");
        
    } catch (e) { err.innerText = e.message; }
}
</script>
</body>
</html>
"""

# Hiển thị hoặc Login hoặc Game
if not st.session_state.logged_in:
    # Nhúng HTML và lắng nghe sự kiện từ iframe
    components.html(html_auth, height=550)
    
    # Một chút "mẹo" để bắt sự kiện từ JS trong Streamlit
    # Duy có thể dùng nút này để giả lập chuyển trang sau khi JS báo thành công
    if st.button("Xác nhận vào vườn 🌿"):
        st.session_state.logged_in = True
        st.rerun()
else:
    # Đây chính là phần "index.html" của Duy
    st.title(f"🌱 Chào mừng, {st.session_state.user_name}!")
    st.write("Bạn đã đăng nhập thành công vào hệ thống Plantrees.")
    
    if st.button("Đăng xuất"):
        st.session_state.logged_in = False
        st.rerun()
