import os
import json
from flask import Flask, request, jsonify, render_template_string
from datetime import datetime
import hashlib

app = Flask(__name__)

# Configuration
DB_FILE = "config_database.json"
RAW_LINK = "https://update-config.onrender.com/raw/config"

# 🔴 AUTH KEY - Change this to your password
AUTH_KEY = "vishal80555"  # Your authentication key
AUTH_KEY_HASH = hashlib.sha256(AUTH_KEY.encode()).hexdigest()

# Initialize database
def init_database():
    if not os.path.exists(DB_FILE):
        data = {
            "encrypted_config": "",
            "version": 1,
            "last_updated": "Never",
            "total_updates": 0,
            "author": "Admin"
        }
        save_database(data)

def load_database():
    with open(DB_FILE, 'r') as f:
        return json.load(f)

def save_database(data):
    with open(DB_FILE, 'w') as f:
        json.dump(data, f, indent=4)

# Check authentication
def check_auth(auth_key):
    if not auth_key:
        return False
    return hashlib.sha256(auth_key.encode()).hexdigest() == AUTH_KEY_HASH

# Mobile-friendly HTML Template with Auth
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>🔐 Config Manager - Auth Required</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            background: linear-gradient(135deg, #1a2980 0%, #26d0ce 100%);
            min-height: 100vh;
            padding: 15px;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .container {
            width: 100%;
            max-width: 500px;
            background: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 15px 35px rgba(0,0,0,0.3);
        }
        .header {
            text-align: center;
            margin-bottom: 25px;
        }
        .header h1 {
            color: #333;
            font-size: 28px;
            margin-bottom: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 15px;
        }
        .header p {
            color: #666;
            font-size: 14px;
        }
        .card {
            background: white;
            border-radius: 15px;
            padding: 25px;
            margin-bottom: 20px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.08);
            border: 1px solid #e1e1e1;
        }
        .input-group {
            margin-bottom: 20px;
        }
        .input-label {
            display: block;
            color: #555;
            font-size: 14px;
            margin-bottom: 8px;
            font-weight: 500;
        }
        .input-field {
            width: 100%;
            padding: 15px;
            border: 2px solid #ddd;
            border-radius: 10px;
            font-size: 16px;
            transition: all 0.3s;
        }
        .input-field:focus {
            outline: none;
            border-color: #1a2980;
            box-shadow: 0 0 0 3px rgba(26, 41, 128, 0.1);
        }
        textarea.input-field {
            font-family: 'Consolas', monospace;
            resize: vertical;
            min-height: 200px;
        }
        .btn {
            background: linear-gradient(135deg, #1a2980 0%, #26d0ce 100%);
            color: white;
            border: none;
            padding: 16px;
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
            margin-top: 10px;
        }
        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 7px 20px rgba(26, 41, 128, 0.3);
        }
        .btn-secondary {
            background: #6c757d;
            margin-top: 15px;
        }
        .link-box {
            background: #f8f9fa;
            border: 2px dashed #1a2980;
            border-radius: 10px;
            padding: 15px;
            margin: 20px 0;
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
            font-size: 18px;
            font-weight: bold;
            color: #333;
        }
        .message {
            padding: 15px;
            border-radius: 10px;
            margin: 15px 0;
            text-align: center;
            display: none;
        }
        .success {
            background: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
            display: block;
        }
        .error {
            background: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
            display: block;
        }
        .auth-badge {
            position: absolute;
            top: 15px;
            right: 15px;
            background: #28a745;
            color: white;
            padding: 5px 10px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: bold;
        }
        .footer {
            text-align: center;
            margin-top: 25px;
            padding-top: 15px;
            border-top: 1px solid #eee;
            color: #888;
            font-size: 12px;
        }
        .hidden {
            display: none;
        }
        @media (max-width: 480px) {
            .container { padding: 20px; }
            .header h1 { font-size: 24px; }
            .info-grid { grid-template-columns: 1fr; }
        }
    </style>
</head>
<body>
    <div class="container">
        {% if not authenticated %}
        <!-- Login Screen -->
        <div class="header">
            <h1>🔐 Authentication Required</h1>
            <p>Enter auth key to access config manager</p>
        </div>
        
        <div class="card">
            <form action="/" method="POST">
                <div class="input-group">
                    <label class="input-label">Auth Key</label>
                    <input type="password" name="auth_key" class="input-field" placeholder="Enter auth key..." required autofocus>
                </div>
                <button type="submit" class="btn">
                    <span>🔑</span> LOGIN
                </button>
            </form>
            
            {% if error %}
            <div class="message error">
                ❌ {{ error }}
            </div>
            {% endif %}
        </div>
        
        {% else %}
        <!-- Authenticated Screen -->
        {% if show_auth_badge %}
        <div class="auth-badge">🔐 AUTHENTICATED</div>
        {% endif %}
        
        <div class="header">
            <h1>📱 Config Manager</h1>
            <p>Protected by Auth Key | Version: {{ version }}</p>
        </div>
        
        {% if message %}
        <div class="message {{ 'success' if 'Success' in message else 'error' }}">
            {{ message }}
        </div>
        {% endif %}
        
        <!-- Config Editor -->
        <div class="card">
            <div class="input-group">
                <label class="input-label">Encrypted Config</label>
                <textarea name="config" class="input-field" placeholder="Paste your encrypted config here..." id="configText">{{ current_config }}</textarea>
            </div>
            <button class="btn" onclick="updateConfig()">
                <span>💾</span> UPDATE CONFIG
            </button>
        </div>
        
        <!-- Permanent Link -->
        <div class="card">
            <h3 style="margin-bottom: 15px; color: #444;">🔗 Permanent Raw Link</h3>
            <div class="link-box">
                <input type="text" value="{{ raw_link }}" class="link-input" readonly id="rawLink">
                <p style="margin-top: 10px; text-align: center;">
                    <button onclick="copyLink()" style="background: #28a745; padding: 10px 20px; border-radius: 8px; color: white; border: none; cursor: pointer; width: 100%;">
                        📋 Copy Link to Clipboard
                    </button>
                </p>
            </div>
            <p style="color: #666; font-size: 13px; margin-top: 10px;">
                ⚡ Use this link in your app's ConfigUpdate.java file
            </p>
        </div>
        
        <!-- Current Status -->
        <div class="card">
            <h3 style="margin-bottom: 15px; color: #444;">📊 Current Status</h3>
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
                    <div class="info-label">Size</div>
                    <div class="info-value">{{ config_length }} chars</div>
                </div>
            </div>
        </div>
        
        <!-- Logout -->
        <div class="card">
            <button class="btn btn-secondary" onclick="logout()">
                <span>🚪</span> LOGOUT
            </button>
        </div>
        
        <div class="footer">
            <p>🔒 Auth Protected • ⚡ Always Online • 🔄 Update Anytime</p>
            <p style="margin-top: 5px;">Render Hosted | Mobile Optimized</p>
        </div>
        {% endif %}
    </div>
    
    <script>
    {% if authenticated %}
    // Update config via AJAX
    function updateConfig() {
        const configText = document.getElementById('configText').value;
        const authKey = '{{ auth_key }}';
        
        if (!configText.trim()) {
            showMessage('❌ Error: Config cannot be empty!', 'error');
            return;
        }
        
        const formData = new FormData();
        formData.append('config', configText);
        formData.append('auth_key', authKey);
        
        fetch('/update', {
            method: 'POST',
            body: formData
        })
        .then(response => response.text())
        .then(html => {
            // Reload page to show updated data
            location.reload();
        })
        .catch(error => {
            showMessage('❌ Update failed!', 'error');
        });
    }
    
    function copyLink() {
        const linkInput = document.getElementById('rawLink');
        linkInput.select();
        document.execCommand('copy');
        
        // Show temporary feedback
        const original = linkInput.value;
        linkInput.value = '✅ Link Copied!';
        setTimeout(() => linkInput.value = original, 1500);
    }
    
    function logout() {
        document.cookie = "auth_key=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
        location.reload();
    }
    
    function showMessage(text, type) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${type}`;
        messageDiv.textContent = text;
        messageDiv.style.display = 'block';
        
        document.querySelector('.container').insertBefore(messageDiv, document.querySelector('.card'));
        
        setTimeout(() => {
            messageDiv.remove();
        }, 5000);
    }
    
    // Auto-focus textarea
    document.addEventListener('DOMContentLoaded', function() {
        const textarea = document.getElementById('configText');
        if (textarea) {
            textarea.focus();
        }
    });
    {% endif %}
    </script>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def home():
    auth_key = request.cookies.get('auth_key') or request.form.get('auth_key')
    authenticated = check_auth(auth_key)
    
    init_database()
    data = load_database()
    
    if request.method == 'POST' and not authenticated:
        # Login attempt
        auth_key = request.form.get('auth_key', '')
        if check_auth(auth_key):
            authenticated = True
            # Set cookie for future requests
            response = app.make_response(render_template_string(HTML_TEMPLATE,
                authenticated=True,
                show_auth_badge=True,
                current_config=data.get("encrypted_config", ""),
                raw_link=RAW_LINK,
                version=data.get("version", 1),
                last_updated=data.get("last_updated", "Never"),
                total_updates=data.get("total_updates", 0),
                config_length=len(data.get("encrypted_config", "")),
                auth_key=auth_key,
                message=""
            ))
            response.set_cookie('auth_key', auth_key, max_age=86400)  # 24 hours
            return response
        else:
            return render_template_string(HTML_TEMPLATE,
                authenticated=False,
                error="❌ Invalid auth key!"
            )
    
    if authenticated:
        return render_template_string(HTML_TEMPLATE,
            authenticated=True,
            show_auth_badge=False,
            current_config=data.get("encrypted_config", ""),
            raw_link=RAW_LINK,
            version=data.get("version", 1),
            last_updated=data.get("last_updated", "Never"),
            total_updates=data.get("total_updates", 0),
            config_length=len(data.get("encrypted_config", "")),
            auth_key=auth_key,
            message=request.args.get('message', '')
        )
    else:
        return render_template_string(HTML_TEMPLATE,
            authenticated=False,
            error=request.args.get('error', '')
        )

@app.route('/update', methods=['POST'])
def update_config():
    auth_key = request.cookies.get('auth_key') or request.form.get('auth_key')
    
    if not check_auth(auth_key):
        return jsonify({"error": "Authentication required"}), 401
    
    config_text = request.form.get('config', '').strip()
    
    if not config_text:
        return jsonify({"error": "Config cannot be empty"}), 400
    
    init_database()
    data = load_database()
    
    # Update data
    data["encrypted_config"] = config_text
    data["version"] = data.get("version", 1) + 1
    data["last_updated"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data["total_updates"] = data.get("total_updates", 0) + 1
    
    save_database(data)
    
    return jsonify({
        "success": True,
        "message": f"✅ Config Updated Successfully! Version: {data['version']}",
        "version": data["version"],
        "last_updated": data["last_updated"]
    })

@app.route('/raw/config')
def raw_config():
    # 🔴 PUBLIC ACCESS - No auth required for raw config
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
    # Public API
    init_database()
    data = load_database()
    
    return jsonify({
        "status": "online",
        "version": data.get("version", 1),
        "last_updated": data.get("last_updated", ""),
        "total_updates": data.get("total_updates", 0),
        "config_exists": bool(data.get("encrypted_config", "")),
        "raw_link": RAW_LINK,
        "protected": True
    })

@app.route('/logout')
def logout():
    response = app.make_response(jsonify({"message": "Logged out"}))
    response.set_cookie('auth_key', '', expires=0)
    return response

if __name__ == '__main__':
    init_database()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
