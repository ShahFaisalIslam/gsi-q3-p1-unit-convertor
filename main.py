import streamlit as st
import json
# Page Setup
st.set_page_config(page_title="Unit Convertor",layout="wide")
st.header("Unit Convertor",divider=True)
st.write("Replicates [Google's Unit Convertor](https://www.google.com/search?q=unit+convertor)")

# Instantiate session state left_value and right_value
if "left_value" not in st.session_state:
    st.session_state.left_value = 1
if "right_value" not in st.session_state:
    st.session_state.right_value = None

def swap_if_duplicate(**kwargs):
    if kwargs["direction"] == "left":
        # Change right unit to previous left unit if it matches the left unit
        if st.session_state.right_unit == st.session_state.left_unit:
            st.session_state.right_unit = st.session_state.prev_left_unit
    else:
        # Change left unit to previous right unit if it matches the right unit
        if st.session_state.left_unit == st.session_state.right_unit:
            st.session_state.left_unit = st.session_state.prev_right_unit

def convert_right_value_temperature():
    return 1,1

def convert_left_value_temperature():
    return 1,1

def convert_right_value():
    # Deal with temperature quantity in a separate function
    if st.session_state.quantity == "Temperature":
        return convert_right_value_temperature()
    # Get right and left unit factors
    factor_right = unit_data[unit_list.index(st.session_state.right_unit)][1]
    factor_right_operator = unit_data[unit_list.index(st.session_state.right_unit)][2]
    factor_left = unit_data[unit_list.index(st.session_state.left_unit)][1]
    factor_left_operator = unit_data[unit_list.index(st.session_state.left_unit)][2]
    # Factor numerator
    # It will have factor_right if factor_right_operator is divide
    # Similarly, it will have factor_left it factor_left_operator is multiply
    factor_numerator = (factor_right if factor_right_operator == "/" else 1)
    factor_numerator *= (factor_left if factor_left_operator == "*" else 1)
    # Factor denominator
    # It will have factor_right if factor_right_operator is multiply
    # Similarly, it will have factor_left it factor_left_operator is divide
    factor_denominator = (factor_right if factor_right_operator == "*" else 1)
    factor_denominator *= (factor_left if factor_left_operator == "/" else 1)
    # Conversion
    # To reduce truncation error, we first multiply the numerator then divide the denominator
    st.session_state.right_value = st.session_state.left_value * factor_numerator / factor_denominator
    return factor_numerator, factor_denominator

def convert_left_value():
    # Deal with temperature quantity in a separate function
    if st.session_state.quantity == "Temperature":
        return convert_left_value_temperature()
    # Get right and left unit factors
    factor_right = unit_data[unit_list.index(st.session_state.right_unit)][1]
    factor_right_operator = unit_data[unit_list.index(st.session_state.right_unit)][2]
    factor_left = unit_data[unit_list.index(st.session_state.left_unit)][1]
    factor_left_operator = unit_data[unit_list.index(st.session_state.left_unit)][2]
    # Factor denominator
    # It will have factor_right if factor_right_operator is divide
    # Similarly, it will have factor_left it factor_left_operator is multiply
    factor_denominator = (factor_right if factor_right_operator == "/" else 1)
    factor_denominator *= (factor_left if factor_left_operator == "*" else 1)
    # Factor numerator
    # It will have factor_right if factor_right_operator is multiply
    # Similarly, it will have factor_left it factor_left_operator is divide
    factor_numerator = (factor_right if factor_right_operator == "*" else 1)
    factor_numerator *= (factor_left if factor_left_operator == "/" else 1)
    # Conversion
    # To reduce truncation error, we first multiply the numerator then divide the denominator

    st.session_state.left_value = st.session_state.right_value * factor_numerator / factor_denominator

with open("data/quantity.json") as quantity_file:
    quantity_list = json.loads(quantity_file.read())
    quantity = st.selectbox("Quantity",quantity_list,index=quantity_list.index("Length"),label_visibility="hidden",key="quantity")
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
            if "right_unit" not in st.session_state or st.session_state.right_unit not in unit_list:
                st.session_state.right_unit = unit_list[1]
            # Conversion
            [factor_numerator, factor_denominator] = convert_right_value()
            st.number_input("Right Value",key="right_value",step=0.01,label_visibility="hidden",on_change=convert_left_value)
            st.session_state.prev_right_unit = st.selectbox("Unit",unit_list,label_visibility="hidden",key="right_unit",on_change=swap_if_duplicate,kwargs={"direction":"right"})

        # Information about how to convert
        action = "Multiply" if factor_numerator > factor_denominator else "Divide"
        factor = (factor_numerator/factor_denominator) if factor_numerator > factor_denominator else (factor_denominator/factor_numerator)
        st.subheader(f"Formula: {action} by {factor}")
