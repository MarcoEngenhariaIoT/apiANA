# apiANA.py
# Sistema de monitoramento do nível do Guaíba com integração Firebase
# Coleta dados da ANA (Agência Nacional de Águas) e envia para Firebase
# Execução automática a cada 30 minutos

import time
import schedule
import requests
import json
import firebase_admin
from firebase_admin import credentials, db
from datetime import datetime

class MonitorGuaiba:
    """
    Classe principal para monitoramento do nível do Guaíba
    Implementa padrão Singleton para garantir única instância
    """
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MonitorGuaiba, cls).__new__(cls)
            cls._instance._inicializar()
        return cls._instance
    
    def _inicializar(self):
        """Inicializa variáveis e configurações do sistema"""
        
        # Configurações do aplicativo
        self.cotaAlerta = 3.15
        self.cotaInundacao = 3.60
        self.labelVersao = "Versão 2.1.0"
        self.labelCotaAlerta = "Cota de alerta 3.15m"
        self.labelCotaInundacao = "Cota de inundação 3.60m"
        self.labelEstacao = "Estação: Cais Mauá C6"
        self.labelFree = "Aplicativo experimental de uso livre sem fins lucrativos, os dados coletados podem conter erros e não nos responsabilizamos pelo mau uso dessas informações, para tomada de decisão recomendamos consultar diretamente a fonte confiável com o SNIRH/ANA."
        
        # Controle de estado
        self.nivel_anterior = None
        self.firebase_initialized = False
        
        # Inicializa Firebase
        self._inicializar_firebase()
    
    def _inicializar_firebase(self):
        """
        Inicializa conexão com Firebase
        Carrega configurações do arquivo firebase.log
        """
        try:
            with open("firebase.log") as f:
                firebase_config = json.load(f)
            
            cred_path = firebase_config['firebase_config']
            database_url = firebase_config['databaseURL']
            
            cred = credentials.Certificate(cred_path)
            firebase_admin.initialize_app(cred, {'databaseURL': database_url})
            self.firebase_initialized = True
            print("Firebase inicializado com sucesso")
            return True
        except Exception as e:
            print(f"Erro ao inicializar Firebase: {e}")
            return False
    
    def coletar_nivel(self):
        """
        Coleta nível atual do Guaíba da API da ANA
        Retorna: (nivel, houve_mudanca) onde:
          - nivel: float com nível em metros (None se erro)
          - houve_mudanca: boolean indicando se houve mudança significativa
        """
        
        try:
            # Carrega credenciais de acesso à ANA
            with open("caisMaua.log") as f:
                cred = json.load(f)
            
            # Obtém token de autenticação
            resp = requests.get(
                "https://www.ana.gov.br/hidrowebservice/EstacoesTelemetricas/OAUth/v1",
                headers={
                    'Identificador': cred['identificador'].strip('"'), 
                    'Senha': cred['senha'].strip('"')
                }
            )
            token = resp.json()['items']['tokenautenticacao']
            
            # Busca dados da estação
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
                # Encontra medição mais recente
                item = max(dados['items'], key=lambda x: x.get('Data_Hora_Medicao', ''))
                cota = float(item['Cota_Adotada'])
                data_medicao = item['Data_Hora_Medicao']
                
                nivel = cota / 100  # Converte de cm para m
                
                # Formata data/hora
                data_original = data_medicao.split('.')[0]  # Remove milissegundos
                dt = datetime.strptime(data_original, '%Y-%m-%d %H:%M:%S')
                data_formatada = dt.strftime('%d/%m/%Y %H:%M')
                
                # Salva dados em arquivo local
                dados_firebase = {
                    'nivel': nivel,
                    'data_medicao': data_formatada
                }
                
                with open('nivel.json', 'w') as f:
                    json.dump(dados_firebase, f, indent=2)
                
                # Verifica mudança significativa (arredondada para 2 casas decimais)
                nivel_arredondado = round(nivel, 2)
                if self.nivel_anterior is None or nivel_arredondado != self.nivel_anterior:
                    self.nivel_anterior = nivel_arredondado
                    print(f"Nivel do Guaiba: {nivel:.2f}m ({data_formatada}) - DADO NOVO")
                    return nivel, True
                else:
                    print(f"Nivel do Guaiba: {nivel:.2f}m ({data_formatada}) - Sem mudanca")
                    return nivel, False
            
            return None, False
            
        except Exception as e:
            print(f"Erro ao coletar nivel: {e}")
            return None, False
    
    def enviar_para_firebase(self, nivel):
        """
        Envia dados para Firebase Realtime Database
        Param: nivel - float com nível em metros
        Retorna: boolean indicando sucesso
        """
        
        if not self.firebase_initialized:
            if not self._inicializar_firebase():
                return False
        
        try:
            timestamp = datetime.now().strftime('%H:%M %d-%m-%Y')
            ref = db.reference()
            
            # Envia todos os dados para Firebase
            ref.set({
                'nivel': nivel,  # Número decimal
                'timestamp': f'"{timestamp}"',
                'labelVersao': f'"{self.labelVersao}"',
                'labelCotaAlerta': f'"{self.labelCotaAlerta}"',
                'labelCotaInundacao': f'"{self.labelCotaInundacao}"',
                'labelEstacao': f'"{self.labelEstacao}"',
                'labelFree': f'"{self.labelFree}"',
                'gAlerta': self.cotaAlerta,
                'gInundacao': self.cotaInundacao
            })
            return True
        except Exception as e:
            print(f"Erro ao enviar para Firebase: {e}")
            return False
    
    def executar_coleta(self):
        """
        Executa uma coleta completa: coleta dados e envia para Firebase se houver mudanças
        """
        print(f"{datetime.now().strftime('%d/%m/%Y %H:%M:%S')} - Coletando...")
        
        try:
            resultado = self.coletar_nivel()
            if resultado[0] is not None:  # Se tem dados
                nivel, houve_mudanca = resultado
                if houve_mudanca:
                    print("Enviando para Firebase...")
                    if self.enviar_para_firebase(nivel):
                        print("Dados enviados para Firebase")
                    else:
                        print("Erro ao enviar para Firebase")
                else:
                    print("Sem mudancas - Firebase nao atualizado")
            else:
                print("Sem dados disponiveis")
        except Exception as e:
            print(f"Erro na coleta: {e}")
    
    def iniciar_monitoramento(self):
        """
        Inicia o monitoramento automático
        Executa imediatamente e agenda a cada 30 minutos
        """
        # Executa primeira coleta imediatamente
        self.executar_coleta()
        
        # Agenda coleta a cada 30 minutos
        schedule.every(30).minutes.do(self.executar_coleta)
        
        print("Coletor automatico iniciado (30min)")
        
        # Loop principal
        while True:
            schedule.run_pending()
            time.sleep(60)

# Ponto de entrada do programa
if __name__ == "__main__":
    monitor = MonitorGuaiba()
    monitor.iniciar_monitoramento()