import streamlit as st
import base64
import base64 as b64

# ===== Caesar =====
def caesar_encrypt(text, shift=3):
    result = ""
    for char in text:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            result += chr((ord(char) - base + shift) % 26 + base)
        else:
            result += char
    return result

def caesar_decrypt(text, shift=3):
    return caesar_encrypt(text, -shift)

# ===== Vigenere =====
def vigenere_encrypt(text, key="kunci"):
    result = ""
    key = key.lower()
    j = 0
    for char in text:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            shift = ord(key[j % len(key)]) - ord('a')
            result += chr((ord(char) - base + shift) % 26 + base)
            j += 1
        else:
            result += char
    return result

def vigenere_decrypt(text, key="kunci"):
    result = ""
    key = key.lower()
    j = 0
    for char in text:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            shift = ord(key[j % len(key)]) - ord('a')
            result += chr((ord(char) - base - shift) % 26 + base)
            j += 1
        else:
            result += char
    return result

# ===== XOR & Block =====
def xor_encrypt(text, key="xor"):
    cipher_bytes = bytes([ord(c) ^ ord(key[i % len(key)]) for i, c in enumerate(text)])
    return b64.b64encode(cipher_bytes).decode()

def xor_decrypt(cipher, key="xor"):
    cipher_bytes = b64.b64decode(cipher.encode())
    plain = ''.join(chr(b ^ ord(key[i % len(key)])) for i, b in enumerate(cipher_bytes))
    return plain

def block_encrypt(text, key="1010"):
    key_bits = [int(b) for b in key]
    cipher_bytes = bytes([ch ^ key_bits[i % len(key_bits)] for i, ch in enumerate(text.encode())])
    return b64.b64encode(cipher_bytes).decode()

def block_decrypt(cipher, key="1010"):
    key_bits = [int(b) for b in key]
    cipher_bytes = b64.b64decode(cipher.encode())
    plain_bytes = bytes([b ^ key_bits[i % len(key_bits)] for i, b in enumerate(cipher_bytes)])
    return plain_bytes.decode(errors="ignore")

# ===== Super =====
def super_encrypt(text, shift, vkey, xkey, bkey):
    return block_encrypt(xor_encrypt(vigenere_encrypt(caesar_encrypt(text, shift), vkey), xkey), bkey)

def super_decrypt(cipher, shift, vkey, xkey, bkey):
    return caesar_decrypt(vigenere_decrypt(xor_decrypt(block_decrypt(cipher, bkey), xkey), vkey), shift)

# ===== Streamlit UI  =====
st.set_page_config(page_title="Aplikasi Kriptografi", layout="centered")

def load_css(file, bg_path=None):
    with open(file, "r") as f:
        css = f.read()
    if bg_path:
        with open(bg_path, "rb") as img:
            bg_base64 = base64.b64encode(img.read()).decode()
        css = css.replace("BG_IMAGE", bg_base64)
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

load_css("style.css", "image/lucu.jpg")

# ===== Helper: Card =====
def card(content_func):
    st.markdown('<div class="card-flag">', unsafe_allow_html=True)
    content_func()
    st.markdown('</div>', unsafe_allow_html=True)

# ===== Helper: Header Tengah =====
def render_header(title, with_icon=True):
    st.markdown(f"<h1 style='text-align:center;'>{title}</h1>", unsafe_allow_html=True)
    if with_icon:
        file_ = open("image/icon.jpg", "rb")
        data = file_.read()
        file_.close()
        encoded = base64.b64encode(data).decode()
        st.markdown(
            f"""
            <div style="text-align:center; margin-bottom:20px;">
                <img src="data:image/png;base64,{encoded}" 
                     width="200" 
                     style="border-radius:50%; margin-bottom:20px;">
            </div>
            """,
            unsafe_allow_html=True
        )

# ===== Nav Buttons =====
def render_nav_buttons(back_action=None, done_action=None):
    col1, col2 = st.columns(2)

    with col1:
        if st.button("⬅ Kembali", key="btn_kembali"):
            if back_action:
                back_action()
                st.rerun()

    with col2:
        if st.button("✅ Selesai", key="btn_selesai"):
            if done_action:
                done_action()
                st.rerun()

# ===== Session State =====
if "page" not in st.session_state:
    st.session_state.page = "home"
if "algorithm" not in st.session_state:
    st.session_state.algorithm = None
if "mode" not in st.session_state:
    st.session_state.mode = None

# ===== Halaman Home =====
if st.session_state.page == "home":
    def home_page():
        render_header("🔒 Aplikasi Enkripsi & Dekripsi")
        st.markdown('<div class="menu_tombol">', unsafe_allow_html=True)
        if st.button("Mulai", key="btn_mulai"):
            st.session_state.page = "menu"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    card(home_page)

# ===== Halaman Menu =====
elif st.session_state.page == "menu":
    def menu_page():
        render_header("🔒 Aplikasi Enkripsi & Dekripsi")
        st.markdown("### Pilih Algoritma:", unsafe_allow_html=True)
        st.markdown('<div class="menu_tombol">', unsafe_allow_html=True)
        st.button("1. Caesar Cipher", key="btn_caesar", on_click=lambda: st.session_state.update(algorithm="caesar", page="mode"))
        st.button("2. Vigenere Cipher", key="btn_vigenere", on_click=lambda: st.session_state.update(algorithm="vigenere", page="mode"))
        st.button("3. XOR Cipher", key="btn_xor", on_click=lambda: st.session_state.update(algorithm="xor", page="mode"))
        st.button("4. Block Cipher", key="btn_block", on_click=lambda: st.session_state.update(algorithm="block", page="mode"))
        st.button("5. Super Encryption", key="btn_super", on_click=lambda: st.session_state.update(algorithm="super", page="mode"))
        st.markdown('</div>', unsafe_allow_html=True)
        render_nav_buttons(
            back_action=lambda: st.session_state.update(page="home", algorithm=None),
            done_action=lambda: st.session_state.update(page="home", algorithm=None, mode=None)
        )
    card(menu_page)

# ===== Halaman Mode =====
elif st.session_state.page == "mode":
    def mode_page():
        algo = st.session_state.algorithm
        if not algo:
            st.session_state.page = "menu"
            st.rerun()

        render_header(f"Algoritma: {algo.upper()}", with_icon=False)
        st.markdown("### Pilih Mode:", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<div class="menu_tombol">', unsafe_allow_html=True)
            col1.button("Enkripsi", key="btn_encrypt", on_click=lambda: st.session_state.update(mode="encrypt", page="process"))
            st.markdown('</div>', unsafe_allow_html=True)
        with col2:
            st.markdown('<div class="menu_tombol">', unsafe_allow_html=True)
            col2.button("Dekripsi", key="btn_decrypt", on_click=lambda: st.session_state.update(mode="decrypt", page="process"))
            st.markdown('</div>', unsafe_allow_html=True)
        render_nav_buttons(
            back_action=lambda: st.session_state.update(page="menu", algorithm=None),
            done_action=lambda: st.session_state.update(page="home", algorithm=None, mode=None)
        )
    card(mode_page)

# ===== Halaman Proses =====
elif st.session_state.page == "process":
    algo = st.session_state.get("algorithm")
    mode = st.session_state.get("mode")

    def process_page():
        if not algo or not mode:
            st.warning("Silakan pilih algoritma dan mode dulu.")
            st.session_state.page = "menu"
            st.rerun()

        render_header(f"{mode.capitalize()} - {algo.upper()}", with_icon=False)
        text = st.text_area("Masukkan teks:")

        shift = vkey = xkey = bkey = None
        if algo == "caesar":
            shift = st.number_input("Masukkan shift:", min_value=-25, max_value=25, value=3)
        elif algo == "vigenere":
            vkey = st.text_input("Masukkan kunci Vigenere:", value="kunci")
        elif algo == "xor":
            xkey = st.text_input("Masukkan kunci XOR:", value="xor")
        elif algo == "block":
            bkey = st.text_input("Masukkan kunci Block (contoh: 1010):", value="1010")
        elif algo == "super":
            shift = st.number_input("Shift Caesar:", value=3)
            vkey = st.text_input("Kunci Vigenere:", value="kunci")
            xkey = st.text_input("Kunci XOR:", value="xor")
            bkey = st.text_input("Kunci Block:", value="1010")

        st.markdown('<div class="menu_tombol">', unsafe_allow_html=True)
        if st.button("Proses", key="btn_proses"):
            valid = True
            if algo in ["vigenere", "super"] and not vkey.isalpha():
                st.error("Kunci Vigenere harus alfabet")
                valid = False
            if algo in ["block", "super"] and not all(ch in "01" for ch in bkey):
                st.error("Kunci Block harus angka biner")
                valid = False

            if valid:
                result = None
                if algo == "caesar":
                    result = caesar_encrypt(text, shift) if mode == "encrypt" else caesar_decrypt(text, shift)
                elif algo == "vigenere":
                    result = vigenere_encrypt(text, vkey) if mode == "encrypt" else vigenere_decrypt(text, vkey)
                elif algo == "xor":
                    result = xor_encrypt(text, xkey) if mode == "encrypt" else xor_decrypt(text, xkey)
                elif algo == "block":
                    result = block_encrypt(text, bkey) if mode == "encrypt" else block_decrypt(text, bkey)
                elif algo == "super":
                    result = super_encrypt(text, shift, vkey, xkey, bkey) if mode == "encrypt" else super_decrypt(text, shift, vkey, xkey, bkey)

                if result:
                    st.success(f"Hasil: {result}")
        st.markdown('</div>', unsafe_allow_html=True)

        render_nav_buttons(
            back_action=lambda: st.session_state.update(page="mode", mode=None),
            done_action=lambda: st.session_state.update(page="home", algorithm=None, mode=None)
        )
    card(process_page)
