````markdown
# API ANA - Monitor de Nível do Guaíba

Sistema Python para monitoramento automatizado do nível do Rio Guaíba através da API HidroWeb da ANA (Agência Nacional de Águas e Saneamento Básico) com integração Firebase.

## Sobre o Projeto

Este sistema foi desenvolvido para fornecer dados em tempo real do nível do Rio Guaíba através de um aplicativo móvel sem fins lucrativos. Coletamos dados da estação Cais Mauá C6 da ANA e disponibilizamos via Firebase Realtime Database para o aplicativo de monitoramento.

**Importante**: Este código foi desenvolvido com base no exemplo oficial fornecido pela ANA conforme a documentação "manual-hidrowebservice_publica.pdf" anexo nesse repositório. Adaptamos e expandimos a funcionalidade básica para atender às necessidades específicas de monitoramento contínuo.

## Dados Públicos e Conformidade Legal

Todos os dados hidrológicos coletados são **públicos e abertos**, fornecidos pela ANA através de sua API oficial. Esses dados não contêm informações pessoais ou sensíveis, estando em conformidade com a Lei Geral de Proteção de Dados (LGPD) por se tratarem de:

- Dados hidrometeorológicos de domínio público
- Informações ambientais de interesse coletivo
- Dados oficiais disponibilizados por órgão público
- Estatísticas e medições sem vínculo com pessoas físicas

## Base Técnica

O núcleo de comunicação com a API ANA foi implementado seguindo a documentação oficial e exemplos de código disponibilizados pela Agência Nacional de Águas. A ANA fornece exemplos de como autenticar e consumir seus serviços web, que serviram como ponto de partida para este projeto.

As principais adaptações realizadas foram:

- Código feito em Python 3
- Implementação de coleta automática periódica
- Integração com Firebase para disponibilização em tempo real
- Sistema de detecção de mudanças para otimização de tráfego
- Utilizado o padrão Singleton aumentando a confiabilidade

## Funcionalidades

- Coleta automática a cada 30 minutos da API da ANA
- Integração em tempo real com Firebase
- Detecção inteligente de mudanças (evita dados duplicados)
- Tratamento robusto de erros e reconexões
- Formatação padronizada dos dados para aplicativos
- Configuração simplificada via arquivos externos

## Arquitetura

O sistema no padrão Singleton, garantindo que apenas uma instância do monitor esteja em execução. Isso melhora a confiabilidade e facilita a manutenção do código.

A estrutura básica de autenticação e consumo da API mantém a lógica original recomendada pela ANA, com adições para robustez e integração com outras plataformas.

## Tecnologias Utilizadas

- **Python 3.x** - Linguagem principal
- **Firebase Admin SDK** - Integração com banco de dados Real Time Database
- **Requests** - Comunicação com APIs
- **Schedule** - Agendamento de tarefas
- **JSON** - Manipulação de dados

## Instalação

```bash
# Clone o repositório
git clone https://github.com/MarcoEngenhariaIoT/apiANA.git

# Entre no diretório
cd apiANA

# Instale as dependências
pip install requests schedule firebase-admin
```
````

## Configuração

### 1. Credenciais da ANA

Crie o arquivo `caisMaua.log` com suas credenciais de acesso fornecidos pelo ANA seguindo o formato:

```json
{
  "identificador": "SEU_CPF_OU_CNPJ",
  "senha": "SUA_SENHA",
  "codigo_estacao": "87450004"
}
```

### 2. Configuração do Firebase

Crie o arquivo `firebase.log` com a configuração do Firebase:

```json
{
  "firebase_config": "caminho/para/serviceAccountKey.json",
  "databaseURL": "https://seu-projeto.firebaseio.com"
}
```

### 3. Execução

```bash
# Inicia o monitoramento automático
python apiANA.py
```

O sistema iniciará imediatamente uma coleta e continuará executando a cada 30 minutos.

## Estrutura do Projeto

```
apiANA/
├── apiANA.py                 # Sistema principal
├── caisMaua.log              # Credenciais ANA (não versionado)
├── firebase.log              # Configuração Firebase (não versionado)
├── nivel.json                # Dados atuais (gerado automaticamente)
├── README.md
└── LICENSE
```

## Como Funciona

1. **Autenticação**: O sistema obtém um token de acesso da API ANA usando o método oficial
2. **Coleta**: Busca os dados mais recentes da estação Cais Mauá C6 seguindo o padrão ANA
3. **Processamento**: Converte e formata os dados para metros
4. **Verificação**: Compara com a última medição para detectar mudanças
5. **Envio**: Se houver mudança, envia para Firebase
6. **Repetição**: Agenda a próxima execução em 30 minutos

## Saída de Dados

### Firebase Realtime Database

```json
{
  "nivel": 2.45,
  "timestamp": "14:30 15-11-2024",
  "labelVersao": "Versão 2.1.0",
  "labelCotaAlerta": "Cota de alerta 3.15m",
  "labelCotaInundacao": "Cota de inundação 3.60m",
  "labelEstacao": "Estação: Cais Mauá C6",
  "gAlerta": 3.15,
  "gInundacao": 3.6
}
```

### Arquivo Local

O arquivo `nivel.json` é atualizado a cada coleta:

```json
{
  "nivel": 2.45,
  "data_medicao": "15/11/2024 14:30"
}
```

## Referência da API ANA

Este projeto utiliza a API HidroWeb da ANA conforme documentação oficial. Para entender melhor o funcionamento da API e seus endpoints, consulte:

- Portal de Desenvolvedores da ANA
- Documentação da API HidroWeb
- Exemplos de código oficiais

## Personalização

### Alterar Intervalo de Coleta

No arquivo `apiANA.py`, modifique a linha que contém:

```python
schedule.every(30).minutes.do(self.executar_coleta)
```

### Configurar Novas Estações

Edite o arquivo `caisMaua.log` com o código da estação desejada.

## Monitoramento e Logs

O sistema fornece feedback detalhado no console:

```
15/11/2024 14:30:00 - Coletando...
Firebase inicializado com sucesso
Nivel do Guaiba: 2.45m (15/11/2024 14:30) - DADO NOVO
Enviando para Firebase...
Dados enviados para Firebase
```

## Solução de Problemas

### Erro de Autenticação ANA

- Verifique se as credenciais no `caisMaua.log` estão corretas
- Confirme se o CPF/CNPJ e senha são válidos na ANA

### Erro de Conexão Firebase

- Valide o caminho do arquivo de configuração do Firebase
- Verifique se a databaseURL está correta
- Confirme as permissões do service account

### Dados Não Atualizando

- Verifique o token de acesso da ANA (expira em 15 minutos)
- Confirme se a estação está enviando dados
- Verifique a conexão com internet

## Avisos Importantes

- Este projeto é baseado na API pública da ANA mas não é um produto oficial
- Todos os dados hidrológicos são públicos e abertos ao cidadão
- O sistema é experimental e sem fins lucrativos
- Para decisões críticas, consulte sempre fontes oficiais da ANA
- Dados sujeitos à disponibilidade da API HidroWeb
- Projeto em conformidade com LGPD (dados públicos e não-pessoais)

## Licença

Distribuído sob licença MIT. Veja `LICENSE` para mais informações.

## Desenvolvimento

Este sistema foi desenvolvido por Marco Aurélio Machado, Engenheiro de Controle e Automação, como parte de um projeto de monitoramento ambiental de código aberto.

O código de comunicação com a API ANA foi baseado nos exemplos oficiais fornecidos pela agência. Para dúvidas técnicas sobre a API ANA, contate: `hidro@ana.gov.br`

---

**Última atualização**: Novembro 2025  
**Versão do Sistema**: 2.1.0  
**Base Técnica**: API HidroWeb ANA - Exemplos Oficiais  
**Status Legal**: Dados Públicos - Conforme LGPD

```

```
