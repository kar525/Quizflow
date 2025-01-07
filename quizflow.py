import streamlit as st
import google.generativeai as genai
import pandas as pd
import yaml
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth
import tempfile
import os
from fpdf import FPDF

showSidebarNavigation = False

if 'N' not in st.session_state:
    st.session_state['N'] = 0


    #login
with open('C:/Users/kaka/myenv/dads5001/login/1.YAML') as file:
    config = yaml.load(file, Loader=SafeLoader)

# Pre-hashing all plain text passwords once
# stauth.Hasher.hash_passwords(config['credentials'])

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)
try:
    authenticator.login()
except Exception as e:
    st.error(e)


        


if 'response_text' not in st.session_state:
    st.session_state['response_text'] = None  # เก็บผลลัพธ์

if 'N' not in st.session_state:
    st.session_state['N'] = 0  # กำหนดสถานะ N เป็น 0 ตอนเริ่มต้น

if 'response_text' not in st.session_state:
    st.session_state['response_text'] = None  # เก็บผลลัพธ์

if st.session_state['authentication_status']:
    authenticator.logout()
    A = st.session_state["username"]
    col1, col2, col3 = st.columns(3)
    with col2:
        st.markdown(f"<p style='font-size: 30px; color: black; font-weight: bold;'>🎉🎉🎉🎉🎉</p>", unsafe_allow_html=True)
        st.markdown(f"<p style='font-size: 30px; color: black; font-weight: bold;'>Welcome! {A}</p>", unsafe_allow_html=True)
    st.write(" ")

    # ถ้า N == 0 หมายถึงยังไม่ทำการอัพโหลดไฟล์และสร้างเนื้อหา
    if st.session_state['N'] == 0:
        uploaded_files = st.file_uploader("Choose a readable PDF file", type=["pdf"])  # ตัวอัพโหลดไฟล์ PDF
        if uploaded_files is not None:
            genai.configure(api_key="AIzaSyCbZ-5fC2ElkQfBBI2g1n3ZZNuxy400dGU")
            model = genai.GenerativeModel("gemini-1.5-flash")
            with st.spinner('In progress...'):
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
                    temp_file_path = temp_file.name
                    with open(temp_file_path, "wb") as f:
                        f.write(uploaded_files.read())
                pdf = genai.upload_file(temp_file_path)
                response = model.generate_content(["ช่วยให้ข้อสอบ 4 ช๊อส์จำนวน 10 ข้อ  ที่เกี่ยวข้องกับเหล่านี้ทักษะโดยตรง 1.การอ่านจับใจความ 2.การวิเคราะห์ข้อมูล 3.การสังเคราะห์ข้อมูล 4.การตีความข้อมูล 5.การประยุกต์ใช้ความรู้ โดยใช้ข้อมูลข้อความจากเอกสารที่ให้เท่านั้น ทั้งนี้ในข้อสอบแต่ละข้อจะต้องมีโจทย์แยกกันแต่ละข้อ และต้องระบุว่าสอดคล้องกับทักษะใดและต้องบอกเฉลยด้วยทั้งนี้ให้ส่งมาในรูปแบบนี้ {ข้อ: เลขข้อ,ทักษะ:ทักษะอะไร,โจทย์:โจทย์คืออะไร,ช้อยส์:[1,2,3,4],ข้อที่ถูก:ตัวเลข} ต้องไม่ต้องส่งข้อความอื่น ๆ ที่ไม่เกี่ยวข้องมา ทั้งนี้ในทุก key เช่น ข้อ ทักษะ ต้องมี double quote", pdf])
                pdf.delete()
                os.remove(temp_file_path)
                st.session_state['response_text'] = response.text  # เก็บข้อมูลที่ได้จาก AI
                file_path = "C:/Users/kaka/myenv/dads5001/q/q1.txt"
                with open(file_path, "w", encoding="utf-8") as file:
                    file.write(st.session_state['response_text'])
                st.session_state['N'] = 1  # ตั้งค่า N เป็น 1 เพื่อไม่ให้โค้ดนี้รันใหม่อีก
                uploaded_files = None

    # ถ้า N == 1 หมายถึงไฟล์ได้ถูกประมวลผลแล้ว และไม่ต้องรันโค้ดข้างบนซ้ำ
    if st.session_state['N'] == 1:
        # แสดงปุ่ม "Generate quiz" ถ้าไฟล์ประมวลผลแล้ว
        doc = st.text_input("ใส่ชื่อเอกสาร")
        st.session_state['doc'] = doc
        if st.button("ยืนยันชื่อเอกสาร") or st.session_state['doc'] != "":
            st.session_state['doc'] = doc
            st.write(st.session_state['doc'])
            if st.button("Generate quiz"):
                st.switch_page("pages/quiz.py")  # เปลี่ยนไปหน้า quiz.py
            if st.button("Restart"):
                del st.session_state["response_text"]
                del st.session_state["N"]
                del st.session_state["doc"]
                st.rerun()
                

elif st.session_state['authentication_status'] is False:
    st.error('Username/password is incorrect')
elif st.session_state['authentication_status'] is None:
    st.warning('Please enter your username and password')




