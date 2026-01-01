import os
import json
from flask import Flask, request, jsonify, render_template_string
from datetime import datetime

app = Flask(__name__)

# Database file
DB_FILE = "config_database.json"
# Permanent raw link
RAW_LINK = "https://your-app-name.onrender.com/raw/config"

# Initialize database
def init_database():
    if not os.path.exists(DB_FILE):
        data = {
            "encrypted_config": "",
            "version": 1,
            "last_updated": "Never",
            "total_updates": 0
        }
        save_database(data)

def load_database():
    with open(DB_FILE, 'r') as f:
        return json.load(f)

def save_database(data):
    with open(DB_FILE, 'w') as f:
        json.dump(data, f, indent=4)

# Mobile-friendly HTML Template
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>📱 Config Manager</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 15px;
        }
        .container {
            max-width: 100%;
            margin: auto;
            background: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            padding: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }
        .header {
            text-align: center;
            margin-bottom: 25px;
            padding-bottom: 15px;
            border-bottom: 2px solid #eee;
        }
        .header h1 {
            color: #333;
            font-size: 28px;
            margin-bottom: 5px;
        }
        .header p {
            color: #666;
            font-size: 14px;
        }
        .card {
            background: white;
            border-radius: 15px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.08);
            border: 1px solid #e1e1e1;
        }
        .card-title {
            color: #444;
            font-size: 18px;
            margin-bottom: 15px;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .card-title i { color: #667eea; }
        textarea {
            width: 100%;
            padding: 15px;
            border: 2px solid #e1e1e1;
            border-radius: 10px;
            font-family: 'Consolas', monospace;
            font-size: 14px;
            resize: vertical;
            min-height: 200px;
            margin-bottom: 15px;
        }
        textarea:focus {
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }
        .btn {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 15px 25px;
            border-radius: 10px;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
            width: 100%;
            transition: all 0.3s;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
        }
        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 7px 20px rgba(102, 126, 234, 0.3);
        }
        .btn:active {
            transform: translateY(0);
        }
        .link-box {
            background: #f8f9fa;
            border: 2px dashed #667eea;
            border-radius: 10px;
            padding: 15px;
            margin: 15px 0;
        }
        .link-input {
            width: 100%;
            padding: 12px;
            border: 1px solid #ddd;
            border-radius: 8px;
            font-size: 14px;
            background: white;
            color: #333;
        }
        .info-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 15px;
            margin-top: 15px;
        }
        .info-item {
            background: #f8f9fa;
            padding: 15px;
            border-radius: 10px;
            text-align: center;
        }
        .info-label {
            font-size: 12px;
            color: #666;
            margin-bottom: 5px;
        }
        .info-value {
            font-size: 20px;
            font-weight: bold;
            color: #333;
        }
        .success-msg {
            background: #d4edda;
            color: #155724;
            padding: 15px;
            border-radius: 10px;
            margin: 15px 0;
            text-align: center;
        }
        .error-msg {
            background: #f8d7da;
            color: #721c24;
            padding: 15px;
            border-radius: 10px;
            margin: 15px 0;
            text-align: center;
        }
        .footer {
            text-align: center;
            margin-top: 25px;
            padding-top: 15px;
            border-top: 1px solid #eee;
            color: #888;
            font-size: 12px;
        }
        @media (max-width: 480px) {
            .container { padding: 15px; }
            .header h1 { font-size: 24px; }
            .info-grid { grid-template-columns: 1fr; }
        }
    </style>
</head>
<body>
    <div class="container">
        <!-- Header -->
        <div class="header">
            <h1>📱 Config Manager</h1>
            <p>Update your app config anytime, anywhere</p>
        </div>
        
        {% if message %}
        <div class="{{ 'success-msg' if 'Success' in message else 'error-msg' }}">
            {{ message }}
        </div>
        {% endif %}
        
        <!-- Config Form -->
        <div class="card">
            <div class="card-title">
                <span>📝</span> Config Editor
            </div>
            <form action="/update" method="POST">
                <textarea name="config" placeholder="Paste your encrypted config here...">{{ current_config }}</textarea>
                <button type="submit" class="btn">
                    <span>💾</span> UPDATE CONFIG
                </button>
            </form>
        </div>
        
        <!-- Permanent Link -->
        <div class="card">
            <div class="card-title">
                <span>🔗</span> Permanent Raw Link
            </div>
            <p style="margin-bottom: 10px; color: #666; font-size: 14px;">
                Use this link in your app. It never changes!
            </p>
            <div class="link-box">
                <input type="text" value="{{ raw_link }}" class="link-input" readonly onclick="this.select(); copyLink()">
                <p style="margin-top: 10px; text-align: center;">
                    <button onclick="copyLink()" style="background: #28a745; padding: 8px 15px; border-radius: 5px; color: white; border: none; cursor: pointer;">
                        📋 Copy Link
                    </button>
                </p>
            </div>
        </div>
        
        <!-- Current Info -->
        <div class="card">
            <div class="card-title">
                <span>📊</span> Current Status
            </div>
            <div class="info-grid">
                <div class="info-item">
                    <div class="info-label">Version</div>
                    <div class="info-value">{{ version }}</div>
                </div>
                <div class="info-item">
                    <div class="info-label">Total Updates</div>
                    <div class="info-value">{{ total_updates }}</div>
                </div>
                <div class="info-item">
                    <div class="info-label">Last Updated</div>
                    <div class="info-value" style="font-size: 14px;">{{ last_updated }}</div>
                </div>
                <div class="info-item">
                    <div class="info-label">Config Size</div>
                    <div class="info-value">{{ config_length }} chars</div>
                </div>
            </div>
        </div>
        
        <!-- Instructions -->
        <div class="card">
            <div class="card-title">
                <span>📋</span> How to Use
            </div>
            <ol style="padding-left: 20px; color: #555; line-height: 1.6;">
                <li>Paste encrypted config in editor</li>
                <li>Click "UPDATE CONFIG"</li>
                <li>Copy the Permanent Link</li>
                <li>Use link in your app: <code style="background: #f1f1f1; padding: 2px 5px; border-radius: 3px;">{{ raw_link }}</code></li>
                <li>Update anytime - no password needed!</li>
            </ol>
        </div>
        
        <div class="footer">
            <p>⚡ Always Online • 🔄 Update Anytime • 🔒 No Login Required</p>
            <p style="margin-top: 5px;">Render Hosted • Mobile Optimized</p>
        </div>
    </div>
    
    <script>
    function copyLink() {
        var linkInput = document.querySelector('.link-input');
        linkInput.select();
        document.execCommand('copy');
        
        // Show toast
        var originalText = linkInput.value;
        linkInput.value = '✅ Link Copied!';
        setTimeout(() => {
            linkInput.value = originalText;
        }, 1500);
    }
    
    // Auto-focus textarea
    document.addEventListener('DOMContentLoaded', function() {
        var textarea = document.querySelector('textarea');
        if (textarea && textarea.value === '') {
            textarea.focus();
        }
    });
    </script>
</body>
</html>
'''

@app.route('/')
def home():
    init_database()
    data = load_database()
    
    return render_template_string(HTML_TEMPLATE,
        current_config=data.get("encrypted_config", ""),
        raw_link=RAW_LINK,
        version=data.get("version", 1),
        last_updated=data.get("last_updated", "Never"),
        total_updates=data.get("total_updates", 0),
        config_length=len(data.get("encrypted_config", "")),
        message=request.args.get('message', '')
    )

@app.route('/update', methods=['POST'])
def update_config():
    config_text = request.form.get('config', '').strip()
    
    if not config_text:
        return render_template_string(HTML_TEMPLATE,
            current_config="",
            raw_link=RAW_LINK,
            version=1,
            last_updated="Never",
            total_updates=0,
            config_length=0,
            message="❌ Error: Config cannot be empty!"
        )
    
    init_database()
    data = load_database()
    
    # Update data
    data["encrypted_config"] = config_text
    data["version"] = data.get("version", 1) + 1
    data["last_updated"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data["total_updates"] = data.get("total_updates", 0) + 1
    
    save_database(data)
    
    return render_template_string(HTML_TEMPLATE,
        current_config=config_text,
        raw_link=RAW_LINK,
        version=data["version"],
        last_updated=data["last_updated"],
        total_updates=data["total_updates"],
        config_length=len(config_text),
        message="✅ Config Updated Successfully! Version: " + str(data["version"])
    )

@app.route('/raw/config')
def raw_config():
    init_database()
    data = load_database()
    config = data.get("encrypted_config", "")
    
    if not config:
        return "No config uploaded yet", 404
    
    # Set headers for raw content
    response = app.response_class(
        response=config,
        status=200,
        mimetype='text/plain'
    )
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    return response

@app.route('/api/status')
def api_status():
    init_database()
    data = load_database()
    
    return jsonify({
        "status": "online",
        "version": data.get("version", 1),
        "last_updated": data.get("last_updated", ""),
        "total_updates": data.get("total_updates", 0),
        "config_exists": bool(data.get("encrypted_config", "")),
        "raw_link": RAW_LINK
    })

if __name__ == '__main__':
    init_database()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)