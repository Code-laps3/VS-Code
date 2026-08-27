import random
import streamlit as st
neglect = st.selectbox("What do you want to calculate?",
                       ("Friction", "Velocity At End", "Slope Length", "Velocity at Start", "Height"))

mass = random.randint(10, 20)
speedA = random.randint(0, 10)
height = random.randint(2, 12)
slopelenght = random.randint(30, 100)
friction = round(random.uniform(3, 10), 2)

EmA = (mass * 9.8 * height) + (0.5 * mass * speedA**2)
speedB1 = EmA - friction * slopelenght
speedB2 = speedB1 / (0.5 * mass)
speedB3 = round(speedB2**0.5, 2)

if neglect == "Friction" and st.button("Run"):
    st.write(f"Mass is : {mass} kg")
    st.write(f"Speed at A is : {speedA} m/s")
    st.write(f"Height is : {height} m")
    st.write(f"Slope Length is : {slopelenght} m")
    st.write(f"Speed at B is : {speedB3} m/s")
    st.write("Find Friction")


if neglect == "Velocity At End" and st.button("Run"):
    st.write(f"Mass is : {mass} kg")
    st.write(f"Speed at A is : {speedA} m/s")
    st.write(f"Height is : {height} m")
    st.write(f"Slope Length is : {slopelenght} m")
    st.write(f"Friction is : {friction} N")
    st.write("Find Speed at B")


if neglect == "Slope Length" and st.button("Run"):
    st.write(f"Mass is : {mass} kg")
    st.write(f"Speed at A is : {speedA} m/s")
    st.write(f"Height is : {height} m")
    st.write(f"Friction is : {friction} N")
    st.write(f"Speed at B is : {speedB3} m/s")
    st.write("Find Slope Length")


if neglect == "Velocity at Start" and st.button("Run"):
    st.write(f"Mass is : {mass} kg")
    st.write(f"Height is : {height} m")
    st.write(f"Slope Length is : {slopelenght} m")
    st.write(f"Friction is : {friction} N")
    st.write(f"Speed at B is : {speedB3} m/s")
    st.write("Find Speed at A")

if neglect == "Height" and st.button("Run"):
    st.write(f"Mass is : {mass} kg")
    st.write(f"Speed at A is : {speedA} m/s")
    st.write(f"Slope Length is : {slopelenght} m")
    st.write(f"Friction is : {friction} N")
    st.write(f"Speed at B is : {speedB3} m/s")
    st.write("Find Height")

view_answer = st.button("View Answer")
if view_answer:
    if neglect == "Friction":
        st.success(f"Friction is : {friction} N")
    elif neglect == "Velocity At End":
        st.success(f"Speed at B is : {speedB3} m/s")
    elif neglect == "Slope Length":
        st.success(f"Slope Length is : {slopelenght} m")
    elif neglect == "Velocity at Start":
        st.success(f"Speed at A is : {speedA} m/s")
    elif neglect == "Height":
        st.success(f"Height is : {height} m")
