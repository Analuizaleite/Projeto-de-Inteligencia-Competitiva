import React, { useState } from 'react';
import axios from 'axios';
import BenchmarkChart from './components/BenchmarkChart';
import TopicChart from './components/TopicChart';
import PieChart from './components/PieChart';
import DataTable from './components/DataTable';

const API_BASE_URL = 'http://localhost:5000/api';

function App() {
  const [formData, setFormData] = useState({
    api_key: '',
    latitude: -19.80188,
    longitude: -43.96871,
    radius: 5,
    keyword: 'açougue'
  });
  
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    
    try {
      const response = await axios.post(`${API_BASE_URL}/analyze`, formData);
      setResults(response.data);
    } catch (err) {
      setError(err.response?.data?.error || 'Erro ao processar análise');
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <div className="dashboard-header">
        <div className="header-content">
          <h1 className="header-title">🥩 Casa de Carnes Europa</h1>
          <p className="header-subtitle">Dashboard de Inteligência Competitiva</p>
        </div>
      </div>
      
      <div className="container">
      
      <div className="card">
        <h2>Configuração da Análise</h2>
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label>🔑 API Key do Google Places:</label>
            <input
              type="text"
              name="api_key"
              value={formData.api_key}
              onChange={handleInputChange}
              required
              placeholder="Sua chave da API do Google Places"
            />
          </div>
          
          <div className="form-grid">
            <div className="form-group">
              <label>📍 Latitude:</label>
              <input
                type="number"
                step="any"
                name="latitude"
                value={formData.latitude}
                onChange={handleInputChange}
              />
            </div>
            
            <div className="form-group">
              <label>📍 Longitude:</label>
              <input
                type="number"
                step="any"
                name="longitude"
                value={formData.longitude}
                onChange={handleInputChange}
              />
            </div>
            
            <div className="form-group">
              <label>📏 Raio (km):</label>
              <input
                type="number"
                name="radius"
                value={formData.radius}
                onChange={handleInputChange}
                min="1"
                max="50"
              />
            </div>
            
            <div className="form-group">
              <label>🔍 Palavra-chave:</label>
              <input
                type="text"
                name="keyword"
                value={formData.keyword}
                onChange={handleInputChange}
              />
            </div>
          </div>
          
          <button type="submit" className="btn" disabled={loading}>
            {loading ? 'Analisando...' : 'Iniciar Análise'}
          </button>
        </form>
      </div>

      {error && (
        <div className="error">
          {error}
        </div>
      )}

      {loading && (
        <div className="loading">
          <p>Coletando dados dos concorrentes... Isso pode levar alguns minutos.</p>
        </div>
      )}

      {results && (
        <>
          <div className="card">
            <h2>📊 Resumo da Análise</h2>
            <div className="summary-grid">
              <div className="summary-item">
                <div className="summary-number">{results.total_reviews}</div>
                <div className="summary-label">Avaliações Coletadas</div>
              </div>
              <div className="summary-item">
                <div className="summary-number">{results.competitors_found}</div>
                <div className="summary-label">Concorrentes Encontrados</div>
              </div>
            </div>
          </div>

          <div className="charts-grid">
            <div className="card chart-card">
              <h2>Performance Competitiva</h2>
              <p>Reputação vs Risco de Negatividade</p>
              <BenchmarkChart data={results.benchmark} />
            </div>

            <div className="card chart-card">
              <h2>Análise de Tópicos</h2>
              <p>Sentimento por categoria</p>
              <TopicChart data={results.topic_analysis} />
            </div>
          </div>

          <div className="card chart-card-wide">
            <h2>Concentração de Negatividade</h2>
            <p>Qual concorrente atrai mais críticas?</p>
            <PieChart data={results.negativity_concentration} />
          </div>

          <div className="tables-section">
            <div className="card">
              <h2>Tabelas Detalhadas</h2>
              <DataTable 
                data={results.benchmark} 
                columns={[
                  { key: 'empresa', label: 'Empresa' },
                  { key: 'nota_media', label: 'Nota Média' },
                  { key: 'total_mencoes', label: 'Total Menções' },
                  { key: 'risco_negatividade', label: 'Risco Negatividade (%)' }
                ]}
              />
            </div>
          </div>

          {results.sentiment_sample && (
            <div className="card">
              <h2>Análise de Sentimento: Definindo o Tom do Cliente</h2>
              <p>Amostra do tom emocional (Positivo/Negativo) atribuído a cada avaliação pelo modelo de IA.</p>
              <DataTable 
                data={results.sentiment_sample} 
                columns={[
                  { key: 'empresa', label: 'Empresa' },
                  { key: 'texto_avaliacao', label: 'Texto Avaliação' },
                  { key: 'nota_individual', label: 'Nota Individual' },
                  { key: 'sentimento_score', label: 'Score Sentimento' },
                  { key: 'sentimento_categoria', label: 'Categoria Sentimento' }
                ]}
              />
            </div>
          )}

          {results.topic_mapping && (
            <div className="card">
              <h2>Classificação Robusta de Tópicos (Mapeamento de Críticas)</h2>
              <p>Classificação automática de avaliações por tópicos de negócio.</p>
              <DataTable 
                data={results.topic_mapping} 
                columns={[
                  { key: 'empresa', label: 'Empresa' },
                  { key: 'topicos_encontrados', label: 'Tópicos Encontrados' },
                  { key: 'sentimento_categoria', label: 'Categoria Sentimento' }
                ]}
              />
            </div>
          )}
        </>
      )}
      </div>
    </>
  );
}

export default App;