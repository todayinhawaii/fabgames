(function(){
  function injectStyles(){
    if(document.getElementById('__mgStyles')) return;
    const style = document.createElement('style');
    style.id = '__mgStyles';
    style.textContent = `
      #__moreGamesBtn{
        position:fixed;top:14px;left:14px;z-index:999997;
        background:rgba(5,5,8,0.82);border:1px solid rgba(201,168,76,0.5);
        color:#ffd700;font-family:Inter,Arial,sans-serif;font-size:13px;
        font-weight:700;padding:9px 18px;border-radius:20px;
        text-decoration:none;display:inline-flex;align-items:center;gap:6px;
        box-shadow:0 4px 16px rgba(0,0,0,0.3);
        cursor:pointer;user-select:none;
        transition:transform 0.15s, background 0.15s;
      }
      #__moreGamesBtn:hover{background:rgba(30,20,5,0.92);transform:translateY(-1px);}
    `;
    document.head.appendChild(style);
  }

  function addButton(){
    injectStyles();
    const btn = document.createElement('div');
    btn.id = '__moreGamesBtn';
    btn.innerHTML = '← More Games';

    // Same lesson learned from the paywall overlay button: many games
    // attach their own aggressive document-level touch/click handlers.
    // Force navigation ourselves rather than trusting default link
    // behavior, which those handlers can silently swallow.
    const goToPlay = function(e){
      e.preventDefault();
      e.stopPropagation();
      window.location.href = '/play';
    };
    btn.addEventListener('click', goToPlay, true);
    btn.addEventListener('touchend', goToPlay, true);

    document.body.appendChild(btn);
  }

  if(document.readyState==='loading'){
    document.addEventListener('DOMContentLoaded', addButton);
  } else {
    addButton();
  }
})();
