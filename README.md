# API ANA - Coletor de Dados Hidrológicos

Script Python para coleta automatizada de dados de nível de rios através da API HidroWeb da ANA (Agência Nacional de Águas e Saneamento Básico).

## Sobre o Projeto

Esse script faz parte de um sistema de monitoramento em tempo real do nível do Rio Guaíba, desenvolvido para fornecer dados precisos através de um aplicativo móvel sem fins lucrativos.

### Estações Monitoradas

- **Cais Mauá C6** (87450004) - Principal
- **Gasômetro** (87444000) - Em testes
- **Guaíba** (87242000) - Em testes

## Funcionalidades

- Coleta automática a cada 30 minutos
- Autenticação automática com API ANA
- Formatação de dados para Firebase Realtime Database
- Tratamento de erros e logs detalhados
- Suporte a múltiplas estações

## Tecnologias

- **Python 3.x**
- **requests** - Comunicação com API
- **schedule** - Agendamento de tarefas
- **JSON** - Manipulação de dados

## Instalação

```bash
# Clone o repositório
git clone https://github.com/MarcoEngenhariaIoT/apiANA.git

# Entre no diretório
cd apiANA

# Instale as dependências
pip install requests schedule
```

## Configuração

### 1. Credenciais ANA

Crie um arquivo de configuração para cada estação:

**Exemplo `caisMaua.log`:**

```json
{
  "identificador": "SEU_CPF_OU_CNPJ",
  "senha": "SUA_SENHA",
  "codigo_estacao": "87450004"
}
```

### 2. Execução

```bash
# Coleta única
python coletor_guaiba.py

# Coleta automática (30min)
python aut30min.py
```

## Estrutura de Arquivos

```
apiANA/
├── coletor_guaiba.py          # Coletor principal
├── aut30min.py                # Agendador automático
├── nivel.json                 # Dados formatados para Firebase
├── caisMaua.log               # Credenciais da estação
├── README.md
├── LICENSE
└── .gitignore
```

## Uso Avançado

### Monitorar Estação Específica

Edite `coletor_guaiba.py` linha 8:

```python
with open("caisMaua.log") as f:  # Altere para estação desejada
```

### Ajuste de Frequência

Em `aut30min.py` linha 18:

```python
schedule.every(30).minutes.do(coletar_com_log)  # Altere o intervalo
```

## Saída de Dados

### Arquivo `nivel.json` (Firebase)

```json
{
  "nivel": "0.45m",
  "data_medicao": "01/11/2025 15:00"
}
```

## Licença

Distribuído sob licença MIT. Veja `LICENSE` para mais informações.

## Avisos Importantes

- Mantenha arquivos `.log` fora do versionamento
- Tokens ANA expiram em 15 minutos
- Sistema requer credenciais válidas da ANA
- Dados sujeitos à disponibilidade da API oficial

## Suporte

Em caso de problemas com:

- Configuração das credenciais
- Acesso à API ANA
- Interpretação dos dados

Contate a ANA através do email: `hidro@ana.gov.br`

---

**Desenvolvido por Marco Aurélio Machado**  
Engenheiro de Controle e Automação
[LinkedIn](https://www.linkedin.com/in/engenheiro-marco-aurelio-machado/)

```

```
