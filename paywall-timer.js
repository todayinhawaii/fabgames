(function(){
  const FREE_SECONDS = 60;
  const JOIN_URL = '/join';
  let remaining = FREE_SECONDS;
  let tickHandle = null;

  function injectStyles(){
    if(document.getElementById('__pwStyles')) return;
    const style = document.createElement('style');
    style.id = '__pwStyles';
    style.textContent = `
      #__pwBadge{
        position:fixed;top:14px;right:14px;z-index:999998;
        background:rgba(5,5,8,0.88);border:1px solid rgba(201,168,76,0.5);
        color:#ffd700;font-family:Inter,Arial,sans-serif;
        padding:10px 16px;border-radius:14px;
        max-width:240px;
        box-shadow:0 4px 16px rgba(0,0,0,0.3);
        animation:__pwFadeIn 0.3s ease;
      }
      #__pwBadge .__pwBadgeMain{
        font-size:13px;font-weight:700;
        display:flex;align-items:center;gap:6px;
      }
      #__pwBadge .__pwBadgeSub{
        font-size:10.5px;font-weight:500;color:rgba(240,239,232,0.65);
        line-height:1.4;margin-top:5px;
      }
      #__pwBadge.__pwUrgent .__pwBadgeMain{
        color:#ff6b6b;
        animation:__pwPulse 1s ease infinite;
      }
      @keyframes __pwPulse{0%,100%{transform:scale(1);}50%{transform:scale(1.06);}}
      @keyframes __pwFadeIn{from{opacity:0;}to{opacity:1;}}
      #__paywallOverlay{
        position:fixed;inset:0;z-index:999999;
        background:rgba(5,5,8,0.94);
        display:flex;align-items:center;justify-content:center;
        font-family:Inter,Arial,sans-serif;
        animation:__pwFadeIn 0.4s ease;
      }
      #__paywallBox{
        max-width:420px;width:90%;background:#0d0d0f;
        border:1px solid rgba(201,168,76,0.4);border-radius:16px;
        padding:40px 32px;text-align:center;color:#f0efe8;
        box-shadow:0 0 80px rgba(201,168,76,0.15);
      }
      #__paywallBox .__pwEmoji{font-size:48px;margin-bottom:16px;}
      #__paywallBox h2{font-size:24px;font-weight:700;margin-bottom:12px;color:#ffd700;}
      #__paywallBox p{font-size:15px;color:rgba(240,239,232,0.7);line-height:1.7;margin-bottom:26px;}
      #__paywallBox button{
        display:inline-block;padding:15px 36px;border-radius:10px;
        background:linear-gradient(135deg,#ffd700,#c9a84c);color:#000;
        font-weight:700;font-size:14px;border:none;cursor:pointer;
        letter-spacing:1px;text-transform:uppercase;
        font-family:Inter,Arial,sans-serif;
      }
    `;
    document.head.appendChild(style);
  }

  function showBadge(){
    injectStyles();
    const badge = document.createElement('div');
    badge.id = '__pwBadge';
    badge.innerHTML =
      '<div class="__pwBadgeMain">⏱ <span id="__pwBadgeText">Free preview: '+remaining+'s</span></div>' +
      '<div class="__pwBadgeSub">Don\u2019t worry — become a member to keep playing this game (and every game!) forever 💛</div>';
    document.body.appendChild(badge);
  }

  function updateBadge(){
    const el = document.getElementById('__pwBadgeText');
    if(el) el.textContent = 'Free preview: '+remaining+'s';
    const badge = document.getElementById('__pwBadge');
    if(badge) badge.classList.toggle('__pwUrgent', remaining<=10);
  }

  function showPaywallOverlay(){
    if(document.getElementById('__paywallOverlay')) return;
    const badge = document.getElementById('__pwBadge');
    if(badge) badge.remove();
    injectStyles();

    const overlay = document.createElement('div');
    overlay.id = '__paywallOverlay';
    overlay.innerHTML =
      '<div id="__paywallBox">' +
        '<div class="__pwEmoji">🎮</div>' +
        '<h2>Time is up!</h2>' +
        '<p>Loving it so far? Sign up free to keep playing this game and unlock every game on fab.games — no credit card needed for your first 30 days.</p>' +
        '<button id="__pwSignupBtn" type="button">Sign Up Free →</button>' +
      '</div>';
    document.body.appendChild(overlay);

    // Many games attach their own aggressive document-level touch/click
    // handlers to control gameplay. Block ALL of them from ever seeing
    // interactions with our overlay, in both the capture and bubble
    // phases, then force navigation ourselves rather than trusting a
    // plain link's default behavior (which some games' preventDefault()
    // calls can silently swallow on touch devices).
    const blockEvents = ['click','mousedown','mouseup','touchstart','touchend','touchmove','pointerdown','pointerup'];
    blockEvents.forEach(function(evt){
      overlay.addEventListener(evt, function(e){ e.stopPropagation(); }, true);
      overlay.addEventListener(evt, function(e){ e.stopPropagation(); }, false);
    });

    const goToJoin = function(e){
      e.preventDefault();
      e.stopPropagation();
      window.location.href = JOIN_URL;
    };
    const btn = document.getElementById('__pwSignupBtn');
    btn.addEventListener('click', goToJoin, true);
    btn.addEventListener('touchend', goToJoin, true);
  }

  function startCountdown(){
    showBadge();
    tickHandle = setInterval(function(){
      remaining--;
      if(remaining <= 0){
        clearInterval(tickHandle);
        showPaywallOverlay();
      } else {
        updateBadge();
      }
    }, 1000);
  }

  async function checkAndStartTimer(){
    try{
      const cfgRes = await fetch('/api/config');
      const cfg = await cfgRes.json();
      const sb = window.supabase.createClient(cfg.supabase_url, cfg.supabase_anon_key);
      const {data:{session}} = await sb.auth.getSession();

      if(session){
        const planRes = await fetch('/api/get-plan?email='+encodeURIComponent(session.user.email));
        const planData = await planRes.json();
        if(planData.ok){
          const now = new Date();
          const isMember = planData.subscription_status==='active' ||
                           planData.plan==='free_trial' ||
                           (planData.trial_end && new Date(planData.trial_end) > now);
          if(isMember) return; // real member — play forever, no timer at all
        }
      }
    }catch(e){
      console.log('Paywall check error:', e.message||e);
      // If the check itself fails for some reason, fail SAFE by still
      // applying the timer rather than accidentally granting free
      // unlimited access to everyone if something's misconfigured.
    }

    // Not a member (or check failed). Before starting a fresh countdown,
    // check whether this browser has already used its free preview for
    // THIS game recently — otherwise someone could just hit refresh
    // endlessly for unlimited free 60-second chunks. This is a soft
    // deterrent (clearing browser data or using incognito still bypasses
    // it), not a hard security wall — but it stops the easy, casual case.
    const storageKey = 'pw_trial_' + location.pathname;
    const lastTrial = localStorage.getItem(storageKey);
    const oneDayMs = 24*60*60*1000;
    if(lastTrial && (Date.now() - parseInt(lastTrial,10)) < oneDayMs){
      showPaywallOverlay(); // already used today's preview — straight to sign-up prompt
      return;
    }
    localStorage.setItem(storageKey, Date.now().toString());

    // Start the visible free trial countdown
    startCountdown();
  }

  function loadSupabaseThen(cb){
    if(window.supabase){ cb(); return; }
    const s = document.createElement('script');
    s.src = 'https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2/dist/umd/supabase.js';
    s.onload = cb;
    s.onerror = function(){
      console.log('Paywall: failed to load Supabase, applying timer as a safe default');
      startCountdown();
    };
    document.head.appendChild(s);
  }

  function start(){ loadSupabaseThen(checkAndStartTimer); }

  if(document.readyState==='loading'){
    document.addEventListener('DOMContentLoaded', start);
  } else {
    start();
  }
})();
