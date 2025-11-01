# coletor_guaiba.py
import requests
import json
from datetime import datetime

def coletar_nivel():
    # Carrega credenciais
    with open("caisMaua.log") as f: #selecionar o arquivo com as credenciais desejado conforme o local do coletor
        cred = json.load(f)
    
    # Token
    resp = requests.get(
        "https://www.ana.gov.br/hidrowebservice/EstacoesTelemetricas/OAUth/v1",
        headers={'Identificador': cred['identificador'].strip('"'), 'Senha': cred['senha'].strip('"')}
    )
    token = resp.json()['items']['tokenautenticacao']
    
    # Dados
    resp = requests.get(
        "https://www.ana.gov.br/hidrowebservice/EstacoesTelemetricas/HidroinfoanaSerieTelemetricaDetalhada/v1",
        params={
            'Código da Estação': cred['codigo_estacao'],
            'Tipo Filtro Data': 'DATA_ULTIMA_ATUALIZACAO',
            'Data de Busca (yyyy-MM-dd)': datetime.now().strftime('%Y-%m-%d'),
            'Range Intervalo de busca': 'MINUTO_30'
        },
        headers={'Authorization': f'Bearer {token}'}
    )
    
    dados = resp.json()
    
    if dados['items']:
        # Pega o item mais recente
        item = max(dados['items'], key=lambda x: x.get('Data_Hora_Medicao', ''))
        cota = float(item['Cota_Adotada'])
        data_medicao = item['Data_Hora_Medicao']
        
        nivel = (cota/100) - 0.38  # Converte a cota do sensor para nível do Guaíba em metros
        
        # Formata data/hora para DD/MM/AAAA HH:MM
        data_original = data_medicao.split('.')[0]  # Remove milissegundos
        dt = datetime.strptime(data_original, '%Y-%m-%d %H:%M:%S')
        data_formatada = dt.strftime('%d/%m/%Y %H:%M')
        
        # Dados para salvar em nivel.json (formato Firebase)
        dados_firebase = {
            'nivel': f"{nivel:.2f}m",
            'data_medicao': data_formatada
            }
        
        # Salva em nivel.json (para Firebase)
        with open('nivel.json', 'w') as f:
            json.dump(dados_firebase, f, indent=2)
           
        print(f"Guaíba: {nivel:.2f}m ({data_formatada})")
        return nivel

if __name__ == "__main__":
    coletar_nivel()