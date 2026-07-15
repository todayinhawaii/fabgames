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
SUPABASE_URL = os.environ.get('SUPABASE_URL') or 'https://xbzeakoypdyslnnriaef.supabase.co'
SUPABASE_ANON_KEY = os.environ.get('SUPABASE_ANON_KEY') or 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InhiemVha295cGR5c2xubnJpYWVmIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODA2NDI5MzIsImV4cCI6MjA5NjIxODkzMn0.-pS2FE-Q-_EetM5ONbJycZWFm336wJ-z4MTOGCdA1LE'
SUPABASE_SERVICE_KEY = os.environ.get('SUPABASE_SERVICE_KEY')
print(f"SUPABASE_URL: {SUPABASE_URL}", flush=True)
print(f"SUPABASE_SERVICE_KEY set: {bool(SUPABASE_SERVICE_KEY)}", flush=True)
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

def serve_game(filename):
    """Serve a game HTML file with two shared scripts injected automatically:
    the 60-second free-preview paywall timer, and the always-visible
    'More Games' back-button. Individual game files never need to be
    edited by hand — both live in one shared file each and get added to
    every game as it's served."""
    try:
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)
        with open(path, 'r', encoding='utf-8') as f:
            html = f.read()
        snippets = [
            '<script src="/paywall-timer.js"></script>',
            '<script src="/more-games-button.js"></script>',
        ]
        for snippet in snippets:
            if snippet not in html:
                if '</body>' in html:
                    html = html.replace('</body>', snippet + '\n</body>')
                else:
                    html += snippet
        return html, 200, {'Content-Type': 'text/html; charset=utf-8'}
    except Exception as e:
        print(f'serve_game error for {filename}: {e}', flush=True)
        return send_from_directory('.', filename)

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
@app.route('/account')
def account():
    return send_from_directory('.', 'fab_account.html')
@app.route('/veggies')
def veggies():
    return serve_game('veggies.html')
@app.route('/pinball')
def pinball():
    return serve_game('pinball.html')
@app.route('/games.js')
def games_js():
    return send_from_directory('.', 'games.js', mimetype='application/javascript')
@app.route('/artlab')
def artlab():
    return serve_game('artlab_v2.html')
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

# ── GET PLAN (used to decide whether to show the bundle cross-site button) ──
@app.route('/api/get-plan')
def get_plan():
    email = request.args.get('email', '').strip().lower()
    if not email:
        return jsonify({'ok': False, 'error': 'Missing email'})
    members = supabase_request('GET',
        f"members?email=eq.{urllib.parse.quote(email)}&select=plan,status,subscription_status",
        use_service_key=True)
    if not members or len(members) == 0:
        return jsonify({'ok': False, 'error': 'No member found'})
    return jsonify({
        'ok': True,
        'plan': members[0].get('plan'),
        'status': members[0].get('status'),
        'subscription_status': members[0].get('subscription_status'),
    })
# ── FREE TRIAL SIGNUP ────────────────────────────
@app.route('/api/free-trial', methods=['POST'])
def free_trial():
    data = request.get_json()
    email    = data.get('email', '').strip().lower()
    name     = data.get('name', '').strip()
    password = data.get('password', '').strip()
    plan     = data.get('plan', 'fab')
    if not email or '@' not in email:
        return jsonify({'ok': False, 'msg': 'Please enter a valid email!'})
    trial_end = (datetime.utcnow() + timedelta(days=30)).isoformat()

    # Step 1: Create Supabase Auth user via Admin API
    if password:
        try:
            auth_url = f"{SUPABASE_URL}/auth/v1/admin/users"
            auth_headers = {
                'apikey': SUPABASE_SERVICE_KEY,
                'Authorization': f'Bearer {SUPABASE_SERVICE_KEY}',
                'Content-Type': 'application/json'
            }
            auth_body = json.dumps({
                'email': email,
                'password': password,
                'email_confirm': True,
                'user_metadata': {'name': name, 'plan': plan}
            }).encode()
            req = urllib.request.Request(auth_url, data=auth_body, headers=auth_headers, method='POST')
            try:
                with urllib.request.urlopen(req) as res:
                    auth_result = json.loads(res.read().decode())
                    print(f"Auth user created: {email}", flush=True)
            except urllib.error.HTTPError as e:
                err = e.read().decode()
                print(f"Auth error: {err}", flush=True)
                if 'already registered' in err or 'already been registered' in err:
                    # This email already has an account. Do NOT silently overwrite
                    # its password (that would let anyone hijack any email just by
                    # typing it into the signup form) — stop here and tell them
                    # clearly, BEFORE any payment is taken.
                    return jsonify({
                        'ok': False,
                        'msg': 'This email is already registered. Please sign in instead, or use "Forgot Password" if you don\'t remember your login.',
                        'already_registered': True
                    })
        except Exception as e:
            print(f"Auth exception: {e}", flush=True)

    # Step 2: Check if member already exists
    existing = supabase_request('GET',
        f"members?email=eq.{urllib.parse.quote(email)}&select=*",
        use_service_key=True)
    if existing and len(existing) > 0:
        m = existing[0]
        if m.get('status') in ['trial', 'active']:
            return jsonify({'ok': True, 'existing': True, 'msg': 'Welcome back!!'})

    # Step 3: Insert new member
    result = supabase_request('POST', 'members', {
        'email': email,
        'name': name,
        'status': 'trial',
        'trial_end': trial_end,
        'plan': plan
    }, use_service_key=True)
    if result is None:
        supabase_request('PATCH',
            f"members?email=eq.{urllib.parse.quote(email)}",
            {'status': 'trial', 'trial_end': trial_end, 'name': name, 'plan': plan},
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
    name  = data.get('name', '').strip()
    plan  = data.get('plan', 'fab')
    # Use passed price_id if provided, otherwise fall back to env
    price_id = data.get('price_id') or STRIPE_PRICE_ID
    try:
        # Build metadata so webhook knows which plan was purchased
        metadata = {'plan': plan, 'name': name}
        origin = request.headers.get('Origin') or request.headers.get('Referer') or 'https://www.fab.games'
        origin = origin.rstrip('/').split('/join')[0]  # strip any path, keep just the domain
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            mode='subscription',
            customer_email=email,
            line_items=[{'price': price_id, 'quantity': 1}],
            subscription_data={
                'trial_period_days': 30,
                'metadata': metadata,
            },
            success_url=origin+'/success?session_id={CHECKOUT_SESSION_ID}&plan='+plan,
            cancel_url=origin+'/join',
            allow_promotion_codes=True,
            metadata=metadata,
        )
        return jsonify({'ok': True, 'url': session.url})
    except Exception as e:
        print(f'CHECKOUT ERROR: {e}', flush=True)
        return jsonify({'ok': False, 'msg': str(e)})
# ── STRIPE BILLING PORTAL ─────────────────────────
@app.route('/api/create-portal-session', methods=['POST'])
def create_portal_session():
    data = request.get_json()
    email = data.get('email', '').strip().lower()
    try:
        members = supabase_request('GET',
            f"members?email=eq.{urllib.parse.quote(email)}&select=stripe_customer",
            use_service_key=True)
        if not members or not members[0].get('stripe_customer'):
            return jsonify({'ok': False, 'error': 'No subscription found for this account.'})
        customer_id = members[0]['stripe_customer']
        session = stripe.billing_portal.Session.create(
            customer=customer_id,
            return_url='https://www.fab.games/account',
        )
        return jsonify({'ok': True, 'url': session.url})
    except Exception as e:
        print(f'PORTAL ERROR: {e}', flush=True)
        return jsonify({'ok': False, 'error': str(e)})

# ── CANCEL SUBSCRIPTION (direct, no portal redirect needed) ──
@app.route('/api/cancel-subscription', methods=['POST'])
def cancel_subscription():
    data = request.get_json()
    email = data.get('email', '').strip().lower()
    try:
        members = supabase_request('GET',
            f"members?email=eq.{urllib.parse.quote(email)}&select=stripe_customer",
            use_service_key=True)
        if not members or not members[0].get('stripe_customer'):
            return jsonify({'ok': False, 'error': 'No active subscription found for this account.'})
        customer_id = members[0]['stripe_customer']

        subs = stripe.Subscription.list(customer=customer_id, status='active', limit=1)
        if not subs.data:
            subs = stripe.Subscription.list(customer=customer_id, status='trialing', limit=1)
        if not subs.data:
            return jsonify({'ok': False, 'error': 'No active subscription found for this account.'})

        sub = subs.data[0]
        updated = stripe.Subscription.modify(sub.id, cancel_at_period_end=True)

        supabase_request('PATCH',
            f"members?email=eq.{urllib.parse.quote(email)}",
            {'subscription_status': 'cancel_at_period_end'},
            use_service_key=True)

        return jsonify({
            'ok': True,
            'cancel_at': updated.current_period_end,  # unix timestamp
        })
    except Exception as e:
        print(f'CANCEL ERROR: {e}', flush=True)
        return jsonify({'ok': False, 'error': str(e)})
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
        metadata = session.get('metadata', {})
        plan = metadata.get('plan', 'fab')
        name = metadata.get('name', '')
        # Update or insert member as active with plan info
        existing = supabase_request('GET',
            f"members?email=eq.{urllib.parse.quote(email)}&select=*",
            use_service_key=True)
        patch = {
            'status': 'active',
            'stripe_customer': customer_id,
            'plan': plan,
        }
        if name:
            patch['name'] = name
        if existing and len(existing) > 0:
            supabase_request('PATCH',
                f"members?email=eq.{urllib.parse.quote(email)}",
                patch,
                use_service_key=True)
        else:
            patch['email'] = email
            supabase_request('POST', 'members', patch, use_service_key=True)
        print(f'MEMBER ACTIVATED: {email} plan={plan}', flush=True)
    elif event['type'] == 'customer.subscription.updated':
        sub = event['data']['object']
        customer_id = sub.get('customer')
        cancel_at_period_end = sub.get('cancel_at_period_end', False)
        if cancel_at_period_end:
            # Get period end date for trial_end display
            period_end = sub.get('current_period_end')
            patch = {'status': 'cancel_at_period_end'}
            if period_end:
                patch['trial_end'] = datetime.utcfromtimestamp(period_end).isoformat()
            supabase_request('PATCH',
                f"members?stripe_customer=eq.{customer_id}",
                patch,
                use_service_key=True)
        else:
            # Resumed - back to active
            supabase_request('PATCH',
                f"members?stripe_customer=eq.{customer_id}",
                {'status': 'active'},
                use_service_key=True)
    elif event['type'] == 'customer.subscription.deleted':
        sub = event['data']['object']
        customer_id = sub.get('customer')
        supabase_request('PATCH',
            f"members?stripe_customer=eq.{customer_id}",
            {'status': 'cancelled'},
            use_service_key=True)
    elif event['type'] == 'invoice.payment_failed':
        # A renewal charge failed (expired card, insufficient funds, etc).
        # Mark the account as past_due so access checks correctly deny
        # them, instead of letting them keep playing for free forever
        # after Stripe has already given up trying to charge them.
        invoice = event['data']['object']
        customer_id = invoice.get('customer')
        if customer_id:
            supabase_request('PATCH',
                f"members?stripe_customer=eq.{customer_id}",
                {'status': 'past_due', 'subscription_status': 'past_due'},
                use_service_key=True)
            print(f'PAYMENT FAILED: customer={customer_id} marked past_due', flush=True)
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
    return serve_game('capitals.html')
# ── JIGSAW PUZZLE GALLERY ────────────────────────
@app.route('/jigsaw')
def jigsaw():
    return serve_game('jigsaw.html')
@app.route('/<path:filename>')
def static_files(filename):
    # Universal safety net: ANY .html file request that isn't one of the
    # known utility/account pages automatically gets the free-preview
    # timer injected — even if a future game's route is added without
    # remembering to use serve_game() directly. Non-game utility pages
    # (login, join, account, etc.) are explicitly excluded since they
    # already have their own dedicated routes above, but this catches
    # them too just in case, so they're never accidentally timer-gated.
    NON_GAME_PAGES = {
        'index.html','join.html','play.html','success.html','login.html',
        'account.html','fab_account.html','reset_password.html','reset-password.html',
        'about.html','privacy.html','terms.html','contact.html',
    }

    base_dir = os.path.dirname(os.path.abspath(__file__))
    exact_path = os.path.join(base_dir, filename)

    # If the exact file exists (games.js, images, css, an explicit .html
    # request, etc.) serve it the normal way — or with the timer if it's
    # an un-excluded .html file.
    if os.path.isfile(exact_path):
        if filename.endswith('.html') and filename not in NON_GAME_PAGES:
            return serve_game(filename)
        return send_from_directory('.', filename)

    # Otherwise, try it as a clean-URL game: does "<name>.html" exist?
    # This means a BRAND NEW game needs NO route added here at all —
    # just add its entry to games.js (with href:'/new-game') and upload
    # new-game.html, and it works immediately, timer included.
    html_guess = filename + '.html'
    if html_guess not in NON_GAME_PAGES and os.path.isfile(os.path.join(base_dir, html_guess)):
        return serve_game(html_guess)

    return send_from_directory('.', filename)  # will 404 naturally if truly missing

@app.route('/donut')
def donut():
    return serve_game('donut.html')


@app.route('/blob')
def blob():
    return serve_game('blob.html')

@app.route('/spinme')
def spinme():
    return serve_game('spinme.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
# ── MIGRATED GAMES FROM TODAYINHAWAII ──────────────
@app.route('/dolphins')
def dolphins():
    return serve_game('dolphin.html')
@app.route('/peles-fury')
def peles_fury():
    return serve_game('lava.html')
@app.route('/turtle-checkers')
def turtle_checkers():
    return serve_game('turtles.html')
@app.route('/mermaid-chess')
def mermaid_chess():
    return serve_game('chess.html')
@app.route('/trivia')
def trivia():
    return serve_game('trivia.html')
@app.route('/word-search')
def word_search():
    return serve_game('wordsearch.html')
@app.route('/balloons')
def balloons():
    return serve_game('balloons.html')
@app.route('/fortune')
def fortune():
    return serve_game('fortune.html')
@app.route('/slime')
def slime():
    return serve_game('slime.html')
@app.route('/film-lab')
def film_lab():
    return serve_game('camera.html')
@app.route('/memory')
def memory():
    return serve_game('hulaCrush.html')
@app.route('/aloha-letters')
def aloha_letters():
    return serve_game('scrabble.html')
@app.route('/who-are-you')
def who_are_you():
    return serve_game('humor.html')

@app.route('/trash')
def trash():
    return serve_game('trash.html')

@app.route('/coloring')
def coloring():
    return serve_game('coloring_book.html')


@app.route('/learn-the-body')
def learn_the_body():
    return serve_game('learn_the_body.html')

@app.route('/happy-buttons')
def happy_buttons():
    return serve_game('happy_buttons.html')

@app.route('/happy-buttons-2')
def happy_buttons_2():
    return serve_game('happy-buttons-2.html')

@app.route('/happy-buttons-3')
def happy_buttons_3():
    return serve_game('happy-buttons-3.html')

@app.route('/happy-buttons-4')
def happy_buttons_4():
    return serve_game('happy-buttons-4.html')

@app.route('/happy-buttons-5')
def happy_buttons_5():
    return serve_game('happy-buttons-5.html')

@app.route('/happy-buttons-6')
def happy_buttons_6():
    return serve_game('happy-buttons-6.html')


@app.route('/fun-with-numbers')
def fun_with_numbers():
    return serve_game('fun-with-numbers.html')

@app.route('/fun-with-shapes')
def fun_with_shapes():
    return serve_game('fun-with-shapes.html')

@app.route('/magic-sound-keys')
def magic_sound_keys():
    return serve_game('magic-sound-keys.html')

@app.route('/street-hustler')
def street_hustler():
    return serve_game('street-hustler.html')

@app.route('/mystery-phrase')
def mystery_phrase():
    return serve_game('mystery-phrase.html')

@app.route('/tic-tac-toe')
def tic_tac_toe():
    return serve_game('tic-tac-toe.html')

@app.route('/galaxy-explorer')
def galaxy_explorer():
    return serve_game('galaxy-explorer.html')

@app.route('/fab-house')
def fab_house():
    return serve_game('fab-house.html')

@app.route('/crossword')
def crossword():
    return serve_game('crossword.html')

@app.route('/grandmas-cupboard')
def grandmas_cupboard():
    return serve_game('grandmas-cupboard.html')

@app.route('/henry')
def henry():
    return serve_game('henry.html')

@app.route('/animal-discovery')
def animal_discovery():
    return serve_game('animal-discovery.html')

@app.route('/strawberry-farm')
def strawberry_farm():
    return serve_game('strawberry-farm.html')

@app.route('/spelling-game')
def spelling_game():
    return serve_game('spelling-game.html')

@app.route('/teapot-guineapigs')
def teapot_guineapigs():
    return serve_game('teapot-guineapigs.html')

@app.route('/freegames')
def freegames():
    return send_from_directory('.', 'freegames.html')
