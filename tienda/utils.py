import requests

def clp_a_usd(clp_amount, api_key):
    url = (
        f"https://api.exchangerate.host/convert"
        f"?access_key={api_key}"
        f"&from=CLP&to=USD&amount={clp_amount}"
    )

    response = requests.get(url)
    data = response.json()

    if response.status_code != 200 or not data.get("success", False):
        raise Exception(f"Error al convertir moneda: {data.get('error', 'Sin detalles')}")

    return round(data["result"], 2)
