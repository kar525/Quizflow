import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


if st.button("กลับไปหน้า Quiz"):
    st.switch_page("C:/Users/kaka/myenv/dads5001/pages/quiz.py")



# ฟังก์ชันโหลดข้อมูล
def load_data():
    url = "https://docs.google.com/spreadsheets/d/1hFgKsPodlrcZhsP0Q64Ty3ndFaKUL9aA-UBIEqh1Gb0/gviz/tq?tqx=out:csv&sheet=sheet1"
    df = pd.read_csv(url, encoding='utf-8')
    return df

# โหลดข้อมูล
df = load_data()

df["id"] =  df["id"].astype(str)
df["doc"] =  df["doc"].astype(str)

dfchocice = df.loc[df["id"] == st.session_state["username"]]


option = st.selectbox(
    "เลือกเอกสาร",
    (dfchocice['doc'].unique()),
)

dftime = df.loc[(df["id"] == st.session_state["username"]) & (df["doc"] == option)]

option2 = st.selectbox(
    "เลือกเวลาที่ทำข้อสอบ",
    (dftime['time'].unique()),
)



dfana = df.loc[(df["id"] == st.session_state["username"]) & (df["doc"] == option) & (df["time"] == option2)]




filtered_data = df[df['id'].isin(['1234'])]


# สร้าง Bar Chart โดยใช้ labels
fig = px.bar(
    dfana,
    x="skill",  # ใช้ชื่อเต็มในแกน x
    y="score",
    title="result",
)

# แสดงกราฟใน Streamlit
st.plotly_chart(fig)


# สร้างกราฟ Radar Chart
fig2 = go.Figure(data=go.Scatterpolar(
    r=dfana['score'],  # คะแนน
    theta=dfana['skill'],  # ทักษะ
    fill='toself',  # เติมกราฟ
    name='Skill Assessment'
))

# เพิ่มชื่อกราฟ
fig.update_layout(
    title='Basic Radar Chart',
    polar=dict(
        radialaxis=dict(
            visible=True,
            range=[0, 2]  # กำหนดช่วงคะแนนจาก 0 ถึง 100
        )
    ),
    showlegend=False  # ไม่แสดง legend
)

# แสดงกราฟ
st.plotly_chart(fig2)
