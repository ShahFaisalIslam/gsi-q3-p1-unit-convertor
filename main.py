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

# Inverts series of operation as follows:
# 1. Reverses the order of operations in the series
# 2. Turns the operator of each operation into its opposite
def invert_operations(series: list) -> list:
    rseries = reversed(series)
    series = []
    for operation in rseries:
        if operation["operator"] == "+":
            roperation = {"operator" : "-","factor" : operation["factor"]}
        if operation["operator"] == "-":
            roperation = {"operator" : "+","factor" : operation["factor"]}
        if operation["operator"] == "*":
            roperation = {"operator" : "/","factor" : operation["factor"]}
        if operation["operator"] == "/":
            roperation = {"operator" : "*","factor" : operation["factor"]}
        series.append(roperation)
    return series
# Function takes in series of operations, which is a list of dictionaries,
# and presents them to the user.
# Each dictionary consists of two key-value pairs: factor and operator
# Operators tells what to do, and factor tells us what number will be used
# in the operation.
# For example, [{"factor": 5, "operator": "+"}, {"factor" : 20, "operator": "/"}]
# Will yield 'result = result + 5; result = result / 20'
# The simple series of statements for now is easier to display than a complex web
# of parentheses-filled statements, so let's ignore that for now
def display_conversion(series: list,invert=False,step=0):
    conversion_string = ""
    if invert:
        series = invert_operations(series)
    for operation in series:
        if operation["operator"] == "+":
            action = "add"
        elif operation["operator"] == "-":
            action = "subtract"
        elif operation["operator"] == "*":
            action = "multiply by"
        elif operation["operator"] == "/":
            action = "divide by"
        if conversion_string:
            conversion_string += ", then "
            conversion_string += f"{action} {operation["factor"]}"
        elif step:
            conversion_string += f"Step {step}: "
            conversion_string += f"{action} {operation["factor"]}".capitalize()
    st.write(conversion_string)

# Performs given series of operations on given value, and returns the result
# Inverts the series first if given to do so
def perform_operations(series: list,input: float,invert=False):
    if invert:
        series = invert_operations(series)
    for operation in series:
        if operation["operator"] == '+':
            input += operation["factor"]
        elif operation["operator"] == '-':
            input -= operation["factor"]
        elif operation["operator"] == '*':
            input *= operation["factor"]
        elif operation["operator"] == '/':
            input /= operation["factor"]
    return input

def convert_right_value_temperature():
    st.session_state.right_value = perform_operations(unit_data[unit_list.index(st.session_state.left_unit)][1],st.session_state.left_value)
    st.session_state.right_value = perform_operations(unit_data[unit_list.index(st.session_state.right_unit)][1],st.session_state.right_value,True)
    return 1,1

def convert_left_value_temperature():
    st.session_state.left_value = perform_operations(unit_data[unit_list.index(st.session_state.right_unit)][1],st.session_state.right_value)
    st.session_state.left_value = perform_operations(unit_data[unit_list.index(st.session_state.left_unit)][1],st.session_state.left_value,True)
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
        # with exception for temperature
        if quantity != "temperature":
            action = "Multiply" if factor_numerator > factor_denominator else "Divide"
            factor = (factor_numerator/factor_denominator) if factor_numerator > factor_denominator else (factor_denominator/factor_numerator)
            st.write(f"Formula: {action} by {factor}")
        else:
#            display_conversion(unit_list.index(st.session_state.left_unit)[1])
            display_conversion(unit_data[unit_list.index(st.session_state.left_unit)][1],step=1)
            display_conversion(unit_data[unit_list.index(st.session_state.right_unit)][1],True,step=2)