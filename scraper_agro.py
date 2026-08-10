import requests
import json
import datetime
import os

def obtener_datos_dolar():
    dolares = {
        "blue": {"compra": "N/A", "venta": "N/A"},
        "mayorista": {"compra": "N/A", "venta": "N/A"},
        "mep": {"compra": "N/A", "venta": "N/A"},
        "oficial": {"compra": "N/A", "venta": "N/A"}
    }
    
    try:
        # Usamos dolarapi.com, una API pública, gratuita y 100% confiable en Argentina
        response = requests.get("https://dolarapi.com/v1/dolares", timeout=10)
        if response.status_code == 200:
            data = response.json()
            for item in data:
                casa = item.get("casa")
                if casa == "blue":
                    dolares["blue"] = {"compra": f"${item.get('compra'):,.2f}", "venta": f"${item.get('venta'):,.2f}"}
                elif casa == "mayorista":
                    dolares["mayorista"] = {"compra": f"${item.get('compra'):,.2f}", "venta": f"${item.get('venta'):,.2f}"}
                elif casa == "mep":
                    dolares["mep"] = {"compra": f"${item.get('compra'):,.2f}", "venta": f"${item.get('venta'):,.2f}"}
                elif casa == "oficial":
                    dolares["oficial"] = {"compra": f"${item.get('compra'):,.2f}", "venta": f"${item.get('venta'):,.2f}"}
            
            # Obtener el valor numérico del mayorista para los cálculos de granos
            for item in data:
                if item.get("casa") == "mayorista":
                    return dolares, float(item.get("venta"))
            
            # Si no hay mayorista, usar el oficial
            for item in data:
                if item.get("casa") == "oficial":
                    return dolares, float(item.get("venta"))
                    
        return dolares, 1385.0 # Valor de respaldo si falla la API
    except Exception as e:
        print(f"Error al obtener cotizaciones del dólar: {e}")
        return dolares, 1385.0

def calcular_precios_granos(valor_dolar_mayorista):
    # En el mercado argentino, los granos se cotizan en dólares por tonelada (USD/t) 
    # y se pesifican al Dólar Mayorista (Dólar Divisa BNA) al momento de la liquidación.
    # Valores de referencia FOB/FAS promedio actuales (en USD):
    precio_usd_soja = 330.0   # Aprox 330 USD/t
    precio_usd_trigo = 215.0  # Aprox 215 USD/t
    precio_usd_maiz = 180.0   # Aprox 180 USD/t
    
    # Calculamos el precio estimado en pesos (ARS)
    soja_ars = precio_usd_soja * valor_dolar_mayorista
    trigo_ars = precio_usd_trigo * valor_dolar_mayorista
    maiz_ars = precio_usd_maiz * valor_dolar_mayorista
    
    return {
        "soja": f"${soja_ars:,.2f} ($460.200 Ref)",
        "trigo": f"${trigo_ars:,.2f} ($300.000 Ref)",
        "maiz": f"${maiz_ars:,.2f} ($249.500 Ref)",
        "soja_usd": f"USD {precio_usd_soja:.0f}",
        "trigo_usd": f"USD {precio_usd_trigo:.0f}",
        "maiz_usd": f"USD {precio_usd_maiz:.0f}"
    }

def guardar_datos():
    fecha_actual = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    print("Obteniendo cotizaciones en tiempo real...")
    dolares, valor_mayorista = obtener_datos_dolar()
    
    datos = {
        "fecha_actualizacion": fecha_actual,
        "dolares": dolares,
        "granos": calcular_precios_granos(valor_mayorista)
    }
    
    # Guardamos en el archivo JSON
    ruta_archivo = os.path.join(os.path.dirname(__file__), 'precios_agro.json')
    
    with open(ruta_archivo, 'w', encoding='utf-8') as f:
        json.dump(datos, f, ensure_ascii=False, indent=4)
        
    print(f"[OK] Datos actualizados y guardados en {ruta_archivo}")

if __name__ == "__main__":
    print("Iniciando extracción y cálculo de datos del mercado...")
    guardar_datos()
