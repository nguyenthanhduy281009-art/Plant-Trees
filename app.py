import streamlit as st
import streamlit.components.v1 as components

# Cấu hình trang
st.set_page_config(page_title="Plantrees Game", layout="centered")

# Dán toàn bộ nội dung file HTML của bạn vào biến này
html_code = """
<!DOCTYPE html>
<html>
<head>
    <!-- Giữ nguyên toàn bộ code HTML, CSS và Script Plantrees của bạn ở đây -->
</head>
<body>
    <!-- Giữ nguyên phần thân trang -->
</body>
</html>
"""

# Hiển thị code HTML lên Streamlit
components.html(html_code, height=800, scrolling=True)
