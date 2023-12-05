from typing import Literal

import pandas as pd
import numpy as np
import requests

from utils.const.bing import (
    MAPS_API_KEY,
    LOCATIONS_URL_LAYOUT,
    DMATRIX_URL_LAYOUT,
    POST_HEADERS,
)
from utils._logging import logger
from utils._typing import DMatrixPayload
from typing import Any


def get_location(
    countryRegion: str,
    zone: str,
    locality: str,
    addressLine: str,
    postalCode: str,
    includeNeighborhood: Literal[0, 1] = 1,
    maxResults: int = 1,
) -> tuple[float, float]:
    """
    Función que obtiene la latitud y longitud de una dirección dada.

        addr (str): dirección de la cual se quiere obtener la latitud y longitud.

    RETURNS

        latitude (float): latitud de la dirección dada.
        longitude (float): longitud de la dirección dada.
    """

    LOCATIONS_URL = LOCATIONS_URL_LAYOUT.format(
        countryRegion=countryRegion,
        adminDistrict=zone,
        locality=locality,
        addressLine=addressLine,
        includeNeighborhood=includeNeighborhood,
        maxResults=maxResults,
        postalCode=postalCode,
        BingMapsKey=MAPS_API_KEY,
    )

    response = requests.get(LOCATIONS_URL).json()

    latlon = response["resourceSets"][0]["resources"][0]["point"]["coordinates"]

    lat = latlon[0]
    lon = latlon[1]

    return (lat, lon)


def distance_matrix_payload(
    origin_coord: tuple[float, float],
    destin_coords: list[tuple[float, float]],
    travelMode="driving",
    time_unit: str = "minute",
    distance_unit: str = "km",
    start_time: str = "2023-12-01T10:00:00-06:00",
) -> DMatrixPayload:
    """
    Función que crea el payload para la API de Bing Maps Distance Matrix.

        origin_coord (tuple[float, float]): coordenadas de origen.
        destin_coords (list[tuple[float, float]]): coordenadas de destino.
        travelMode (str): modo de transporte.
        time_unit (str): unidad de tiempo.
        distance_unit (str): unidad de distancia.
        start_time (str): tiempo de inicio.

    RETURNS

        payload (dict): payload para la API de Bing Maps Distance Matrix.

    """

    origin_point_locations = [
        {
            "latitude": origin_coord[0],
            "longitude": origin_coord[1],
        }
    ]

    destin_point_locations = [
        {
            "latitude": location[0],
            "longitude": location[1],
        }
        for location in destin_coords
    ]

    payload: DMatrixPayload = dict(
        origins=origin_point_locations,
        destinations=destin_point_locations,
        travelMode=travelMode,
        timeUnit=time_unit,
        distanceUnit=distance_unit,
        startTime=start_time,
    )

    return payload


def distance_vector(
    post_payload: DMatrixPayload,
    origin_index: int,
) -> dict[str, Any]:
    """
    Función que obtiene el vector de distancias de una dirección dada.

        post_payload (dict): payload para la API de Bing Maps Distance Matrix.
        origin_index (int): índice de la dirección de origen en el vector de distancias.

    RETURNS

        dvector (list[float]): vector de distancias.
    """

    response = requests.post(
        DMATRIX_URL_LAYOUT.format(BingMapsKey=MAPS_API_KEY),
        json=post_payload,
        headers=POST_HEADERS,
    ).json()

    dvector = [
        result["travelDuration"]
        for result in response["resourceSets"][0]["resources"][0]["results"]
    ]

    dvector.insert(origin_index, 0)

    return dvector


def distance_matrix(locations_coords: pd.DataFrame) -> dict[int, list[float]]:
    """
    Función que obtiene la matriz de distancias de un conjunto de direcciones.

        locations_coords (pd.DataFrame): DataFrame con las coordenadas de las direcciones.

    RETURNS

        distance_matrix (dict[int, list[float]]): matriz de distancias.
    """
    distance_matrix = dict()
    for orig_id, orig in locations_coords.iterrows():
        print(f"CURRENT ORIGIN: {orig_id}")
        destinies = locations_coords[locations_coords.index != orig_id]

        origin_location = orig[["lat", "lon"]].to_list()
        destin_locations = destinies[["lat", "lon"]].to_records(index=False).tolist()

        vector_distances_payload = distance_matrix_payload(
            origin_coord=origin_location,
            destin_coords=destin_locations,
            travelMode="driving",
            time_unit="minute",
            distance_unit="km",
            start_time="2023-12-01T10:00:00-06:00",
        )

        dvector = distance_vector(
            post_payload=vector_distances_payload,
            origin_index=orig_id,
        )

        distance_matrix.update({orig.name: dvector})

    return distance_matrix
