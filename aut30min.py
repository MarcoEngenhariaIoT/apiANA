# coletor_automatico.py
import time
import schedule
from coletor_guaiba import coletar_nivel
from datetime import datetime

def coletar_com_log():
    print(f"\n{datetime.now().strftime('%d/%m/%Y %H:%M:%S')} - Coletando...")
    try:
        nivel = coletar_nivel()
        if nivel:
            print(f"Coleta realizada com sucesso")
        else:
            print("Sem dados disponíveis")
    except Exception as e:
        print(f"Erro: {e}")

# Agenda a cada 30 minutos
schedule.every(30).minutes.do(coletar_com_log)

# Executa imediatamente
coletar_com_log()

print("Coletor automático iniciado (30min)")
while True:
    schedule.run_pending()
    time.sleep(60)