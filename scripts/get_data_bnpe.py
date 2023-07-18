#!/usr/bin/env python3

# Code to extract datas from "BNPE eaufrance" website
# from the 1st year with available informations (2008) to current year
# files are stored on "output" folder" per 'department' / 'year' / 'types of data'
#
import os
import random  # to generate random user-agent
import logging  # to log various stuff
import datetime
import requests
import pandas
from lxml import etree # check README.md to solve install problem on Linux/macOS

# Variables
DEPARTEMENT_SCRAPE = 66  # target department
today = datetime.datetime.now()
current_year = today.year  # get current year
STARTING_YEAR = 2008

# Initialize the log and record informations in a CSV way
logging.basicConfig(
    format="%(asctime)s , %(levelname)-8s , %(message)s",
    filename="logging_bnpe.log",
    datefmt="%Y-%m-%d , %H:%M:%S",
    encoding="utf-8",
    level=logging.INFO,
)


def generate_random_user_agent_list() -> list:
    """generate a random user-agent list based on the most used user-agent

    Parameters :
        url_user_agent : url to retrieve the list
    Returns:
        user_agents : list
    """
    url_user_agent = (
        "https://www.useragents.me/#most-common-desktop-useragents-json-csv"
    )

    # Fetch the website content
    response = requests.get(url_user_agent)
    if response.status_code != 200:
        logging.error("Failed to fetch user agent list")
        pass

    # Parse the HTML content
    html = etree.HTML(response.text)

    # Extract user agent strings using XPath
    user_agents = html.xpath(
        '//*[@id="most-common-desktop-useragents-json-csv"]/div[1]/textarea/text()'
    )
    if not user_agents:
        logging.error("Failed to extract user agent list")
        pass

    # Parse the JSON data
    try:
        user_agents = eval(user_agents[0])
    except:
        logging.warning("Failed to parse user agent list")
        pass

    return user_agents


user_agents_list = generate_random_user_agent_list()


def random_user_agent() -> dict:
    """select a random user-agent from the list

    Returns:
        random_user_agent : dict
    """
    random_user_agent = {"user-agent": random.choice(user_agents_list)["ua"]}
    return random_user_agent


def retrieve_data_json(url_to_get) -> dict:
    """Retrieve JSON datas from the URL

    Parameters:
    url_to_get: previously generated URL where to get datas

    Returns:
    data_json: dict
    """
    user_agent = random_user_agent()
    website_response = requests.get(url_to_get, headers=user_agent)
    if website_response.status_code == 200:
        data_json = website_response.json()
    # Process the JSON data as needed
    else:
        logging.error(
            f"Request failed with status code:", {website_response.status_code}
        )
    return data_json


def convert_to_dataframe(data_with_json):
    """Convert dict to dataframe with pandas

    Parameters:
    filtered_output: filtered JSON datas

    Returns:
    dataframe_database: DataFrame
    """
    dataframe_database = pandas.DataFrame(data_with_json)
    return dataframe_database


def department_get_only_needed_data(data_dataframe_initial):
    """Filter to keep only needed JSON datas

    Parameters:
    data_json: raw JSON retrived datas

    Returns:
    filtered_output: DataFrame
    """
    filtered_output = [item["properties"]
                       for item in data_dataframe_initial["features"]]
    return filtered_output


def department_remove_unused_informations(data_dataframe_to_clean):
    """Sort columns and remove unused informations for further treatments

    Parameters:
    dataframe_database: original dataframe

    Returns:
    cleaned_database: dataframe
    """
    data_dataframe_to_clean.sort_index(axis=1, inplace=True)  # par ordre alphabétique
    cleaned_database = data_dataframe_to_clean.drop(
        columns=["peuple", "codeRegion", "codeCommune", "_SRID"]
    )
    return cleaned_database


def department_remove_empty_data(data_dataframe_to_convert) -> list:
    """Remove empty rows if volume has no value

    Parameters:
    cleaned_database: modified dataframe

    Returns:
    colonne_insee: list
    """
    department_final_database = data_dataframe_to_convert[data_dataframe_to_convert["volume"].notna(
    )]
    # keep only the codeInsee column and convert into list
    colonne_insee = department_final_database["codeInsee"].values.tolist()
    return colonne_insee


def communes_url(list_in_entry, annee, data_type) -> list:
    url_generated = []
    for commune_scrape in list_in_entry:
        # Créer une liste des url à scraper par type, commune et année considérée
        url_generated.append(
            f"https://bnpe.eaufrance.fr/Bnpe-Diffusion/synthese/synthese_commune_{data_type}?&insee_com={commune_scrape}&annee={annee}&ecrasant=false"
        )
    return url_generated


def communes_get_datas(input, annee, departement, colonne, data_type):
    temporary = pandas.DataFrame(
        {}
    )  # initialize dataframe and reset it at each function call
    logging.info(
        f"année : {annee}, département : {departement}, type : {data_type}, itération : {len(input)+1}"
    )

    for url_number in range(len(input)):

        data_json = retrieve_data_json(input[url_number])
        dataframe_json = convert_to_dataframe(data_json)
        # add columns "annee" and "codeinsee"
        dataframe_json.insert(0, "annee", annee, True)
        dataframe_json.insert(1, "departement", departement, True)
        dataframe_json.insert(2, "codeinsee", colonne[url_number], True)
        # Mettre à jour avec les données collectées
        temporary = pandas.concat([temporary, dataframe_json])
    # test to write file only if the dataframe is not empty
    if temporary.empty == True:
        logging.warning(
            f"année : {annee}, département :{departement}, type : {data_type}, aucune donnée à sauvegarder"
        )
    else:
        temporary.rename(
            columns={temporary.columns[4]: "code",
                     temporary.columns[5]: "libelle"},
            inplace=True,
        )
        os.makedirs(f"data/bnpe/", exist_ok=True)
        temporary.to_csv(
            f"data/bnpe/{departement}_{annee}_{data_type}_output.csv", index=False
        )


def main():
    """
    """    
    for annee_scrape in range(STARTING_YEAR, current_year):
        bnpe_generated_url = f"https://bnpe.eaufrance.fr/Bnpe-Diffusion/synthese/synthese_geographique?&code_dep={DEPARTEMENT_SCRAPE}&annee={annee_scrape}&ecrasant=false"
        department_data_json = retrieve_data_json(bnpe_generated_url)
        department_filtered_output = department_get_only_needed_data(
            department_data_json)
        department_dataframe_database = convert_to_dataframe(
            department_filtered_output)
        department_cleaned_database = department_remove_unused_informations(
            department_dataframe_database)
        colonne_insee = department_remove_empty_data(
            department_cleaned_database)
        # Generate the lists of URL to retrieve searched information per towns in the department
        usage = communes_url(colonne_insee, annee_scrape, "usage")
        eau = communes_url(colonne_insee, annee_scrape, "type_eau")
        communes_get_datas(usage, annee_scrape, DEPARTEMENT_SCRAPE, colonne_insee, "usage")
        communes_get_datas(eau, annee_scrape, DEPARTEMENT_SCRAPE, colonne_insee, "type_eau")


if __name__ == "__main__":
    main()
