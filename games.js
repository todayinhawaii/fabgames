// ── MASTER GAMES LIST ─────────────────────────────────────────
// Edit this ONE file to add/remove games from BOTH the home page and play page!!
// Both index.html and play.html load this file via <script src="/games.js"></script>

const GAMES=[
  // ── ROW 1 ──
  {id:'animal-discovery',emoji:'🐾',cat:'Discovery · Kids',title:'Animal Discovery',
   desc:'Drag each animal into its silhouette on the habitat board! Barn, Forest, Ocean and Jungle — discover 30 amazing animals across 5 beautiful habitats!!',
   color:'rgba(80,180,80,0.15)',href:'/animal-discovery'},
  {id:'strawberry-farm',emoji:'🍓',cat:'Educational · Kids',title:'Strawberry Farm',
   desc:'Help the farmer fill the basket! Drag the exact number of strawberries you\'re told into the basket — count carefully and watch the basket fill up!!',
   color:'rgba(216,32,58,0.15)',href:'/strawberry-farm'},
  {id:'spelling-game',emoji:'🔤',cat:'Educational · Kids',title:'Spelling Game',
   desc:'Drag the swaying letters to spell fruits, vegetables, animals and pets! Colourful art, levels that get trickier, and big celebrations when you get it right!!',
   color:'rgba(139,95,230,0.15)',href:'/spelling-game'},
  {id:'teapot-guineapigs',emoji:'🫖',cat:'Memory · Fun',title:'Teapot Guinea Pigs',
   desc:'12 adorable guinea pigs hide behind 12 pretty teapots! Meet them all, then see if you remember who\'s hiding where. Sweet, cute and surprisingly tricky!!',
   color:'rgba(255,143,196,0.15)',href:'/teapot-guineapigs'},
  {id:'henry',emoji:'🦛',cat:'Memory · Fun',title:"Henry the Hungry Hippo",
   desc:"Open Henry's mouth and study where each cupcake sits — then remember it all! Drag them back in the right place. 3 to 10 cupcakes — endless fun!!",
   color:'rgba(100,180,220,0.15)',href:'/henry'},

  {id:'grandmas-cupboard',emoji:'🧺',cat:'Memory · Fun',title:"Grandma's Cupboard",
   desc:"Open the cupboard and study what's inside — then close it! Can you remember where everything goes? Drag it all back in the right place. Easy, Medium and Hard!!",
   color:'rgba(180,120,80,0.15)',href:'/grandmas-cupboard'},
  {id:'donut',emoji:'🍩',cat:'Arcade · Fun',title:'Donut Dash',
   desc:'Hit the falling donuts into the goal — but watch out for the mad chef!! He floats around and if he touches you, you lose ALL your points!! How high can you score??',
   color:'rgba(255,157,226,0.15)',href:'/donut'},

  {id:'blob',emoji:'🍦',cat:'Arcade · Fun',title:'Blob Boy',
   desc:'Move Blob Boy to eat ice creams and cakes! He grows bigger and bigger with every bite — until Professor Popper shows up!!',
   color:'rgba(255,157,226,0.15)',href:'/blob'},

  {id:'learn-the-body',emoji:'🧠',cat:'Educational · Kids',title:'Learn The Body',
   desc:'Tap any part of the boy or girl body to learn what it does! Switch to Quiz Mode to test yourself - fun for all ages!!',
   color:'rgba(255,143,171,0.10)',href:'/learn-the-body'},

  {emoji:'🎭',cat:'Fun · Personality',title:'Who Are You?',id:'whoareyou',
   desc:'Find out which Hawaiian spirit animal you are. Fun for everyone!',
   href:'/who-are-you',color:'rgba(236,72,153,0.12)',neon:'#ffd700',neonbg:'rgba(255,215,0,0.06)'},

  // ── ROW 2 ──
  {emoji:'🎈',cat:'Arcade · Fun',title:'Pop That Balloon!',
   desc:'Pop as many balloons as you can before time runs out!',
   href:'/balloons',color:'rgba(234,179,8,0.12)',neon:'#ffd700',neonbg:'rgba(255,215,0,0.06)'},

  {id:'trash',emoji:'🧹',cat:'Arcade · Fun',title:'Pick Up The Trash!',
   desc:'Choose your hero and clean up the park or beach!! Pick up litter, dump it in the bins. Fun for all ages!!',
   color:'rgba(34,197,94,0.12)',href:'/trash'},

  {id:'happy-buttons-2',emoji:'🎨',cat:'ASMR · Creative',title:'Happy Buttons 2',
   desc:'Six gorgeous big squishy buttons with slime sounds — press them in, pop them out! Satisfying ASMR fun for all ages. Pure joy in every press!!',
   color:'rgba(255,100,200,0.15)',href:'/happy-buttons-2'},

  {id:'happy-buttons-3',emoji:'🎨',cat:'ASMR · Creative',title:'Happy Buttons 3',
   desc:'Six brand new squishy art buttons with fun sounds — press them in, pop them out! Satisfying ASMR fun for all ages. Pure joy in every press!!',
   color:'rgba(100,200,255,0.15)',href:'/happy-buttons-3'},

  {id:'happy-buttons-4',emoji:'🎨',cat:'ASMR · Creative',title:'Happy Buttons 4',
   desc:'Six gorgeous squishy art buttons with amazing sounds — press them in, pop them out! Satisfying ASMR fun for all ages. Pure joy in every press!!',
   color:'rgba(200,255,100,0.15)',href:'/happy-buttons-4'},

  {id:'happy-buttons-5',emoji:'🎨',cat:'ASMR · Creative',title:'Happy Buttons 5',
   desc:'Six incredible squishy art buttons with wild sounds — press them in, pop them out! Satisfying ASMR fun for all ages. Pure joy in every press!!',
   color:'rgba(255,200,100,0.15)',href:'/happy-buttons-5'},

  {id:'happy-buttons-6',emoji:'🎨',cat:'ASMR · Creative',title:'Happy Buttons 6',
   desc:'Six fantastic squishy art buttons with cool sounds — press them in, pop them out! Satisfying ASMR fun for all ages. Pure joy in every press!!',
   color:'rgba(200,100,255,0.15)',href:'/happy-buttons-6'},


  {id:'happy-buttons',emoji:'🐾',cat:'ASMR · Relaxation',title:'Happy Buttons',
   desc:'Press the adorable squishy animal buttons for a satisfying ASMR experience!! 10 different sounds - pop, squish, boing and more. Just press and relax!!',
   color:'rgba(255,183,197,0.15)',href:'/happy-buttons'},

  {emoji:'🧠',cat:'Memory · Puzzle',title:'Aloha Memory Game',
   desc:'This fun game is perfect for helping improve your memory for any age!',
   href:'/memory',color:'rgba(59,130,246,0.12)',neon:'#ffd700',neonbg:'rgba(255,215,0,0.06)'},

  // ── REST ──
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

  {emoji:'🌋',cat:'Arcade · Strategy',title:"Pele's Fury",id:'pelesfury',
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

  {emoji:'🔤',cat:'Word · Puzzle',title:'Hawaii Word Search',
   desc:'Find hidden Hawaiian words in this beautiful island word puzzle.',
   href:'/word-search',color:'rgba(245,158,11,0.12)',neon:'#ffd700',neonbg:'rgba(255,215,0,0.06)'},

  {emoji:'🎰',cat:'Arcade · Letters',title:'Aloha Letters',
   desc:'Fast-paced letter matching arcade game with Hawaiian words.',
   href:'/aloha-letters',color:'rgba(168,85,247,0.12)',neon:'#ffd700',neonbg:'rgba(255,215,0,0.06)'},

  {emoji:'🔮',cat:'Fun · Social',title:'Fortune Roulette',
   desc:'Spin the wheel, discover your Hawaiian fortune. Share with friends!',
   href:'/fortune',color:'rgba(99,102,241,0.12)',neon:'#ffd700',neonbg:'rgba(255,215,0,0.06)'},

  {emoji:'🧪',cat:'Creative · Art',title:'Slime Artists',
   desc:'Mix colours, create slime art. A messy, beautiful creative experience.',
   href:'/slime',color:'rgba(16,185,129,0.12)',neon:'#ffd700',neonbg:'rgba(255,215,0,0.06)'},

  // {emoji:'🎞️',cat:'Creative · Photo',title:'Film Lab',
  //  desc:'Apply gorgeous film filters to your photos. Analogue vibes, digital ease.',
  //  href:'/film-lab',color:'rgba(251,146,60,0.12)',neon:'#ffd700',neonbg:'rgba(255,215,0,0.06)'}, // HIDDEN - not ready yet

  {id:'capitals',title:'Capital City Challenge',emoji:'🌍',
   desc:'195 countries · 195 capitals · Can you name them all? Take the ultimate geography challenge!',
   color:'#0a0a20',href:'/capitals'},

  {id:'jigsaw',emoji:'🧩',cat:'Puzzle · Art',title:'Jigsaw Puzzle',
   desc:'Drag and snap a beautiful original artwork puzzle together! Easy, Medium, Hard or Expert — then discover hundreds more at jigsaw.games!',
   color:'rgba(201,168,76,0.12)',href:'/jigsaw'},

  {id:'coloring',emoji:'🎨',cat:'Creative · Art',title:'Fab Coloring Book',
   desc:'20 beautiful pages! Pencil, crayon and watercolor brushes, zoom in to color the details, then save or share your masterpiece!!',
   color:'rgba(255,215,0,0.10)',href:'/coloring'},

  {id:'spinme',emoji:'🌍',cat:'Educational · Fun',title:'Spin Me',
   desc:'Spin the globe and land on a city — discover amazing facts, flight times and world wonders from wherever you call home! 50 cities, real geography, Vegas roulette spin!',
   color:'rgba(74,176,255,0.15)',href:'/spinme'},

  {id:'fun-with-numbers',emoji:'🔢',cat:'Educational · Kids',title:'Fun With Numbers',
   desc:'Drag big chunky 3D numbers into their matching carved wooden holes! Perfect for kids and families. Numbers 0–100, Vegas celebrations and happy sounds!!',
   color:'rgba(255,180,0,0.15)',href:'/fun-with-numbers'},

  {id:'fun-with-shapes',emoji:'🌈',cat:'Educational · Kids',title:'Fun With Shapes',
   desc:'Drag gorgeous 3D rainbow shapes into their matching glowing holes! Circle, Square, Triangle and 13 more — Vegas celebrations, neon colours and big happy sounds!!',
   color:'rgba(128,0,255,0.15)',href:'/fun-with-shapes'},

  {id:'magic-sound-keys',emoji:'🎹',cat:'Music · Creative',title:'Magic Sound Keys',
   desc:'Play a real piano keyboard OR unleash 44 hilarious sound effects — animals, crowd, transport, silly sounds, nature and party!! Hours of musical fun for all ages!!',
   color:'rgba(200,0,255,0.15)',href:'/magic-sound-keys'},

  {id:'street-hustler',emoji:'🎩',cat:'Arcade · Strategy',title:'Street Hustler',
   desc:'Watch the ball... or lose it all! 5 cups, 1 ball, NYC back alley vibes. Can you beat the hustler? Easy to Hustler difficulty — the ultimate shell game!!',
   color:'rgba(255,50,0,0.15)',href:'/street-hustler'},

  {id:'fab-house',emoji:'🏠',cat:'Creative · Building',title:'Fab House',
   desc:'Build your dream home in full 3D! Place walls, windows, roofs, furniture and more. Drag, rotate and move anything you place. The ultimate creative building experience!!',
   color:'rgba(255,150,50,0.15)',href:'/fab-house'},

  {id:'crossword',emoji:'🔤',cat:'Word · Puzzle',title:'Fab Crossword',
   desc:'Classic crossword puzzles with a proper interlocking grid! Easy, Medium, Hard and Expert levels. 20 puzzles — animals, science, geography, philosophy and more!!',
   color:'rgba(100,180,255,0.15)',href:'/crossword'},

  {id:'galaxy-explorer',emoji:'🚀',cat:'Educational · Space',title:'Galaxy Explorer',
   desc:'Blast off and tour the solar system! Visit the Sun, all 8 planets, the Moon and a Black Hole! Learn amazing facts and answer quiz questions to earn stars!!',
   color:'rgba(0,100,255,0.15)',href:'/galaxy-explorer'},

  {id:'tic-tac-toe',emoji:'⭕',cat:'Strategy · Classic',title:'Tic Tac Toe',
   desc:'The classic game! Play against the computer on 3×3, 5×5, 9×9 Gomoku or 15×15 Pro! Easy, Good or Excellent difficulty — can you beat the AI??',
   color:'rgba(0,200,255,0.15)',href:'/tic-tac-toe'},

  {id:'mystery-phrase',emoji:'🔤',cat:'Game Show · Word',title:'Mystery Phrase',
   desc:'Spin the wheel, guess the letters and solve the mystery phrase to win big! BANKRUPT wipes your cash! Buy vowels, solve early and rack up the highest score across 3 rounds!!',
   color:'rgba(255,215,0,0.15)',href:'/mystery-phrase'},

  {id:'music-in-space',emoji:'🎵',cat:'ASMR · Relaxation',title:'Music in Space',
   desc:'Drift through an endless tunnel of glowing button pills in deep space, popping gentle harp notes as you go. Drag to steer, adjust speed and size, and play your own comforting tune. No score, just the ride. 🎧',
   color:'rgba(255,143,214,0.15)',href:'/music-in-space'},

  {id:'color-match',emoji:'🎨',cat:'Memory · Puzzle',title:'Color Match',
   desc:'Study a beautiful pastel shade, then find it again among ten close look-alikes! A retro 1960s memory game with hundreds of possible tones — how sharp is your eye for color?',
   color:'rgba(197,180,227,0.15)',href:'/color-match'},

];
