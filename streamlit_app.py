import streamlit as st
import pandas as pd
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import HttpRequest
import google_auth_httplib2
import httplib2

# Constants for Google Sheets API
SCOPE = ["https://www.googleapis.com/auth/spreadsheets"]
SPREADSHEET_ID = "10iVbv4eoBjgxnMOHHN_ZEz1qM_SGccftXel18yhzx4c"
SHEET_NAME = "Sheet1"
GSHEET_URL = f"https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}"

# Create connection to Google Sheets API
@st.cache_resource
def connect_to_gsheet():
    credentials = service_account.Credentials.from_service_account_info(
        st.secrets["gcp_service_account"], scopes=SCOPE
    )
    
    authorized_http = google_auth_httplib2.AuthorizedHttp(credentials, http=httplib2.Http())
    
    service = build("sheets", "v4", http=authorized_http)
    gsheet_connector = service.spreadsheets()
    return gsheet_connector

# Function to fetch data from the Google Sheet and return as DataFrame
def get_data(gsheet_connector) -> pd.DataFrame:
    values = (
        gsheet_connector.values()
        .get(spreadsheetId=SPREADSHEET_ID, range=f"{SHEET_NAME}!A:AJ")
        .execute()
    )
    df = pd.DataFrame(values["values"])
    df.columns = df.iloc[0]  # Use the first row as the column headers
    df = df[1:]  # Remove the header row
    return df

# Function to append a new row of data to Google Sheet
def add_row_to_gsheet(gsheet_connector, row) -> None:
    gsheet_connector.values().append(
        spreadsheetId=SPREADSHEET_ID,
        range=f"{SHEET_NAME}!A:AJ",
        body=dict(values=row),
        valueInputOption="USER_ENTERED",
    ).execute()

# Google Sheets connection
gsheet_connector = connect_to_gsheet()

#detail
st.header("👴🏻👵🏻Thai Geriatric Depression Scale")
st.subheader("แบบประเมินความรู้สึกของผู้สูงอายุ")
st.divider()

def clear_inputs():
    st.session_state.name = " "
    st.session_state.gender = ''
    st.session_state.age = 0
    st.session_state.address = False

st.header("1.ข้อมูลส่วนตัว")
name = st.text_input ("ชื่อ-สกุล*",key='ชื่อ-สกุล')
gender = st.radio("เพศ*",["ชาย","หญิง"],key='เพศ')
age = st.number_input("อายุ(ปี)*",0,130,key='อายุ(ปี)')
address = st.checkbox("ในมหาสวัสดิ์*",key='ที่อยู่')

st.markdown("**required*")

if st.button('Clear Inputs'):
    clear_inputs()

st.header("2.แบบประเมิน")
# create form screening
with st.form('my_form'):
    questions = {
        "one": "**1.ท่านพอใจกับชีวิตความเป็นอยู่ตอนนี้**",
        "two": "**2.ท่านไม่อยากทำในสิ่งที่เคยสนใจหรือเคยทำเป็นประจำ**",
        "three": "**3.ท่านรู้สึกชีวิตของท่านช่วงนี้ว่างเปล่า ไม่รู้จะทำอะไร**",
        "four": "**4.ท่านรู้สึกเบื่อหน่ายบ่อยๆ**",
        "five": "**5.ท่านหวังว่าจะมีสิ่งที่ดีเกิดขึ้นในวันหน้า**",
        "six": "**6.ท่านมีเรื่องกังวลอยู่ตลอดเวลา และเลิกคิดไม่ได้**",
        "seven": "**7.ส่วนใหญ่แล้วท่านรู้สึกอารมณ์ดี**",
        "eight": "**8.ท่านรู้สึกกลัวว่าจะมีเรื่องไม่ดีเกิดขึ้นกับท่าน**",
        "nine": "**9.ส่วนใหญ่ท่านรู้สึกมีความสุข**",
        "ten": "**10.บ่อยครั้งที่ท่านรู้สึกไม่มีที่พึ่ง**",
        "eleven": "**11.ท่านรู้สึกกระวนกระวาย กระสับกระส่ายบ่อยๆ**",
        "twelve": "**12.ท่านชอบอยู่กับบ้านมากกว่าที่จะออกนอกบ้าน**",
        "thirteen":  "**13.บ่อยครั้งที่ท่านรู้สึกวิตกกังวลเกี่ยวกับชีวิตข้างหน้า**",
        "fourteen": "**14.ท่านคิดว่าความจำท่านไม่ดีเท่ากับคนอื่น**",
        "fifteen": "**15.การที่มีชีวิตถึงปัจจุบันนี้ เป็นเรื่องน่ายินดีหรือไม่**",
        "sixteen": "**16.ท่านรู้สึกหมดกำลังใจ หรือเศร้าใจบ่อยๆ**",
        "seventeen": "**17.ท่านรู้สึกว่าชีวิตท่านค่อนข้างไม่มีคุณค่า**",
        "eighteen": "**18.ท่านรู้สึกกังวลมากกับชีวิตที่ผ่านมา**",
        "nineteen": "**19.ท่านรู้สึกว่าชีวิตนี้ยังมีเรื่องน่าสนุกอีกมาก**",
        "twenty": "**20.ท่านรู้สึกลำบากที่จะเริ่มต้นทำอะไรใหม่ๆ**",
        "twentyone": "**21.ท่านรู้สึกกระตือรือร้น**",
        "twentytwo": "**22.ท่านรู้สึกสิ้นหวัง**",
        "twentythree":"**23.ท่านคิดว่าคนอื่นดีกว่าท่าน**",
        "twentyfour": "**24.ท่านอารมณ์เสียง่ายกับเรื่องเล็กๆน้อยๆอยู่เสมอ**",
        "twentyfive": "**25.ท่านรู้สึกอยากร้องไห้บ่อยๆ**",
        "twentysix": "**26.ท่านมีความตั้งใจในการทำสิ่งหนึ่งสิ่งใดได้ไม่นาน**",
        "twentyseven": "**27.ท่านรู้สึกสดชื่นในเวลาตื่นนอนตอนเช้า**",
        "twentyeight": "**28.ท่านไม่อยากพบปะพูดคุยกับคนอื่น**",
        "twentynine": "**29.ท่านตัดสินใจอะไรได้เร็ว**",
        "thirty":  "**30.ท่านมีจิตใจสบายแจ่มใสเหมือนก่อน**",
    }

    answers = {q: st.radio(q_text, ["ใช่", "ไม่ใช่"]) for q, q_text in questions.items()}

    ans_no = {
        "one": one,
        "five": five,
        "nine": nine,
        "fifteen": fifteen,
        "nineteen": nineteen,
        "twentyone": twentyone,
        "twentyseven": twentyseven,
        "twentynine": twentynine,
        "thirty": thirty,
    }

    ans_yes = {
        'two': two,
        'three': three,
        'four': four,
        'six': six,
        'eight': eight,
        'ten': ten,
        'eleven': eleven,
        'twelve': twelve,
        'thriteen': thirteen,
        'fourteen': fourteen,
        'sixteen': sixteen,
        'seventeen': seventeen,
        'eighteen': eighteen,
        'twenty': twenty,
        'twentytwo': twentytwo,
        'twentythree': twentythree,
        'twentyfour': twentyfour,
        'twentyfive': twentyfive,
        'twentysix': twentysix,
        'twentyeight': twentyeight,
    }
        
    
    submitted = st.form_submit_button("Submit")

# Scoring logic
if submitted:
    score_no = sum(1 for ans in ans_no.values() if ans == "ไม่ใช่")
    score_yes = sum(1 for ans in ans_yes.values() if ans == "ใช่")
    total_score = score_no + score_yes

    # Determine the result based on the score
    if total_score <= 12:
        result = "👵🏻👴🏻 ผู้สูงอายุปกติ"
    elif total_score <= 18:
        result = "🙂 ผู้มีความเศร้าเล็กน้อย (Mild depression)"
    elif total_score <= 24:
        result = "😕 ผู้มีความเศร้าปานกลาง (Moderate depression)"
    else:
        result = "😭 ผู้มีความเศร้ารุนแรง (Severe depression)"
    
    # Add the row to Google Sheet
    add_row_to_gsheet(
        gsheet_connector,
        [[name, gender, age, address, *answers.values(), total_score, result]],
    )
    st.success(f'✅ คะแนนของคุณ 👉 {total_score}   แปลผล: {result}')

# Expander to view all records in Google Sheets
expander = st.expander("See all records")
with expander:
    st.write(f"Open original [Google Sheet]({GSHEET_URL})")
    st.dataframe(get_data(gsheet_connector))
