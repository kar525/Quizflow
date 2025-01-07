import streamlit as st
import re
import json
from streamlit_gsheets import GSheetsConnection
from oauth2client.service_account import ServiceAccountCredentials
import gspread
from datetime import datetime

if "skillscore" not in st.session_state:
    st.session_state.skillscore = [0,0,0,0,0]




user = st.session_state["username"]

# กำหนดค่าเริ่มต้นใน st.session_state ถ้ายังไม่ได้กำหนด
if "score" not in st.session_state:
    st.session_state.score = 0  # ถ้าไม่มีกำหนดค่าเริ่มต้นเป็น 0

if 'T' not in st.session_state:
    st.session_state.T = 0  # เริ่มต้นที่คำถามแรก

def choices(a, question, options):
    # ใช้ radio button แสดงตัวเลือก
    selected = st.radio(label=f"ข้อ {a}\n{question}", options=options, key=str(a))
    return selected  # คืนค่าคำตอบที่ผู้ใช้เลือก

# อ่านไฟล์คำถาม
with open('C:/Users/kaka/myenv/dads5001/q/q1.txt', 'r', encoding='utf-8') as file:
    content = file.read()
    matches = re.findall(r'\{(.*?)\}', content, re.DOTALL)
    questions = [json.loads("{" + match + "}") for match in matches]

# ตรวจสอบว่าผู้ใช้ยังทำแบบทดสอบไม่เสร็จ
if st.session_state.T < len(questions):
    # ดึงคำถามปัจจุบัน
    current_question = questions[st.session_state.T]
    skill = current_question.get("ทักษะ")
    question_number = current_question.get("ข้อ")
    question_text = current_question.get("โจทย์")
    options = current_question.get("ช้อยส์")
    correct_index = int(current_question.get("ข้อที่ถูก")) - 1  # แปลงให้ index เริ่มที่ 0
    
    # แสดงคำถามและรับคำตอบจากผู้ใช้
    st.write("เอกสาร : "+st.session_state['doc'])
    st.write("user : "+user)
    st.write(skill)
    user_answer = choices(question_number, question_text, options)

    if st.button("ยืนยันคำตอบ"):  # ปุ่มเพื่อยืนยันคำตอบ
        # ตรวจสอบคำตอบ
        correct_answer = options[correct_index]
        if user_answer == correct_answer:
            st.session_state.score += 1  # เพิ่มคะแนนถ้าตอบถูก
            if skill == "การอ่านจับใจความ" :
                st.session_state.skillscore[0] += 1
            elif skill == "การวิเคราะห์ข้อมูล":
                st.session_state.skillscore[1] += 1
            elif skill == "การสังเคราะห์ข้อมูล":
                st.session_state.skillscore[2] += 1
            elif skill == "การตีความข้อมูล":
                st.session_state.skillscore[3] += 1
            else:
                st.session_state.skillscore[4] += 1

        # ไปคำถามถัดไป
        st.session_state.T += 1
        st.rerun()  # รีเฟรชหน้าเพื่อแสดงคำถามถัดไป
else:
    # เมื่อทำเสร็จ
    st.write("คุณทำแบบทดสอบเสร็จแล้ว!")
    


# แสดงคะแนนปัจจุบันและคำถามที่กำลังตอบ
st.write(f"คะแนน: {st.session_state.score}")

if st.session_state.T <= 9:
    st.write(f"คำถามที่: {st.session_state.T+1}/{len(questions)}")

    
#st.write(st.session_state.T)

if st.session_state.T == 10:
    if st.button("Restart"):
        del st.session_state["skillscore"]
        del st.session_state["score"]
        del st.session_state["T"]
        del st.session_state["response_text"]
        del st.session_state["N"]
        del st.session_state["doc"]
        st.switch_page("quizflow.py")
        st.rerun()
    if st.button("ทำข้อสอบอีกครั้ง"):
        del st.session_state["skillscore"]
        del st.session_state["score"]
        del st.session_state["T"]
        st.rerun()
    if st.button("บันทึกคะแนน"):        
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name("C:/Users/kaka/myenv/dads5001/.streamlit/gen-lang-client-0418933665-0cff057bb5d3.json", scope)
        client = gspread.authorize(creds)
        now = datetime.now()
        sheet = client.open_by_key("1hFgKsPodlrcZhsP0Q64Ty3ndFaKUL9aA-UBIEqh1Gb0").sheet1
        newrow = [ [str(user),'การอ่านจับใจความ', st.session_state.skillscore[0],str(now), st.session_state['doc']],[str(user),'การวิเคราะห์ข้อมูล', st.session_state.skillscore[1],str(now), st.session_state['doc']],[str(user),'การสังเคราะห์ข้อมูล', st.session_state.skillscore[2],str(now), st.session_state['doc']],[str(user),'การตีความข้อมูล', st.session_state.skillscore[3],str(now), st.session_state['doc']],[str(user),'การประยุกต์ใช้ความรู้', st.session_state.skillscore[4],str(now), st.session_state['doc']]]
        sheet.append_rows(newrow)
    if st.button("ไปยังหน้าวิเคราะห์คะแนน"):
        st.switch_page("C:/Users/kaka/myenv/dads5001/pages/analystics.py")
        




#if st.session_state.T <= 9:
    #st.write(current_question.get("ข้อที่ถูก"))

