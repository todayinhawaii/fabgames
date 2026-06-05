import os
import json
import stripe
from flask import Flask, send_from_directory, request, jsonify, redirect

app = Flask(__name__)

# Stripe config
stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')
STRIPE_PUBLISHABLE_KEY = os.environ.get('STRIPE_PUBLISHABLE_KEY')
STRIPE_PRICE_ID = os.environ.get('STRIPE_PRICE_ID')
STRIPE_WEBHOOK_SECRET = os.environ.get('STRIPE_WEBHOOK_SECRET', '')

# Supabase config
SUPABASE_URL = os.environ.get('SUPABASE_URL')
SUPABASE_ANON_KEY = os.environ.get('SUPABASE_ANON_KEY')

# ── PAGES ────────────────────────────────────────
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/about')
def about():
    return send_from_directory('.', 'about.html')

@app.route('/privacy')
def privacy():
    return send_from_directory('.', 'privacy.html')

@app.route('/terms')
def terms():
    return send_from_directory('.', 'terms.html')

@app.route('/contact')
def contact():
    return send_from_directory('.', 'contact.html')

@app.route('/join')
def join():
    return send_from_directory('.', 'join.html')

@app.route('/play')
def play():
    return send_from_directory('.', 'play.html')

@app.route('/success')
def success():
    return send_from_directory('.', 'success.html')

@app.route('/login')
def login():
    return send_from_directory('.', 'login.html')

@app.route('/reset-password')
def reset_password():
    return send_from_directory('.', 'reset_password.html')

# ── STRIPE CHECKOUT ──────────────────────────────
@app.route('/api/create-checkout', methods=['POST'])
def create_checkout():
    data = request.get_json()
    email = data.get('email', '').strip().lower()
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            mode='subscription',
            customer_email=email,
            line_items=[{'price': STRIPE_PRICE_ID, 'quantity': 1}],
            success_url='https://www.fab.games/success?session_id={CHECKOUT_SESSION_ID}',
            cancel_url='https://www.fab.games/join',
            allow_promotion_codes=True,
        )
        return jsonify({'ok': True, 'url': session.url})
    except Exception as e:
        return jsonify({'ok': False, 'msg': str(e)})

# ── STRIPE WEBHOOK ───────────────────────────────
@app.route('/api/webhook', methods=['POST'])
def webhook():
    payload = request.get_data()
    sig_header = request.headers.get('Stripe-Signature')
    try:
        if STRIPE_WEBHOOK_SECRET:
            event = stripe.Webhook.construct_event(payload, sig_header, STRIPE_WEBHOOK_SECRET)
        else:
            event = json.loads(payload)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        email = session.get('customer_email', '').lower()
        # Update user metadata in Supabase via admin API
        import urllib.request
        import urllib.parse
        try:
            # Find user by email and update their premium status
            req = urllib.request.Request(
                f"{SUPABASE_URL}/auth/v1/admin/users",
                headers={
                    'apikey': SUPABASE_ANON_KEY,
                    'Authorization': f'Bearer {os.environ.get("SUPABASE_SERVICE_KEY", SUPABASE_ANON_KEY)}',
                    'Content-Type': 'application/json'
                }
            )
        except:
            pass

    return jsonify({'ok': True})

# ── SUPABASE CONFIG FOR FRONTEND ─────────────────
@app.route('/api/config')
def config():
    return jsonify({
        'supabase_url': SUPABASE_URL,
        'supabase_anon_key': SUPABASE_ANON_KEY,
        'stripe_publishable_key': STRIPE_PUBLISHABLE_KEY,
    })

# ── STATIC FILES ─────────────────────────────────
@app.route('/<path:filename>')
def static_files(filename):
    return send_from_directory('.', filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
