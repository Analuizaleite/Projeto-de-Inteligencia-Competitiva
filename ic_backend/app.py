from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
import time
import json
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
import re
from unidecode import unidecode
from collections import Counter

app = Flask(__name__)
CORS(app)

# Download NLTK data
try:
    nltk.download('vader_lexicon', quiet=True)
except:
    pass

class CompetitiveAnalysis:
    def __init__(self, api_key):
        self.api_key = api_key
        self.analyzer = SentimentIntensityAnalyzer()
        
    def find_nearby_competitors(self, latitude, longitude, radius_km, keyword):
        RADIUS_M = radius_km * 1000
        NEARBY_SEARCH_URL = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
        
        params = {
            'location': f"{latitude},{longitude}",
            'radius': RADIUS_M,
            'keyword': keyword,
            'type': 'store',
            'key': self.api_key
        }
        
        try:
            response = requests.get(NEARBY_SEARCH_URL, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            place_ids = {}
            if data['status'] == 'OK' and data['results']:
                for result in data['results']:
                    if result.get('place_id'):
                        place_ids[result['name']] = result['place_id']
            
            return place_ids
        except Exception as e:
            print(f"Erro na busca: {e}")
            return {}
    
    def get_reviews_from_place_id(self, place_id, name):
        DETAILS_URL = "https://maps.googleapis.com/maps/api/place/details/json"
        
        params = {
            'place_id': place_id,
            'fields': 'name,rating,reviews',
            'key': self.api_key,
            'language': 'pt'
        }
        
        try:
            response = requests.get(DETAILS_URL, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            reviews_data = []
            if data['status'] == 'OK' and 'reviews' in data['result']:
                for review in data['result']['reviews']:
                    reviews_data.append({
                        'Empresa': name,
                        'Place_ID': place_id,
                        'Nota_Avaliacao_Individual': review.get('rating'),
                        'Data_Textual': review.get('relative_time_description'),
                        'Texto_Avaliacao': review.get('text'),
                        'Nota_Media_Geral': data['result'].get('rating')
                    })
            
            return reviews_data
        except Exception as e:
            print(f"Erro ao obter reviews para {name}: {e}")
            return []
    
    def analyze_sentiment(self, text):
        if not text or text == '' or text is None:
            return 0, 'Neutro'
        
        score = self.analyzer.polarity_scores(str(text))['compound']
        
        if score >= 0.05:
            category = 'Positivo'
        elif score <= -0.05:
            category = 'Negativo'
        else:
            category = 'Neutro'
            
        return score, category
    
    def classify_topics(self, text):
        termos_chave = {
            'Qualidade': ['carne', 'corte', 'picanha', 'macia', 'selecao', 'excelente', 'fresca'],
            'Preço': ['caro', 'preco', 'custo', 'salgado', 'barato', 'promocao'],
            'Atendimento': ['atendimento', 'vendedor', 'balcao', 'funcionario', 'educado', 'pessoal', 'rapido'],
            'Limpeza_Ambiente': ['limpeza', 'sujo', 'ambiente', 'organizado', 'estrutura', 'higiene'],
            'Variedade': ['variedade', 'opcoes', 'diversidade', 'poucas']
        }
        
        topics = []
        processed_text = unidecode(str(text).lower())
        
        for categoria, palavras in termos_chave.items():
            for palavra in palavras:
                if re.search(r'\b' + re.escape(palavra) + r'\b', processed_text):
                    topics.append(categoria)
                    break
        
        return topics if topics else ['Outros']

@app.route('/api/analyze', methods=['POST'])
def analyze_competitors():
    try:
        data = request.json
        api_key = data.get('api_key')
        latitude = data.get('latitude', -19.80188)
        longitude = data.get('longitude', -43.96871)
        radius = data.get('radius', 5)
        keyword = data.get('keyword', 'açougue')
        
        if not api_key:
            return jsonify({'error': 'API key é obrigatória'}), 400
        
        analyzer = CompetitiveAnalysis(api_key)
        
        # Buscar concorrentes
        competitors = analyzer.find_nearby_competitors(latitude, longitude, radius, keyword)
        
        if not competitors:
            return jsonify({'error': 'Nenhum concorrente encontrado'}), 404
        
        # Coletar reviews
        all_reviews = []
        for name, place_id in competitors.items():
            reviews = analyzer.get_reviews_from_place_id(place_id, name)
            all_reviews.extend(reviews)
            time.sleep(0.5)  # Rate limiting
        
        if not all_reviews:
            return jsonify({'error': 'Nenhuma avaliação encontrada'}), 404
        
        # Processar dados sem pandas
        unique_reviews = []
        seen = set()
        for review in all_reviews:
            key = (review['Texto_Avaliacao'], review['Empresa'])
            if key not in seen:
                seen.add(key)
                # Análise de sentimento
                score, category = analyzer.analyze_sentiment(review['Texto_Avaliacao'])
                review['Sentimento_Score'] = score
                review['Sentimento_Categoria'] = category
                # Classificação de tópicos
                review['Topicos'] = analyzer.classify_topics(review['Texto_Avaliacao'])
                unique_reviews.append(review)
        
        # Gerar métricas
        benchmark = generate_benchmark(unique_reviews)
        topic_analysis = generate_topic_analysis(unique_reviews)
        
        # Gerar análise de concentração de negatividade
        negativity_concentration = generate_negativity_concentration(unique_reviews)
        
        # Gerar tabelas adicionais
        sentiment_sample = generate_sentiment_sample(unique_reviews)
        topic_mapping = generate_topic_mapping(unique_reviews)
        
        return jsonify({
            'benchmark': benchmark,
            'topic_analysis': topic_analysis,
            'negativity_concentration': negativity_concentration,
            'sentiment_sample': sentiment_sample,
            'topic_mapping': topic_mapping,
            'total_reviews': len(unique_reviews),
            'competitors_found': len(competitors)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def generate_benchmark(reviews):
    # Análise por empresa
    empresa_stats = []
    empresas = list(set(review['Empresa'] for review in reviews))
    
    for empresa in empresas:
        empresa_reviews = [r for r in reviews if r['Empresa'] == empresa]
        
        total_reviews = len(empresa_reviews)
        avg_rating = empresa_reviews[0]['Nota_Media_Geral'] if empresa_reviews else 0
        
        negative_count = sum(1 for r in empresa_reviews if r['Sentimento_Categoria'] == 'Negativo')
        negative_pct = (negative_count / total_reviews) * 100 if total_reviews > 0 else 0
        
        empresa_stats.append({
            'empresa': empresa,
            'nota_media': round(avg_rating, 1),
            'total_mencoes': total_reviews,
            'risco_negatividade': round(negative_pct, 1)
        })
    
    return sorted(empresa_stats, key=lambda x: x['nota_media'], reverse=True)

def generate_topic_analysis(reviews):
    # Expandir tópicos
    expanded_data = []
    for review in reviews:
        for topic in review['Topicos']:
            expanded_data.append({
                'topico': topic,
                'sentimento': review['Sentimento_Categoria']
            })
    
    # Análise por tópico
    topic_stats = []
    topics = list(set(item['topico'] for item in expanded_data if item['topico'] != 'Outros'))
    
    for topic in topics:
        topic_data = [item for item in expanded_data if item['topico'] == topic]
        
        total = len(topic_data)
        positive = sum(1 for item in topic_data if item['sentimento'] == 'Positivo')
        negative = sum(1 for item in topic_data if item['sentimento'] == 'Negativo')
        
        positive_pct = (positive / total) * 100 if total > 0 else 0
        negative_pct = (negative / total) * 100 if total > 0 else 0
        
        topic_stats.append({
            'topico': topic,
            'total_mencoes': total,
            'positivo_pct': round(positive_pct, 1),
            'negativo_pct': round(negative_pct, 1)
        })
    
    return sorted(topic_stats, key=lambda x: x['negativo_pct'], reverse=True)

def generate_negativity_concentration(reviews):
    # Filtrar apenas avaliações negativas
    negative_reviews = [r for r in reviews if r['Sentimento_Categoria'] == 'Negativo']
    
    if not negative_reviews:
        return []
    
    # Contar negatividade por empresa
    empresa_negative_count = {}
    for review in negative_reviews:
        empresa = review['Empresa']
        empresa_negative_count[empresa] = empresa_negative_count.get(empresa, 0) + 1
    
    # Calcular percentual de concentração
    total_negative = sum(empresa_negative_count.values())
    
    concentration_data = []
    for empresa, count in empresa_negative_count.items():
        percentage = (count / total_negative) * 100
        concentration_data.append({
            'empresa': empresa,
            'negative_count': count,
            'percentage': round(percentage, 1)
        })
    
    return sorted(concentration_data, key=lambda x: x['percentage'], reverse=True)

def generate_sentiment_sample(reviews):
    # Amostra de análise de sentimento (primeiras 10 avaliações)
    sample_data = []
    for i, review in enumerate(reviews[:10]):
        sample_data.append({
            'empresa': review['Empresa'],
            'texto_avaliacao': review['Texto_Avaliacao'][:100] + '...' if len(review['Texto_Avaliacao']) > 100 else review['Texto_Avaliacao'],
            'nota_individual': review['Nota_Avaliacao_Individual'],
            'sentimento_score': round(review['Sentimento_Score'], 3),
            'sentimento_categoria': review['Sentimento_Categoria']
        })
    return sample_data

def generate_topic_mapping(reviews):
    # Mapeamento de tópicos (primeiras 10 avaliações com tópicos)
    mapping_data = []
    count = 0
    for review in reviews:
        if count >= 10:
            break
        if review['Topicos'] and review['Topicos'] != ['Outros']:
            mapping_data.append({
                'empresa': review['Empresa'],
                'topicos_encontrados': ', '.join(review['Topicos']),
                'sentimento_categoria': review['Sentimento_Categoria']
            })
            count += 1
    return mapping_data

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'OK', 'message': 'API funcionando'})

if __name__ == '__main__':
    app.run(debug=True, port=5000)