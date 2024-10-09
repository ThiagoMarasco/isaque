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

# Lista de proxies
proxies_list = [
    "https://spchdses18:fyTmb5szFC5_z8le3Q@gate.smartproxy.com:10001",
    "https://spchdses18:fyTmb5szFC5_z8le3Q@gate.smartproxy.com:10002",
    "https://spchdses18:fyTmb5szFC5_z8le3Q@gate.smartproxy.com:10003",
    "https://spchdses18:fyTmb5szFC5_z8le3Q@gate.smartproxy.com:10004",
    "https://spchdses18:fyTmb5szFC5_z8le3Q@gate.smartproxy.com:10005",
    "https://spchdses18:fyTmb5szFC5_z8le3Q@gate.smartproxy.com:10006",
    "https://spchdses18:fyTmb5szFC5_z8le3Q@gate.smartproxy.com:10007",
    "https://spchdses18:fyTmb5szFC5_z8le3Q@gate.smartproxy.com:10008",
    "https://spchdses18:fyTmb5szFC5_z8le3Q@gate.smartproxy.com:10009",
    "https://spchdses18:fyTmb5szFC5_z8le3Q@gate.smartproxy.com:10010"
]

# Set para rastrear proxies bloqueados
blocked_proxies = {}

def fetch_data(url, data):
    """Função para fazer requisições POST e retornar os dados."""
    max_retries = 20
    retries = 0
    
    while retries < max_retries:
        available_proxies = [proxy for proxy in proxies_list if proxy not in blocked_proxies]
        
        if not available_proxies:
            print("Todos os proxies estão bloqueados. Aguardando 120 segundos.")
            time.sleep(120)
            blocked_proxies.clear()
            continue
        
        proxy = random.choice(available_proxies)
        proxies = {"https": proxy}
        
        try:
            response = requests.post(url, headers=headers, data=json.dumps(data), proxies=proxies)
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 429:
                print(f"Erro 429 com proxy {proxy}. Adicionando ao bloqueio por 120 segundos.")
                blocked_proxies[proxy] = time.time() + 120
                time.sleep(5)  # Espera breve antes de tentar outro proxy
            else:
                print(f"Erro na requisição: {response.status_code} com proxy {proxy}")
                return {}
        except requests.exceptions.RequestException as e:
            print(f"Exceção ao fazer a requisição: {e} com proxy {proxy}")
            return {}

        retries += 1

    print("Número máximo de tentativas atingido. Abortando.")
    return {}

def check_blocked_proxies():
    """Remove proxies do bloqueio após o tempo especificado."""
    current_time = time.time()
    for proxy in list(blocked_proxies.keys()):
        if blocked_proxies[proxy] <= current_time:
            del blocked_proxies[proxy]

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
    check_blocked_proxies()  # Verifica e remove proxies bloqueados
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
