import streamlit as st  # pip install streamlit
from deta import Deta  # pip install deta


# Load the environment variables
DETA_KEY = "a0mnukwqayt_cLiQRjhxBc1SyDRRxLyk84Vxp2np6GW2"

# Initialize with a project key
deta = Deta(DETA_KEY)

# This is how to create/connect a database
db = deta.Base("housing_berlin")


def insert_berlinDistrict(berlinDistrict, finalPrice, mainFacilities, comment):
    """Returns the report on a successful creation, otherwise raises an error"""
    return db.put({"key": berlinDistrict, "finalPrice": finalPrice, "mainFacilities": mainFacilities, "comment": comment})


def fetch_all_berlinDistricts():
    """Returns a dict of all periods"""
    res = db.fetch()
    return res.items


def get_berlinDistrict(berlinDistrict):
    """If not found, the function will return None"""
    return db.get(berlinDistrict)