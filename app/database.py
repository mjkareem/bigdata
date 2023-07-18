import streamlit as st
from deta import Deta

# Load the environment variables
DETA_KEY = "a0mnukwqayt_cLiQRjhxBc1SyDRRxLyk84Vxp2np6GW2"

# Initialize with a project key
deta = Deta(DETA_KEY)

# This is how to create/connect a database
db = deta.Base("housing_berlin")


def insert_berlinDistrict(berlinDistrict, finalPrice, mainFacilities, comment):
    """Returns the report on a successful creation, otherwise raises an error"""
    data = {
        "berlinDistricts": berlinDistrict,
        "finalPrice": finalPrice,
        "mainFacilities": mainFacilities,
        "comment": comment
    }
    return db.put(data)

def get_all_berlinDistricts():
    """Returns a list of all Berlin districts"""
    res = db.fetch()
    berlinDistricts = [item.get("berlinDistricts") for item in res.items]
    return berlinDistricts


def fetch_all_berlinDistricts():
    """Returns a dict of all Berlin districts"""
    res = db.fetch()
    return res.items


def fetch_berlinDistrict_data(berlinDistrict):
    """Returns the data for a specific Berlin district"""
    data = db.get(berlinDistrict)
    return data


def get_berlinDistrict(berlinDistrict):
    """If not found, the function will return None"""
    return db.get(berlinDistrict)
