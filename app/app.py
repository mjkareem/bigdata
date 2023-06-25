import streamlit as st
import requests

RAPIDAPI_KEY = '4ae92f42famsh1cebfa71809ef22p17d619jsna4dec9182f15'
ENDPOINT = 'https://flight-radar1.p.rapidapi.com/flights/search'
HEADERS = {
    'X-RapidAPI-Key': RAPIDAPI_KEY,
    'X-RapidAPI-Host': 'flight-radar1.p.rapidapi.com'
}

def get_flight_data(flight_number):
    params = {'query': flight_number}
    try:
        response = requests.get(ENDPOINT, headers=HEADERS, params=params)
        return response.json()
    except requests.RequestException as e:
        st.error(f'Error occurred: {e}')
        return None

def main():
    st.title('FlightRadar API App')
    flight_number = st.text_input('Enter Flight Number:')
    if st.button('Get Flight Data'):
        if flight_number:
            flight_data = get_flight_data(flight_number)
            if flight_data:
                st.write(flight_data)
        else:
            st.warning('Please enter a flight number.')

if __name__ == '__main__':
    main()


