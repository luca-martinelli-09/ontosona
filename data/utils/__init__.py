# Imports
import configparser
from urllib.request import urlopen

import pandas as pd
import unidecode
import ontopia_py

# Namespaces constants
from .ns import *

# Get configurations from file


def getConfig(fileName):
    config = configparser.ConfigParser()
    config.read(fileName)

    return config

# Get data from CKAN OpenData portal


def getOpenData(baseURL, datasetID, resID, rawData=False, dtype=None):
    dataURI = "{}/dataset/{}/resource/{}/download".format(
        baseURL, datasetID, resID)

    if rawData:
        getDataRequest = urlopen(dataURI)

        return getDataRequest

    df = pd.read_csv(dataURI, dtype=dtype)
    df = df.applymap(lambda x: x.strip() if type(x) == str else x)

    return df

# Standardize name
# Convert name to lower case and capitalize each word


def standardizeName(name):
    name = name.lower().title()

    if name.endswith("a'"):
        name = name.removesuffix("a'") + "à"

    return name.strip()

# Generate ID by name
# Convert in lowercase and replace special characters with dash


def genNameForID(name):
    nameID = ""

    name.replace("'", "")
    name = unidecode.unidecode(name.lower())

    # Replace special chars with -
    for char in name:
        nameID += char if char.isalnum() else "-"

    return nameID

# Generate graph with default namespaces


def createGraph():
    # Create the graph
    g = ontopia_py.createGraph()

    # Data
    g.bind("anncsu", ANNCSU)
    g.bind("accommodation", ACCO_DATA)
    g.bind("organization", COV_DATA)

    return g