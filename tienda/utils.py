import requests

def clp_a_usd(clp_amount, api_key, tasa_respaldo=900):
    url = (
        f"https://api.exchangerate.host/convert"
        f"?access_key={api_key}"
        f"&from=CLP&to=USD&amount={clp_amount}"
    )

    try:
        response = requests.get(url, timeout=5)
        data = response.json()

        if response.status_code != 200 or not data.get("success", False):
            raise Exception("Fallo la API")

        return round(data["result"], 2)

    except Exception as e:
        print(f"[Aviso] Error al obtener tasa CLP→USD, usando tasa fija: {tasa_respaldo} CLP/USD. Detalle: {e}")
        return round(clp_amount / tasa_respaldo, 2)
