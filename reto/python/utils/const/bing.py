MAPS_API_KEY = "ApGQtt9FSO3BaeUDBmsBWgS_S6bwQQqANNI8fZFZHYtjVUI8piSEc9Xh7ZAr5Jx4"

# === LOCATIONS LAT/LON API PARAMETERS ===

LOCATIONS_URL_LAYOUT = "http://dev.virtualearth.net/REST/v1/Locations?countryRegion={countryRegion}&adminDistrict={adminDistrict}&locality={locality}&postalCode={postalCode}&addressLine={addressLine}&includeNeighborhood={includeNeighborhood}&maxResults={maxResults}&key={BingMapsKey}"


DMATRIX_URL_LAYOUT = (
    "https://dev.virtualearth.net/REST/v1/Routes/DistanceMatrix?key={BingMapsKey}"
)

# === DISTANCE MATRIX API PARAMETERS ===

CONTENT_LENGTH = "2500"
CONTENT_TYPE = "application/json"

POST_HEADERS = {"content-length": CONTENT_LENGTH, "content-type": CONTENT_TYPE}
