import os
import json
import stripe
import urllib.request
import urllib.parse
from datetime import datetime, timedelta
from flask import Flask, send_from_directory, request, jsonify

app = Flask(__name__)

# Stripe config
stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')
STRIPE_PUBLISHABLE_KEY = os.environ.get('STRIPE_PUBLISHABLE_KEY')
STRIPE_PRICE_ID = os.environ.get('STRIPE_PRICE_ID')
STRIPE_WEBHOOK_SECRET = os.environ.get('STRIPE_WEBHOOK_SECRET', '')

# Supabase config
SUPABASE_URL = os.environ.get('SUPABASE_URL')
SUPABASE_ANON_KEY = os.environ.get('SUPABASE_ANON_KEY')
SUPABASE_SERVICE_KEY = os.environ.get('SUPABASE_SERVICE_KEY')

def supabase_request(method, path, data=None, use_service_key=False):
    """Make a request to Supabase REST API"""
    url = f"{SUPABASE_URL}/rest/v1/{path}"
    key = SUPABASE_SERVICE_KEY if use_service_key else SUPABASE_ANON_KEY
    headers = {
        'apikey': key,
        'Authorization': f'Bearer {key}',
        'Content-Type': 'application/json',
        'Prefer': 'return=representation'
    }
    body = json.dumps(data).encode() if data else None
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req) as res:
            return json.loads(res.read().decode())
    except urllib.error.HTTPError as e:
        print(f"Supabase error: {e.read().decode()}")
        return None

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

@app.route('/veggies')
def veggies():
    return send_from_directory('.', 'veggies.html')

@app.route('/pinball')
def pinball():
    return send_from_directory('.', 'pinball.html')

@app.route('/games.js')
def games_js():
    return send_from_directory('.', 'games.js', mimetype='application/javascript')

@app.route('/artlab')
def artlab():
    return send_from_directory('.', 'artlab_v2.html')

@app.route('/reset-password')
def reset_password():
    return send_from_directory('.', 'reset_password.html')

# ── CONFIG FOR FRONTEND ──────────────────────────
@app.route('/api/config')
def config():
    return jsonify({
        'supabase_url': SUPABASE_URL,
        'supabase_anon_key': SUPABASE_ANON_KEY,
        'stripe_publishable_key': STRIPE_PUBLISHABLE_KEY,
    })

# ── FREE TRIAL SIGNUP ────────────────────────────
@app.route('/api/free-trial', methods=['POST'])
def free_trial():
    data = request.get_json()
    email = data.get('email', '').strip().lower()
    name  = data.get('name', '').strip()

    if not email or '@' not in email:
        return jsonify({'ok': False, 'msg': 'Please enter a valid email!'})

    trial_end = (datetime.utcnow() + timedelta(days=30)).isoformat()

    # Check if member already exists
    existing = supabase_request('GET',
        f"members?email=eq.{urllib.parse.quote(email)}&select=*",
        use_service_key=True)

    if existing and len(existing) > 0:
        m = existing[0]
        if m.get('status') in ['trial', 'active']:
            return jsonify({'ok': True, 'existing': True, 'msg': 'Welcome back!!'})

    # Insert new member
    result = supabase_request('POST', 'members', {
        'email': email,
        'name': name,
        'status': 'trial',
        'trial_end': trial_end
    }, use_service_key=True)

    if result is None:
        # Try upsert
        supabase_request('PATCH',
            f"members?email=eq.{urllib.parse.quote(email)}",
            {'status': 'trial', 'trial_end': trial_end, 'name': name},
            use_service_key=True)

    return jsonify({'ok': True, 'msg': 'Welcome to fab.games! Enjoy your free month!!'})

# ── PWA FILES ────────────────────────────────────
@app.route('/manifest.json')
def manifest():
    return send_from_directory('.', 'manifest.json',
        mimetype='application/manifest+json')

@app.route('/service-worker.js')
def service_worker():
    response = send_from_directory('.', 'service-worker.js',
        mimetype='application/javascript')
    response.headers['Service-Worker-Allowed'] = '/'
    response.headers['Cache-Control'] = 'no-cache'
    return response

@app.route('/icon-192.png')
def icon192():
    return send_from_directory('.', 'icon-192.png', mimetype='image/png')

@app.route('/icon-512.png')
def icon512():
    return send_from_directory('.', 'icon-512.png', mimetype='image/png')

# ── CHECK MEMBER ─────────────────────────────────
@app.route('/api/check-member', methods=['POST'])
def check_member():
    data = request.get_json()
    email = data.get('email', '').strip().lower()
    members = supabase_request('GET',
        f"members?email=eq.{urllib.parse.quote(email)}&select=*",
        use_service_key=True)
    if not members or len(members) == 0:
        return jsonify({'exists': False, 'status': 'none'})
    return jsonify({'exists': True, 'status': members[0].get('status','trial')})

# ── CHECK ACCESS ─────────────────────────────────
@app.route('/api/check-access', methods=['POST'])
def check_access():
    data = request.get_json()
    email = data.get('email', '').strip().lower()

    members = supabase_request('GET',
        f"members?email=eq.{urllib.parse.quote(email)}&select=*",
        use_service_key=True)

    if not members or len(members) == 0:
        return jsonify({'access': False})

    m = members[0]
    if m.get('status') == 'active':
        return jsonify({'access': True, 'status': 'premium', 'name': m.get('name')})

    if m.get('status') == 'trial':
        trial_end = datetime.fromisoformat(m['trial_end'].replace('Z',''))
        if datetime.utcnow() < trial_end:
            days_left = (trial_end - datetime.utcnow()).days
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
        customer_id = session.get('customer')

        # Update or insert member as active
        existing = supabase_request('GET',
            f"members?email=eq.{urllib.parse.quote(email)}&select=*",
            use_service_key=True)

        if existing and len(existing) > 0:
            supabase_request('PATCH',
                f"members?email=eq.{urllib.parse.quote(email)}",
                {'status': 'active', 'stripe_customer': customer_id},
                use_service_key=True)
        else:
            supabase_request('POST', 'members', {
                'email': email,
                'status': 'active',
                'stripe_customer': customer_id
            }, use_service_key=True)

    elif event['type'] == 'customer.subscription.deleted':
        sub = event['data']['object']
        customer_id = sub.get('customer')
        supabase_request('PATCH',
            f"members?stripe_customer=eq.{customer_id}",
            {'status': 'cancelled'},
            use_service_key=True)

    return jsonify({'ok': True})

# ── STATIC FILES ─────────────────────────────────

# ── HULA/MEMORY SCORES ──────────────────────────
@app.route('/api/hula-scores', methods=['GET','POST'])
def hula_scores():
    if request.method=='POST':
        data = request.get_json() or {}
        try:
            supabase_request('POST','hula_scores',{
                'name':data.get('name','')[:30],
                'score':int(data.get('score',0)),
                'island':data.get('island','')[:40],
                'time_str':data.get('timeStr',''),
                'time_secs':int(data.get('timeSecs',0)),
            }, use_service_key=True)
            return jsonify({'ok':True})
        except Exception as e:
            return jsonify({'ok':False,'error':str(e)})
    else:
        try:
            res = supabase_request('GET','hula_scores?select=*&order=score.desc&limit=10')
            return jsonify(res if isinstance(res,list) else [])
        except:
            return jsonify([])

# ── WORDSEARCH SCORES ────────────────────────────
@app.route('/api/wordsearch-scores', methods=['GET','POST'])
def wordsearch_scores():
    if request.method=='POST':
        data = request.get_json() or {}
        try:
            supabase_request('POST','wordsearch_scores',{
                'name':data.get('name','')[:30],
                'score':int(data.get('score',0)),
                'island':data.get('island','')[:40],
                'puzzles':int(data.get('puzzles',0)),
            }, use_service_key=True)
            return jsonify({'ok':True})
        except Exception as e:
            return jsonify({'ok':False,'error':str(e)})
    else:
        try:
            res = supabase_request('GET','wordsearch_scores?select=*&order=score.desc&limit=10')
            return jsonify(res if isinstance(res,list) else [])
        except:
            return jsonify([])

# ── CAPITAL CITY CHALLENGE ──────────────────────
@app.route('/capitals')
def capitals():
    return send_from_directory('.', 'capitals.html')

@app.route('/<path:filename>')
def static_files(filename):
    return send_from_directory('.', filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)

# ── MIGRATED GAMES FROM TODAYINHAWAII ──────────────

@app.route('/dolphins')
def dolphins():
    return send_from_directory('.', 'dolphin.html')

@app.route('/peles-fury')
def peles_fury():
    return send_from_directory('.', 'lava.html')

@app.route('/turtle-checkers')
def turtle_checkers():
    return send_from_directory('.', 'turtles.html')

@app.route('/mermaid-chess')
def mermaid_chess():
    return send_from_directory('.', 'chess.html')

@app.route('/trivia')
def trivia():
    return send_from_directory('.', 'trivia.html')

@app.route('/word-search')
def word_search():
    return send_from_directory('.', 'wordsearch.html')

@app.route('/balloons')
def balloons():
    return send_from_directory('.', 'balloons.html')

@app.route('/fortune')
def fortune():
    return send_from_directory('.', 'fortune.html')

@app.route('/slime')
def slime():
    return send_from_directory('.', 'slime.html')

@app.route('/film-lab')
def film_lab():
    return send_from_directory('.', 'camera.html')

@app.route('/memory')
def memory():
    return send_from_directory('.', 'hulaCrush.html')

@app.route('/aloha-letters')
def aloha_letters():
    return send_from_directory('.', 'scrabble.html')

@app.route('/who-are-you')
def who_are_you():
    return send_from_directory('.', 'humor.html')
