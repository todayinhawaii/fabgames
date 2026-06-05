import os
import json
import stripe
from flask import Flask, send_from_directory, request, jsonify, redirect

app = Flask(__name__)

# Stripe config from environment variables
stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')
STRIPE_PUBLISHABLE_KEY = os.environ.get('STRIPE_PUBLISHABLE_KEY')
STRIPE_PRICE_ID = os.environ.get('STRIPE_PRICE_ID')
STRIPE_WEBHOOK_SECRET = os.environ.get('STRIPE_WEBHOOK_SECRET', '')

# Simple JSON file storage for members
MEMBERS_FILE = 'members.json'

def load_members():
    try:
        with open(MEMBERS_FILE) as f:
            return json.load(f)
    except:
        return {}

def save_members(members):
    with open(MEMBERS_FILE, 'w') as f:
        json.dump(members, f)

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

# ── FREE TRIAL SIGNUP ────────────────────────────
@app.route('/api/free-trial', methods=['POST'])
def free_trial():
    data = request.get_json()
    email = data.get('email', '').strip().lower()
    name  = data.get('name', '').strip()

    if not email or '@' not in email:
        return jsonify({'ok': False, 'msg': 'Please enter a valid email!'})

    members = load_members()

    if email in members:
        m = members[email]
        if m.get('status') in ['trial', 'active']:
            return jsonify({'ok': True, 'existing': True, 'msg': 'Welcome back!'})

    import datetime
    now = datetime.datetime.utcnow()
    trial_end = now + datetime.timedelta(days=30)

    members[email] = {
        'name': name,
        'email': email,
        'status': 'trial',
        'joined': now.isoformat(),
        'trial_end': trial_end.isoformat(),
    }
    save_members(members)

    return jsonify({'ok': True, 'msg': 'Welcome to fab.games! Enjoy your free month!'})

# ── CHECK ACCESS ─────────────────────────────────
@app.route('/api/check-access', methods=['POST'])
def check_access():
    data = request.get_json()
    email = data.get('email', '').strip().lower()

    members = load_members()
    if email not in members:
        return jsonify({'access': False})

    import datetime
    m = members[email]

    if m.get('status') == 'active':
        return jsonify({'access': True, 'status': 'premium', 'name': m.get('name')})

    if m.get('status') == 'trial':
        trial_end = datetime.datetime.fromisoformat(m['trial_end'])
        if datetime.datetime.utcnow() < trial_end:
            days_left = (trial_end - datetime.datetime.utcnow()).days
            return jsonify({'access': True, 'status': 'trial',
                          'days_left': days_left, 'name': m.get('name')})
        else:
            return jsonify({'access': False, 'status': 'expired'})

    return jsonify({'access': False})

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
            line_items=[{
                'price': STRIPE_PRICE_ID,
                'quantity': 1,
            }],
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
            event = stripe.Webhook.construct_event(
                payload, sig_header, STRIPE_WEBHOOK_SECRET)
        else:
            event = json.loads(payload)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        email = session.get('customer_email', '').lower()
        members = load_members()
        if email in members:
            members[email]['status'] = 'active'
            members[email]['stripe_customer'] = session.get('customer')
        else:
            members[email] = {
                'email': email,
                'status': 'active',
                'stripe_customer': session.get('customer'),
            }
        save_members(members)

    elif event['type'] == 'customer.subscription.deleted':
        sub = event['data']['object']
        customer_id = sub.get('customer')
        members = load_members()
        for email, m in members.items():
            if m.get('stripe_customer') == customer_id:
                members[email]['status'] = 'cancelled'
                break
        save_members(members)

    return jsonify({'ok': True})

# ── STATIC FILES ─────────────────────────────────
@app.route('/game_<name>.jpg')
def game_card_jpg(name):
    f = f'game_{name}.jpg'
    if os.path.exists(f):
        return send_from_directory('.', f)
    return '', 404

@app.route('/game_<name>.mp4')
def game_card_mp4(name):
    f = f'game_{name}.mp4'
    if os.path.exists(f):
        return send_from_directory('.', f, mimetype='video/mp4')
    return '', 404

@app.route('/<path:filename>')
def static_files(filename):
    return send_from_directory('.', filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
