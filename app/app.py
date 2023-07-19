import plotly.graph_objects as go
import streamlit as st
from streamlit_option_menu import option_menu

import database as db

# -------------- SETTINGS --------------
finalPrice = ["Cold Price", "Warm Price", "Other Price (eg: Insurance)"]
mainFacilities = ["Parking", "Balcony", "Elevator", "Garden", "Cellar"]
currency = "EUR"
page_title = "House Prices in Berlin Reviewer"
page_icon = ":money_with_wings:"
layout = "centered"
# --------------------------------------

st.set_page_config(page_title=page_title, page_icon=page_icon, layout=layout)
st.title(page_title + " " + page_icon)

# --- DROP DOWN VALUES FOR SELECTING THE BERLIN DISTRICTS ---
districts = ["Mitte", "Friedrichshain-Kreuzberg", "Pankow", "Charlottenburg-Wilmersdorf", "Spandau", "Steglitz-Zehlendorf",
             "Tempelhof-Schöneberg", "Neukölln", "Treptow-Köpenick", "Marzahn-Hellersdorf", "Lichtenberg", "Reinickendorf"]
codes = [
    ("10115", "Mitte"), ("10117", "Mitte"), ("10119", "Mitte"), ("10178", "Mitte"), ("10179", "Mitte"),
    ("10243", "Friedrichshain"), ("10245", "Friedrichshain"), ("10247", "Friedrichshain"), ("10249", "Friedrichshain"),
    ("10318", "Lichtenberg"), ("10319", "Lichtenberg"),
    ("10405", "Prenzlauer Berg"), ("10407", "Prenzlauer Berg"), ("10409", "Prenzlauer Berg"), ("10435", "Prenzlauer Berg"),
    ("10437", "Prenzlauer Berg"), ("10439", "Prenzlauer Berg"),
    ("10585", "Charlottenburg"), ("10587", "Charlottenburg"), ("10589", "Charlottenburg"), ("10623", "Charlottenburg"),
    ("10625", "Charlottenburg"), ("10627", "Charlottenburg"), ("10629", "Charlottenburg"),
    ("10823", "Schöneberg"), ("10825", "Schöneberg"), ("10827", "Schöneberg"), ("10829", "Schöneberg"),
    ("10961", "Kreuzberg"), ("10963", "Kreuzberg"), ("10965", "Kreuzberg"), ("10967", "Kreuzberg"), ("10969", "Kreuzberg"),
    ("10997", "Kreuzberg"), ("109979", "Kreuzberg"),
    ("12043", "Neukölln"), ("12045", "Neukölln"), ("12047", "Neukölln"), ("12049", "Neukölln"), ("12051", "Neukölln"),
    ("12053", "Neukölln"), ("12055", "Neukölln"), ("12057", "Neukölln"), ("12059", "Neukölln"),
    ("12203", "Steglitz"), ("12205", "Steglitz"), ("12207", "Steglitz"), ("12209", "Steglitz"),
    ("12247", "Zehlendorf"), ("12249", "Zehlendorf"), ("12277", "Zehlendorf"), ("12279", "Zehlendorf"),
    ("12305", "Mariendorf"), ("12307", "Mariendorf"), ("12309", "Mariendorf"), ("12487", "Mariendorf"),
    ("12489", "Mariendorf"),
    ("12555", "Pankow"), ("12557", "Pankow"), ("12559", "Pankow"), ("12679", "Pankow"), ("12681", "Pankow"),
    ("12683", "Pankow"), ("12685", "Pankow"), ("12687", "Pankow"), ("12689", "Pankow"),
    ("13086", "Reinickendorf"), ("13088", "Reinickendorf"), ("13089", "Reinickendorf"), ("13187", "Reinickendorf"),
    ("13189", "Reinickendorf"), ("13347", "Reinickendorf"), ("13349", "Reinickendorf"),
    ("13351", "Spandau"), ("13353", "Spandau"), ("13355", "Spandau"), ("13357", "Spandau"), ("13359", "Spandau"),
    ("13403", "Spandau"), ("13405", "Spandau"), ("13407", "Spandau"), ("13409", "Spandau"),
    ("13435", "Treptow"), ("13437", "Treptow"), ("13439", "Treptow"), ("14109", "Treptow"),
    ("14163", "Köpenick"), ("14165", "Köpenick"), ("14167", "Köpenick"), ("14169", "Köpenick")
]


# --- DATABASE INTERFACE ---
def get_all_berlinDistricts():
    """Returns a list of all Berlin districts"""
    items = db.fetch_all_berlinDistricts()
    berlinDistricts = []
    for item in items:
        if "berlinDistricts" in item:
            berlinDistricts.append(item["berlinDistricts"])
    return berlinDistricts


# --- HIDE STREAMLIT STYLE ---
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# --- NAVIGATION MENU ---
selected = option_menu(
    menu_title=None,
    options=["Data Entry", "Data Visualization"],
    icons=["pencil-fill", "bar-chart-fill"],  # https://icons.getbootstrap.com/
    orientation="horizontal",
)

# --- INITIALIZE SESSION STATE ---
if "initialized" not in st.session_state:
    st.session_state.initialized = True

# --- INPUT & SAVE BERLIN DISTRICTS ---
if selected == "Data Entry":
    st.header(f"Data Entry in {currency}")
    with st.form("entry_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        col1.selectbox("Select District:", districts, key="district")
        col2.selectbox("Select Postal Code:", codes, key="code")

        "---"
        with st.expander("Total Price"):
            for total_price in finalPrice:
                st.number_input(f"{total_price}:", min_value=0, format="%i", step=10, key=total_price)
        with st.expander("Main Facilities"):
            for main_facilities in mainFacilities:
                st.number_input(f"{main_facilities}:", min_value=0, max_value=3, format="%i", step=1, key=main_facilities)
        with st.expander("Comment"):
            comment = st.text_area("", placeholder="Enter a comment here ...")

        "---"
        submitted = st.form_submit_button("Save Data")
        if submitted:
            berlinDistrict = str(st.session_state["code"]) + "," + str(st.session_state["district"])
            finalPrice = {total_price: st.session_state[total_price] for total_price in finalPrice}
            mainFacilities = {main_facilities: st.session_state[main_facilities] for main_facilities in mainFacilities}
            db.insert_berlinDistrict(berlinDistrict, finalPrice, mainFacilities, comment)
            st.success("Data saved!")

# --- DATA VISUALIZATION ---
elif selected == "Data Visualization":
    st.header("Data Visualization")
    with st.form("saved_berlinDistricts"):
        berlinDistricts = get_all_berlinDistricts()
        submitted = st.form_submit_button("Plot Prices")
        if submitted:
            if berlinDistricts:
                st.subheader("Select Berlin District:")
                selected_district = st.selectbox("Districts", berlinDistricts)
                data = db.fetch_berlinDistrict_data(selected_district)
                if data:
                    st.subheader("Total Price")
                    fig_total_price = go.Figure(data=[go.Bar(x=data["Dates"], y=data["Total Price"])])
                    fig_total_price.update_layout(title="Total Price Over Time")
                    st.plotly_chart(fig_total_price)

                    st.subheader("Main Facilities")
                    fig_main_facilities = go.Figure(data=[go.Scatter(x=data["Dates"], y=data[facility], mode="markers") for facility in mainFacilities])
                    fig_main_facilities.update_layout(title="Main Facilities Over Time")
                    st.plotly_chart(fig_main_facilities)
                else:
                    st.warning("No data available for the selected district.")
            else:
                st.warning("No Berlin districts available.")

