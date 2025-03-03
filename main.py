import streamlit as st
import json
# Page Setup
st.set_page_config(page_title="Unit Convertor",layout="wide")
st.header("Unit Convertor",divider=True)
st.write("Replicates [Google's Unit Convertor](https://www.google.com/search?q=unit+convertor)")

def swap_if_duplicate(**kwargs):
    if kwargs["direction"] == "left":
        # Change right unit to previous left unit if it matches the left unit
        if st.session_state.right_unit == st.session_state.left_unit:
            st.session_state.right_unit = st.session_state.prev_left_unit
    else:
        # Change left unit to previous right unit if it matches the right unit
        if st.session_state.left_unit == st.session_state.right_unit:
            st.session_state.left_unit = st.session_state.prev_right_unit

with open("data/quantity.json") as quantity_file:
    quantity_list = json.loads(quantity_file.read())
    quantity = st.selectbox("Quantity",quantity_list,index=quantity_list.index("Length"),label_visibility="hidden")
    quantity = quantity.lower().replace(" ","_")
    with open(f"data/quantity/{quantity}.json") as unit_file:
        unit_data = json.loads(unit_file.read())
        unit_list = [unit[0] for unit in unit_data]
        # Three columns, one for left hand side unit, one for equals to, and one for right hand side unit
        [left_col,_,right_col] = st.columns(3)
        # Left hand side unit
        with left_col:
            st.number_input("Left Value",key="left_value",step=0.01,label_visibility="hidden",value=float(1))
            st.session_state.prev_left_unit = st.selectbox("Unit",unit_list,label_visibility="hidden",key="left_unit",on_change=swap_if_duplicate,kwargs={"direction":"left"})
        # Equals to sign
        with _:
            st.html("<h1 style='text-align:center'>=</p>")
        # Right hand side unit
        with right_col:
            st.number_input("Right Value",key="right_value",step=0.01,label_visibility="hidden")
            st.session_state.prev_right_unit = st.selectbox("Unit",unit_list,index=1,label_visibility="hidden",key="right_unit",on_change=swap_if_duplicate,kwargs={"direction":"right"})