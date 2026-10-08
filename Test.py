from datetime import date
import streamlit as st
import math
import random

# Page Config
st.set_page_config(page_title="❤️Our Corner Of The Internet❤️",
                   page_icon="💕", layout="centered")

# Find current date.
month = date.today().month
year = date.today().year
calc_day = date.today().day - 4
days = date.today()
past_date = date(2026, 4, 4)

# Get value for years
calc_year = (days - past_date).days

round_date = math.floor(calc_year/365.25)


# Get month value
month_elapse = (month+(12*round_date)) - 4


if month_elapse > 12:
    display_month = month_elapse-(12*round_date)
else:
    display_month = month_elapse
if month == 1 or 3 or 5 or 7 or 8 or 10 or 12:
    thirtyone = True
if month == 4 or 6 or 9 or 11:
    thirty = True
if month == 2:
    feb = True
if calc_day < 0 and thirtyone == True:
    display_day = 31 + calc_day
elif calc_day < 0 and thirtyone == True:
    display_day = 30 + calc_day
elif calc_day < 0 and feb == True:
    display_day = 28 + calc_day
else:
    display_day = calc_day

st.subheader("Its been:", text_alignment="center")
st.title(f"❤️:violet[{round_date} years, {display_month} months and]",
         text_alignment="center")
st.title(f":violet[{display_day} days]❤️", text_alignment="center")
st.subheader("since we started dating", text_alignment="center")


st.header("❤️Photo Gallery Of My Favorite Pictures of You❤️",
          text_alignment="center")

if st.button("Click Here To See The Pictures"):
    PicNum = random.randint(1, 2)
    if PicNum == 1:
        st.subheader("Tongue Touch Tweaker")
        st.image("IMG_1556.JPEG", caption="So I love this picture of you because it super cute in my eyes. It was right after my tongue touched yours while we kissed and seeing you act like this is just super cute to me.", width=400)
