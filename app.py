from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)  # CORS hatlarını engellemek için

@app.route('/index', methods=['GET', 'POST'])
def fetch_url():
    """URL içeriğini getirir"""
    
    # URL parametresini al
    if request.method == 'GET':
        site = request.args.get('url')
    else:  # POST
        data = request.get_json()
        site = data.get('url') if data else None
    
    # URL kontrolü
    if not site:
        return jsonify({
            'durum': 'hata',
            'mesaj': 'URL parametresi gerekli',
            'kullanim': 'GET: /index?url=https://google.com | POST: {"url": "https://google.com"}'
        }), 400
    
    # Çıkış kontrolü
    if site == "0":
        return jsonify({
            'durum': 'basarili',
            'mesaj': 'Çıkış yapıldı'
        }), 200
    
    try:
        # İstek gönder
        response = requests.get(site, timeout=10, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
        # Başarılı yanıt
        return jsonify({
            'durum': 'basarili',
            'url': site,
            'status_kodu': response.status_code,
            'header': dict(response.headers),
            'icerik': response.text,
            'icerik_tipi': response.headers.get('content-type', 'bilinmiyor')
        }), 200
        
    except requests.exceptions.Timeout:
        return jsonify({
            'durum': 'hata',
            'mesaj': 'İstek zaman aşımına uğradı',
            'url': site
        }), 408
        
    except requests.exceptions.ConnectionError:
        return jsonify({
            'durum': 'hata',
            'mesaj': 'Bağlantı hatası - URL geçersiz veya erişilemiyor',
            'url': site
        }), 400
        
    except Exception as e:
        return jsonify({
            'durum': 'hata',
            'mesaj': f'Beklenmeyen hata: {str(e)}',
            'url': site
        }), 500


@app.route('/index-headers', methods=['GET', 'POST'])
def fetch_headers_only():
    """Sadece header bilgilerini getirir"""
    
    if request.method == 'GET':
        site = request.args.get('url')
    else:
        data = request.get_json()
        site = data.get('url') if data else None
    
    if not site:
        return jsonify({
            'durum': 'hata',
            'mesaj': 'URL parametresi gerekli'
        }), 400
    
    try:
        response = requests.get(site, timeout=10, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
        return jsonify({
            'durum': 'basarili',
            'url': site,
            'status_kodu': response.status_code,
            'header': dict(response.headers)
        }), 200
        
    except Exception as e:
        return jsonify({
            'durum': 'hata',
            'mesaj': str(e)
        }), 500


@app.route('/', methods=['GET'])
def index():
    """API ana sayfası"""
    return jsonify({
        'api': 'Keneviz Index Çekme API',
        'versiyon': '1.0',
        'geliştirici': '@KenevizOrjin',
        'durum': 'aktif',
        'endpointler': {
            '/index': {
                'metodlar': ['GET', 'POST'],
                'aciklama': 'URL indexini getirir',
                'parametreler': {
                    'url': 'Hedef URL (örn: https://google.com)'
                },
                'ornek_kullanim': {
                    'get': '/index?url=https://google.com',
                    'post': 'POST /index ile {"url": "https://google.com"}'
                }
            },
            '/index-headers': {
                'metodlar': ['GET', 'POST'],
                'aciklama': 'Sadece header bilgilerini getirir',
                'parametreler': {
                    'url': 'Hedef URL'
                },
                'ornek_kullanim': {
                    'get': '/index-headers?url=https://google.com',
                    'post': 'POST /index-headers ile {"url": "https://google.com"}'
                }
            }
        }
    })


@app.errorhandler(404)
def not_found(error):
    """404 hatası için özel mesaj"""
    return jsonify({
        'durum': 'hata',
        'mesaj': 'Sayfa bulunamadı',
        'mevcut_endpointler': ['/', '/index', '/index-headers']
    }), 404


@app.errorhandler(500)
def internal_error(error):
    """500 hatası için özel mesaj"""
    return jsonify({
        'durum': 'hata',
        'mesaj': 'Sunucu hatası oluştu'
    }), 500


if __name__ == "__main__":
    print("\n" + "="*50)
    print("🚀 Keneviz Index Çekme API Başlatılıyor...")
    print("="*50)
    print("📍 Ana Sayfa: http://127.0.0.1:5000")
    print("📍 Index Çekme: http://127.0.0.1:5000/index?url=https://google.com")
    print("📍 Header Çekme: http://127.0.0.1:5000/index-headers?url=https://google.com")
    print("="*50)
    print("✨ API hazır! Ctrl+C ile durdurulur.\n")
    
    app.run(host='0.0.0.0', port=5000, debug=True)