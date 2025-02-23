import streamlit as st
import secure_file_encryption.auth as auth
import secure_file_encryption.encryption as encryption
import secure_file_encryption.database as db
import os

# Ensure the user_data directory exists
if not os.path.exists("user_data"):
    os.makedirs("user_data")

# App title
st.set_page_config(page_title="SecureVault", page_icon="🔒")

# Check login status
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
    st.session_state["username"] = None

def main():
    if not st.session_state["logged_in"]:
        # Show login or register page
        menu = st.radio("SecureVault", ["Login", "Create Account"])
        
        if menu == "Login":
            username = auth.user_login()
            if username:
                st.session_state["logged_in"] = True
                st.session_state["username"] = username
        
        elif menu == "Create Account":
            auth.create_account()

    else:
        # Once logged in, show Profile + Encrypt/Decrypt options
        st.sidebar.title(f"👤 {st.session_state['username']}'s Profile")
        menu = st.sidebar.radio("Navigation", ["Home", "Encrypt File", "Decrypt File", "Logout"])
        
        if menu == "Home":
            st.subheader(f"Welcome, {st.session_state['username']}!")
            user_files = db.load_user_files(st.session_state['username'])
            
            if user_files:
                st.write("📂 **Your Encrypted/Decrypted Files:**")
                for file in user_files:
                    st.write(f"🔹 {file['name']} - {file['type'].capitalize()}")
            else:
                st.info("No files found. Start encrypting!")

        elif menu == "Encrypt File":
            encrypt_file()

        elif menu == "Decrypt File":
            decrypt_file()

        elif menu == "Logout":
            st.session_state["logged_in"] = False
            st.session_state["username"] = None
            st.rerun()

# Encryption Function
def encrypt_file():
    st.subheader("🔐 Encrypt a File")
    uploaded_file = st.file_uploader("Upload a file to encrypt", type=["pdf", "docx", "pptx", "jpg", "png", "txt"])

    if uploaded_file:
        save_path = f"user_data/{st.session_state['username']}_{uploaded_file.name}"
        with open(save_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        encrypted_path = save_path + ".enc"
        encryption.encrypt_file(save_path, encrypted_path, st.session_state['username'])
        db.save_user_file(st.session_state['username'], uploaded_file.name, "encrypted")

        st.success("✅ File encrypted successfully!")
        st.download_button("Download Encrypted File", open(encrypted_path, "rb").read(), uploaded_file.name + ".enc")

# Decryption Function
def decrypt_file():
    st.subheader("🔓 Decrypt a File")
    encrypted_file = st.file_uploader("Upload an encrypted file to decrypt")

    if encrypted_file:
        entered_username = st.text_input("Enter your username:")
        
        if entered_username and st.button("Decrypt"):
            save_path = f"user_data/{entered_username}_{encrypted_file.name}"
            with open(save_path, "wb") as f:
                f.write(encrypted_file.getbuffer())

            decrypted_path = save_path.replace(".enc", "")
            success = encryption.decrypt_file(save_path, decrypted_path, entered_username)

            if success:
                db.save_user_file(entered_username, encrypted_file.name.replace(".enc", ""), "decrypted")
                st.success("✅ File decrypted successfully!")
                st.download_button("Download Decrypted File", open(decrypted_path, "rb").read(), decrypted_path)
            else:
                st.error("❌ Decryption failed. Check username or file integrity.")

if __name__ == "__main__":
    main()
