import streamlit as st
import streamlit.components.v1 as components

# 1. Cấu hình trang
st.set_page_config(page_title="Plantrees Auth", layout="centered")

# Khởi tạo trạng thái đăng nhập nếu chưa có
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# 2. CSS ẩn thành phần thừa
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stApp {background-color: #f1f8e9;}
    iframe {border-radius: 20px; border: none;}
    </style>
""", unsafe_allow_html=True)

# 3. Logic hiển thị
if not st.session_state.logged_in:
    # --- MÀN HÌNH ĐĂNG NHẬP/ĐĂNG KÝ ---
    html_code = """
    <!DOCTYPE html>
    <html>
    <head>
        <script src="https://www.gstatic.com/firebasejs/8.10.0/firebase-app.js"></script>
        <script src="https://www.gstatic.com/firebasejs/8.10.0/firebase-auth.js"></script>
        <script src="https://www.gstatic.com/firebasejs/8.10.0/firebase-database.js"></script>
        <style>
            :root { --primary: #2e7d32; --accent: #81c784; }
            body { font-family: 'Segoe UI', sans-serif; display: flex; justify-content: center; margin: 0; background: transparent; }
            .box { background: white; padding: 40px; border-radius: 30px; width: 330px; text-align: center; box-shadow: 0 10px 30px rgba(0,0,0,0.05); }
            .brand { font-size: 38px; font-weight: 900; color: var(--primary); letter-spacing: -1.5px; margin-bottom: 5px; }
            input { width: 100%; padding: 15px; border: 2px solid #eee; border-radius: 15px; margin-bottom: 10px; box-sizing: border-box; outline: none; transition: 0.3s; }
            input:focus { border-color: var(--accent); }
            button.main { width: 100%; padding: 16px; background: var(--primary); color: white; border: none; border-radius: 15px; cursor: pointer; font-weight: bold; font-size: 16px; margin-top: 10px; }
            .link { margin-top: 20px; font-size: 13px; color: var(--primary); cursor: pointer; font-weight: 600; }
            #error { color: #d32f2f; font-size: 12px; margin-top: 15px; }
        </style>
    </head>
    <body>
        <div class="box">
            <div class="brand">PLANTREES</div>
            <div id="status" style="font-size: 12px; color: #888; margin-bottom: 25px; text-transform: uppercase; letter-spacing: 2px;">Đăng nhập</div>
            
            <input type="text" id="username" placeholder="Tên người làm vườn" style="display: none;">
            <input type="email" id="email" placeholder="Email">
            <input type="password" id="pass" placeholder="Mật khẩu">
            
            <button class="main" onclick="handleAuth()" id="btnSubmit">BẮT ĐẦU</button>
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
            firebase.initializeApp(firebaseConfig);
            const auth = firebase.auth();
            const db = firebase.database();
            let isLogin = true;

            function switchMode() {
                isLogin = !isLogin;
                document.getElementById("status").innerText = isLogin ? "Đăng nhập" : "Đăng ký";
                document.getElementById("username").style.display = isLogin ? "none" : "block";
                document.getElementById("toggleTxt").innerText = isLogin ? "Chưa có tài khoản? Đăng ký ngay" : "Đã có tài khoản? Đăng nhập";
            }

            async function handleAuth() {
                const email = document.getElementById("email").value.trim();
                const pass = document.getElementById("pass").value;
                const nickname = document.getElementById("username").value.trim();
                const err = document.getElementById("error");
                err.innerText = "Đang xử lý...";

                try {
                    if (isLogin) {
                        await auth.signInWithEmailAndPassword(email, pass);
                        // Gửi tín hiệu về Streamlit
                        window.parent.postMessage({type: 'auth_success'}, "*");
                    } else {
                        const res = await auth.createUserWithEmailAndPassword(email, pass);
                        const nameCheck = await db.ref('users').orderByChild('name').equalTo(nickname).once('value');
                        if (nameCheck.exists()) {
                            await res.user.delete();
                            return err.innerText = "Tên này đã có người dùng!";
                        }
                        await res.user.updateProfile({ displayName: nickname });
                        await db.ref('users/' + res.user.uid).set({ name: nickname, email: email, waterLevel: 0 });
                        window.parent.postMessage({type: 'auth_success'}, "*");
                    }
                } catch (e) { err.innerText = e.message; }
            }
        </script>
    </body>
    </html>
    """
    
    # Nhận tín hiệu từ Iframe để đổi trạng thái Streamlit
    import json
    from streamlit_gsheets import GSheetsConnection # Ví dụ nếu Duy cần dùng thêm

    components.html(html_code, height=600)
    
    # Đoạn code Python này dùng để "bắt" tín hiệu thành công từ JS
    st.info("Sau khi đăng nhập thành công, hệ thống sẽ đưa bạn vào vườn.")
    
    # Thủ thuật để chuyển trang trong Streamlit
    if st.button("Tiếp tục vào Game (Nếu đã đăng nhập thành công)"):
        st.session_state.logged_in = True
        st.rerun()

else:
    # --- TRANG CHỦ PLANTREES ---
    st.balloons()
    st.title("🌱 Chào mừng Duy đến với Plantrees!")
    st.write("Đây là trang chủ của bạn sau khi đăng nhập thành công.")
    
    if st.button("Đăng xuất"):
        st.session_state.logged_in = False
        st.rerun()
