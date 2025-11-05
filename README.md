# 🥩 Inteligência Competitiva - Casa de Carnes Europa

Dashboard web para análise competitiva de açougues usando Google Places API e análise de sentimento com NLTK.

## 📋 Sobre o Projeto

Sistema desenvolvido para a disciplina de Tecnologias de Informação e do Conhecimento. 
A persona criada, o **Sr. João** (proprietário da Casa de Carnes Europa), possui o objetivo de monitorar a satisfação dos clientes e comparar performance com concorrentes locais em Belo Horizonte/MG.

### 🎯 Funcionalidades

- **Coleta Automática**: Busca concorrentes via Google Places API
- **Análise de Sentimento**: Classificação NLTK VADER (Positivo/Negativo/Neutro)
- **Classificação de Tópicos**: Qualidade, Preço, Atendimento, Limpeza, Variedade
- **Benchmark Competitivo**: Comparação de notas e risco de negatividade
- **Visualizações Interativas**: Gráficos de barras, pizza e tabelas detalhadas

## 🏗️ Arquitetura

```
IC_CasaDeCarnesEuropa/
├── ic_backend/          # Backend Flask (Python)
│   ├── app.py          # API principal
│   └── requirements.txt # Dependências Python
├── ic_frontend/         # Frontend React
│   ├── public/         # Arquivos estáticos
│   ├── src/           # Código fonte React
│   │   ├── components/ # Componentes reutilizáveis
│   │   ├── App.js     # Componente principal
│   │   └── index.css  # Estilos globais
│   └── package.json   # Dependências Node.js
└── README.md
```

## 🚀 Como Executar

### Pré-requisitos

- **Python 3.8+**
- **Node.js 16+**
- **Chave da API Google Places** ([Obter aqui](https://developers.google.com/maps/documentation/places/web-service/get-api-key))

### 1️⃣ Backend (Flask)

```bash
# Navegar para o diretório do backend
cd ic_backend

# Instalar dependências Python
pip install -r requirements.txt

# Executar servidor Flask
python app.py
```

✅ **Backend disponível em:** `http://localhost:5000`

### 2️⃣ Frontend (React)

```bash
# Navegar para o diretório do frontend
cd ic_frontend

# Instalar dependências Node.js
npm install

# Executar servidor de desenvolvimento
npm start
```

✅ **Frontend disponível em:** `http://localhost:3000`

## 🔧 Configuração

1. **Obter API Key do Google Places**
   - Acesse [Google Cloud Console](https://console.cloud.google.com/)
   - Ative a API "Places API"
   - Gere uma chave de API

2. **Configurar Localização**
   - **Latitude/Longitude**: Coordenadas da Casa Europa (-19.80188, -43.96871)
   - **Raio**: Distância de busca em km (padrão: 5km)
   - **Palavra-chave**: Termo de busca (padrão: "açougue")

## 📊 Dashboards Disponíveis

### 🏆 Performance Competitiva
- Gráfico combinado: Nota Média vs Risco de Negatividade
- Identifica concorrentes vulneráveis e líderes de mercado

### 📈 Análise de Tópicos
- Sentimento por categoria de negócio
- Priorização de melhorias operacionais

### 🥧 Concentração de Negatividade
- Distribuição de críticas entre concorrentes
- Oportunidades de captação de clientes insatisfeitos

### 📋 Tabelas Detalhadas
- Análise de sentimento por avaliação
- Mapeamento de tópicos por empresa
- Rankings de desempenho

## 🛠️ Tecnologias Utilizadas

### Backend
- **Flask**: Framework web Python
- **NLTK VADER**: Análise de sentimento
- **Requests**: Integração com Google Places API
- **Unidecode**: Processamento de texto

### Frontend
- **React**: Interface de usuário
- **Recharts**: Visualizações interativas
- **Axios**: Comunicação com API
- **CSS Grid/Flexbox**: Layout responsivo

## 📡 API Endpoints

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `POST` | `/api/analyze` | Executa análise competitiva completa |
| `GET` | `/api/health` | Verifica status da API |

### Exemplo de Requisição

```json
{
  "api_key": "sua_chave_google_places",
  "latitude": -19.80188,
  "longitude": -43.96871,
  "radius": 5,
  "keyword": "açougue"
}
```

## 🎯 KIQs (Questões-Chave de Inteligência)

### KIQ 1: Análise de Aspectos
**Pergunta**: Quais aspectos são mais mencionados positiva/negativamente?
**Resposta**: Gráfico de tópicos com % de sentimento por categoria

### KIQ 2: Benchmark Competitivo
**Pergunta**: Como a Casa Europa se compara aos concorrentes?
**Resposta**: Ranking de notas médias e risco de negatividade

## ⚠️ Limitações

- **Volume de Dados**: Google Places API retorna máximo 5 avaliações por local
- **Cobertura**: Apenas clientes que avaliam online
- **Rate Limiting**: Pausas entre requisições para evitar bloqueios
- **Idioma**: Otimizado para português brasileiro

## 🔄 Próximas Melhorias

- [ ] Alertas automáticos por email
- [ ] Análise temporal (tendências)
- [ ] Relatórios em PDF
- [ ] Integração com redes sociais
- [ ] Monitoramento de preços

## 📞 Suporte

Para dúvidas ou problemas:
1. Verifique se as APIs estão funcionando
2. Confirme se a chave do Google Places está válida
3. Verifique os logs do console (F12)

---

**Desenvolvido para Casa de Carnes Europa** 🥩
*Transformando dados em decisões estratégicas*

_Por: Ana Luíza Gonçalves Leite_