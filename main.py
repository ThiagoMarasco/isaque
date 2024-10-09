import requests
import json
import pandas as pd
import time
import random

# URLs da API
API_BASE_URL = "http://veiculos.fipe.org.br/api/veiculos"
url_marcas = f"{API_BASE_URL}/ConsultarMarcas"
url_modelo = f"{API_BASE_URL}/ConsultarModelos"
url_ano = f"{API_BASE_URL}/ConsultarAnoModelo"
url_final = f"{API_BASE_URL}/ConsultarValorComTodosParametros"

# Definindo os headers
headers = {
    "Host": "veiculos.fipe.org.br",
    "Referer": "http://veiculos.fipe.org.br",
    "Content-Type": "application/json"
}

# Set para rastrear proxies bloqueados

def fetch_data(url, data):
    """Função para fazer requisições POST e retornar os dados."""
    max_retries = 20
    retries = 0
    
    while retries < max_retries:
        
        try:
            response = requests.post(url, headers=headers, data=json.dumps(data))
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 429:
                time.sleep(120)  # Espera breve antes de tentar outro proxy
            else:
                print(f"Erro na requisição: {response.status_code} ")
                return {}
        except requests.exceptions.RequestException as e:
            print(f"Exceção ao fazer a requisição: {e}")
            return {}

        retries += 1

    print("Número máximo de tentativas atingido. Abortando.")
    return {}

def get_marca(tabela_referencia):
    data = {
        "codigoTabelaReferencia": tabela_referencia,
        "codigoTipoVeiculo": 1
    }
    return fetch_data(url_marcas, data)

def get_modelos(tabela_referencia, codigo_marca):
    data = {
        "codigoTabelaReferencia": tabela_referencia,
        "codigoTipoVeiculo": 1,
        "codigoMarca": codigo_marca
    }
    
    return fetch_data(url_modelo, data).get('Modelos', [])

def get_ano(tabela_referencia, codigo_marca, codigo_modelo):
    data = {
        "codigoTabelaReferencia": tabela_referencia,
        "codigoTipoVeiculo": 1,
        "codigoMarca": codigo_marca,
        "codigoModelo": codigo_modelo
    }
    
    return fetch_data(url_ano, data)

def get_final(tabela_referencia, codigo_marca, codigo_modelo, codigo_ano):
    ano = codigo_ano.split('-')[0]
    data = {
        "codigoTabelaReferencia": tabela_referencia,
        "codigoTipoVeiculo": 1,
        "codigoMarca": codigo_marca,
        "codigoTipoCombustivel": 1,
        "anoModelo": ano,
        "ano": codigo_ano,
        "codigoModelo": codigo_modelo,
        "tipoConsulta": "tradicional"
    }
    return fetch_data(url_final, data)

# Principal
resultados = []
marcas_permitidas = [
    "BYD", "Volvo", "JAC", "Renault", "BMW", "GWM",
    "Toyota", "Ford", "Land Rover", "Porsche",
    "GM - Chevrolet", "Jeep", "Hyundai", "Fiat",
    "VW - VolksWagen", "Honda"
]

veiculos = [
    "Dolphin EV (Elétrico)",
    "Dolphin Mini (Elétrico)",
    "King GL 1.5 16V Aut. (Hibrido)",
    "Seal (Elétrico)",
    "Song Plus 1.5 16V Aut. (Hibrido)",
    "Yuan Plus (Elétrico)",
    "EX30 E40 Core (Elétrico)",
    "C40 Pure (Elétrico)",
    "XC 60 T-8 INSC. EXPRESS. 2.0 (Hibrido)",
    "iEV 40 115cv 5p. (Elétrico)",
    "Megane E-Tech (Elétrico)",
    "KWID Intense (Elétrico)",
    "RAV4 2.5 S 4x4 Aut. (Hibrido)",
    "Corolla Cross SE 1.8 16V Aut. (Hibrido)",
    "Corolla Altis 1.8 16V Aut. (Híbrido)",
    "Hilux CD 4x4 2.8 Diesel Mec.",
    "iX 1 eDrive20 X-Line Aut. (Elétrico)",
    "iX 2 xDrive 30 M Sport (Elétrico)",
    "X3 XDRIVE 30e X-Line Turbo Aut. (Híb.)",
    "Ora 03 Skin (Elétrico)",
    "Haval H6 HEV (Hibrido)",
    "Range R. VEL. R-Dyn. S 2.0 Aut.(Híbrido)",
    "Cayenne 3.0 V6 (Híbrido)",
    "ONIX HATCH 1.0 12V Flex 5p Mec.",
    "TRACKER 1.0 Turbo 12V Flex Aut.",
    "COMPASS SPORT T270 1.3 TB 4x2 Flex Aut.",
    "Renegade T270 1.3 TB 4x2 Flex Aut.",
    "Creta Action 1.6 16V Flex Aut.",
    "HB20 Sense Plus 1.0 Flex 12V Mec.",
    "Strada Endurance 1.4 Flex 8V CS Plus",
    "Fastback 1.0 200 Turbo Flex Aut.",
    "Toro Endurance 1.3 T270 4x2 Flex Aut.",
    "ARGO 1.0 6V Flex.",
    "Nivus Sense 1.0 200 TSI Flex Aut.",
    "HR-V EX 1.5 Flex Sensing 16V 5p Aut.",
    "CITY Hatchback EX 1.5 Flex 16V Aut."
]
veiculos_upper = [veiculo.strip().replace(' ', '').replace('í', 'i').replace('.', '').upper() for veiculo in veiculos]
marcas_permitidas_upper = [marca.strip().replace(' ', '').replace('í', 'i').replace('.', '').upper() for marca in marcas_permitidas]

tabelas_referencia = list(range(298, 315))  # Mes

for tabela in tabelas_referencia:
    marcas = get_marca(tabela)
    if marcas:
        for item in marcas:
            if item['Label'].replace(' ', '').replace('í', 'i').replace('.', '').strip().upper() in marcas_permitidas_upper:
                item['codigoTabelaReferencia'] = tabela
                modelos = get_modelos(tabela, item['Value'])
                if modelos:
                    for modelo in modelos:
                        if modelo['Label'].replace(' ', '').replace('í', 'i').replace('.', '').strip().upper() in veiculos_upper:
                            anos = get_ano(tabela, item['Value'], modelo['Value'])
                            if anos:
                                ano = anos[0]
                                vehicle_data = get_final(tabela, item['Value'], modelo['Value'], ano['Value'])
                                print(vehicle_data)
                                resultados.append({
                                            'codigoTabelaReferencia': tabela,
                                            'nome_marca_carro': item['Label'],
                                            'valor_marca_carro': item['Value'],
                                            'nome_carro': modelo['Label'],
                                            'valor_carro': modelo['Value'],
                                            'nome_ano_carro': ano['Label'],
                                            'valor_ano_carro': ano['Value'],
                                            'codigo_fipe': vehicle_data.get('CodigoFipe', 'N/A'),
                                            'nome_marca_carro_final': vehicle_data.get('Marca', 'N/A'),
                                            'nome_carro_modelo': vehicle_data.get('Modelo', 'N/A'),
                                            'valor_carro_fipe': vehicle_data.get('Valor', 'N/A'),
                                            'ano_modelo_carro': vehicle_data.get('AnoModelo', 'N/A'),
                                            'combustivel': vehicle_data.get('Combustivel', 'N/A'),
                                            'mes_referencia': vehicle_data.get('MesReferencia', 'N/A'),
                                            'data_consulta': vehicle_data.get('DataConsulta', 'N/A'),
                                            'tipo_veiculo': vehicle_data.get('TipoVeiculo', 'N/A'),
                                            'sigla_combustivel': vehicle_data.get('SiglaCombustivel', 'N/A')
                                        })

df_resultados = pd.DataFrame(resultados)
df_resultados.to_csv('final.csv', index=False)
print(df_resultados)
