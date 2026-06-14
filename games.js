// ── MASTER GAMES LIST ─────────────────────────────────────────
// Edit this ONE file to add/remove games from BOTH the home page and play page!!
// Both index.html and play.html load this file via <script src="/games.js"></script>

const GAMES=[
  {emoji:'🎨',cat:'Art & Creativity',title:'Art Lab',
   desc:'Professional drawing app. Pencils, watercolour, oil paint, layers and more. Create and share your art.',
   href:'/artlab',color:'rgba(155,89,182,0.12)',neon:'#ffd700',neonbg:'rgba(255,215,0,0.06)'},

  {emoji:'🎰',cat:'Arcade · Classic',title:'Pinball Paradise',
   desc:'Full Vegas-style pinball! Slingshot launch, spinning bumpers, 4 flippers. Pure arcade magic.',
   href:'/pinball',color:'rgba(20,80,40,0.15)',neon:'#ffd700',neonbg:'rgba(255,215,0,0.06)'},

  {emoji:'🥕',cat:'Encyclopedia · Quiz',title:'Veggie & Fruit Bible',
   desc:'77 vegetables and fruits. Real nutrition data, botanical art, quizzes and rankings.',
   href:'/veggies',color:'rgba(184,147,63,0.12)',neon:'#ffd700',neonbg:'rgba(255,215,0,0.06)',featured:true},

  {emoji:'🐬',cat:'Memory · Cards',title:'Dolphin Card Game',
   desc:'Flip the full 52-card deck across 2 rounds. Find every pair to win.',
   href:'/dolphins',color:'rgba(34,211,238,0.12)',neon:'#ffd700',neonbg:'rgba(255,215,0,0.06)'},

  {emoji:'🌋',cat:'Arcade · Strategy',title:"Pele's Fury",
   desc:"Stack the lava rocks, trigger eruptions. Hawaii's most explosive game.",
   href:'/peles-fury',color:'rgba(239,68,68,0.12)',neon:'#ffd700',neonbg:'rgba(255,215,0,0.06)'},

  {emoji:'🐢',cat:'Board · Strategy',title:'Turtle Checkers',
   desc:'Classic checkers with a Hawaiian twist. Challenge a friend or the AI.',
   href:'/turtle-checkers',color:'rgba(34,197,94,0.12)',neon:'#ffd700',neonbg:'rgba(255,215,0,0.06)'},

  {emoji:'♛',cat:'Board · Strategy',title:'Mermaid Chess',
   desc:'Full chess with stunning mermaid pieces. Classic strategy, ocean style.',
   href:'/mermaid-chess',color:'rgba(139,92,246,0.12)',neon:'#ffd700',neonbg:'rgba(255,215,0,0.06)'},

  {emoji:'🌺',cat:'Trivia · Hawaii',title:'Hawaii Trivia',
   desc:'Test your knowledge of the islands. History, culture, nature and more.',
   href:'/trivia',color:'rgba(244,114,182,0.12)',neon:'#ffd700',neonbg:'rgba(255,215,0,0.06)'},

  {emoji:'🧠',cat:'Memory · Puzzle',title:'Aloha Memory',
   desc:'Match beautiful Hawaiian image pairs. Train your memory island style.',
   href:'/memory',color:'rgba(59,130,246,0.12)',neon:'#ffd700',neonbg:'rgba(255,215,0,0.06)'},

  {emoji:'🔤',cat:'Word · Puzzle',title:'Hawaii Word Search',
   desc:'Find hidden Hawaiian words in this beautiful island word puzzle.',
   href:'/word-search',color:'rgba(245,158,11,0.12)',neon:'#ffd700',neonbg:'rgba(255,215,0,0.06)'},

  {emoji:'🎰',cat:'Arcade · Letters',title:'Aloha Letters',
   desc:'Fast-paced letter matching arcade game with Hawaiian words.',
   href:'/aloha-letters',color:'rgba(168,85,247,0.12)',neon:'#ffd700',neonbg:'rgba(255,215,0,0.06)'},

  {emoji:'🎈',cat:'Arcade · Fun',title:'Pop That Balloon!',
   desc:'Pop as many balloons as you can before time runs out!',
   href:'/balloons',color:'rgba(234,179,8,0.12)',neon:'#ffd700',neonbg:'rgba(255,215,0,0.06)'},

  {emoji:'🔮',cat:'Fun · Social',title:'Fortune Roulette',
   desc:'Spin the wheel, discover your Hawaiian fortune. Share with friends!',
   href:'/fortune',color:'rgba(99,102,241,0.12)',neon:'#ffd700',neonbg:'rgba(255,215,0,0.06)'},

  {emoji:'🎭',cat:'Fun · Personality',title:'Who Are You?',
   desc:'Find out which Hawaiian spirit animal you are. Fun for everyone!',
   href:'/who-are-you',color:'rgba(236,72,153,0.12)',neon:'#ffd700',neonbg:'rgba(255,215,0,0.06)'},

  {emoji:'🧪',cat:'Creative · Art',title:'Slime Artists',
   desc:'Mix colours, create slime art. A messy, beautiful creative experience.',
   href:'/slime',color:'rgba(16,185,129,0.12)',neon:'#ffd700',neonbg:'rgba(255,215,0,0.06)'},

  // {emoji:'🎞️',cat:'Creative · Photo',title:'Film Lab',
  //  desc:'Apply gorgeous film filters to your photos. Analogue vibes, digital ease.',
  //  href:'/film-lab',color:'rgba(251,146,60,0.12)',neon:'#ffd700',neonbg:'rgba(255,215,0,0.06)'}, // HIDDEN - not ready yet

  {id:'capitals',title:'Capital City Challenge',emoji:'🌍',
   desc:'195 countries · 195 capitals · Can you name them all? Take the ultimate geography challenge!',
   color:'#0a0a20',href:'/capitals'},

  {id:'jigsaw',title:'Jigsaw Puzzle Gallery',emoji:'🧩',
   desc:'9 beautiful artworks · drag & drop pieces · snap to place · 4 difficulty levels!',
   color:'#0d0d0f',href:'/jigsaw'},

  {id:'trash',emoji:'🧹',cat:'Arcade · Fun',title:'Pick Up The Trash!',
   desc:'Choose your hero and clean up the park or beach!! Pick up litter, dump it in the bins. Fun for all ages!!',
   color:'rgba(34,197,94,0.12)',href:'/trash'},

  {id:'coloring',emoji:'🎨',cat:'Creative · Art',title:'Fab Coloring Book',
   desc:'20 beautiful pages! Pencil, crayon and watercolor brushes, zoom in to color the details, then save or share your masterpiece!!',
   color:'rgba(255,215,0,0.10)',href:'/coloring'},
];
