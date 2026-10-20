import re, sys, html
shell, src, out, title, desc = sys.argv[1:6]
head = open(shell).read().split('<main>')[0]
head = head.replace('    ul { padding-left: 22px; }', '    ul, ol { padding-left: 22px; }')
head = head.replace('</style>', '''    .doc figure { margin: 22px 0; }
    .doc figure.banner img { display: block; width: 100%; aspect-ratio: 8 / 3; object-fit: cover; border-radius: 14px; }
    .doc figure.shot { text-align: center; }
    .doc figure.shot img { width: 100%; max-width: 260px; height: auto; border-radius: 30px; border: 1px solid var(--line); }
    .doc figcaption { font-size: 14px; color: var(--ink-3); margin-top: 8px; }
    .doc ul.cards { list-style: none; padding: 0; display: grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); gap: 16px; }
    .doc ul.cards li { margin: 0; border: 1px solid var(--line); border-radius: 14px; overflow: hidden; background: var(--paper); }
    .doc ul.cards img { display: block; width: 100%; aspect-ratio: 8 / 3; object-fit: cover; }
    .doc ul.cards .card-text { display: block; padding: 12px 14px 14px; font-size: 15px; }
  </style>''', 1)
head = re.sub(r'<title>.*?</title>', f'<title>{title} — Pleats</title>', head)
head = re.sub(r'<meta name="description" content=".*?">', f'<meta name="description" content="{desc}">', head)
# Share tags (Open Graph, read by Pinterest, iMessage, Slack…): the shell's own are dropped,
# the page's are built from its title, its address and the share copy of its first photo.
head = re.sub(r'\n\s*<(meta (property="og:|name="twitter:)|link rel="canonical")[^>]*>', '', head)
page = out.removesuffix('.html').removesuffix('index')
banner = re.search(r'!\[[^\]]*\]\(/guides/img/([\w-]+)\.jpg\)', open(src).read())
share = f'/og/{banner.group(1)}.jpg' if banner else '/og/home.jpg'
tags = f'''
  <link rel="canonical" href="https://plts.app/{page}">
  <meta property="og:type" content="article">
  <meta property="og:site_name" content="Pleats">
  <meta property="og:title" content="{html.escape(title)}">
  <meta property="og:description" content="{html.escape(desc)}">
  <meta property="og:url" content="https://plts.app/{page}">
  <meta property="og:image" content="https://plts.app{share}">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta name="twitter:card" content="summary_large_image">'''
head = re.sub(r'(<meta name="description" content=".*?">)', lambda m: m.group(1) + tags, head, count=1)
def inline(t):
    t = html.escape(t, quote=False)
    t = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', t)
    t = re.sub(r'\[([^\]]+)\]\(([^)\s]+)\)', r'<a href="\2">\1</a>', t)
    t = re.sub(r'(?<!href=")(https://[^\s)<"]+)', r'<a href="\1">\1</a>', t)
    t = re.sub(r'(?<![/\w.@])(www\.dvi\.gov\.lv|telemetrydeck\.com/privacy|reportaproblem\.apple\.com)', r'<a href="https://\1">\1</a>', t)
    t = re.sub(r'hello@plts\.app', r'<a href="mailto:support@plts.app">support@plts.app</a>', t)
    return t
IMAGE = re.compile(r'!\[([^\]]*)\]\((\S+?)(?: "(\w+)")?\)')
def figure(m):
    alt, src, kind = html.escape(m.group(1)), m.group(2), m.group(3) or 'banner'
    caption = f'<figcaption>{alt}</figcaption>' if kind == 'shot' else ''
    return f'<figure class="{kind}"><img src="{src}" alt="{alt}" loading="lazy">{caption}</figure>'
def card(item):
    # "- ![alt](img) [Title](url): text" → a card with the picture on top
    m = IMAGE.match(item)
    rest = item[m.end():].strip()
    link = re.match(r'\[([^\]]+)\]\(([^)\s]+)\)(.*)', rest)
    text = f'<a href="{link.group(2)}"><strong>{html.escape(link.group(1))}</strong></a>{inline(link.group(3))}'
    return f'<li><a href="{link.group(2)}"><img src="{m.group(2)}" alt="{html.escape(m.group(1))}" loading="lazy"></a><span class="card-text">{text}</span></li>'
body, para, lst, ol = [], [], [], []
def flush():
    global para, lst, ol
    if para: body.append('<p>' + '<br>'.join(inline(p) for p in para) + '</p>'); para = []
    if lst and IMAGE.match(lst[0]): body.append('<ul class="cards">' + ''.join(card(l) for l in lst) + '</ul>'); lst = []
    if lst: body.append('<ul>' + ''.join(f'<li>{inline(l)}</li>' for l in lst) + '</ul>'); lst = []
    if ol: body.append('<ol>' + ''.join(f'<li>{inline(l)}</li>' for l in ol) + '</ol>'); ol = []
for line in open(src).read().splitlines():
    numbered = re.match(r'\d+\. (.*)', line)
    if not line.strip(): flush()
    elif line.startswith('# '): flush(); body.append(f'<h1>{inline(line[2:])}</h1>')
    elif line.startswith('## '): flush(); body.append(f'<h2>{inline(line[3:])}</h2>')
    elif IMAGE.fullmatch(line.strip()): flush(); body.append(figure(IMAGE.fullmatch(line.strip())))
    elif line.startswith('- '): (para or ol) and flush(); lst.append(line[2:])
    elif numbered: (para or lst) and flush(); ol.append(numbered.group(1))
    else: (lst or ol) and flush(); para.append(line)
flush()
foot = '''  </article></main>
  <footer>
    <div class="wrap">
      <span>Pleats · made in Riga</span>
      <nav>
        <a href="mailto:support@plts.app">support@plts.app</a>
        <a href="/support">Support</a>
        <a href="/privacy">Privacy</a>
        <a href="/terms">Terms</a>
      </nav>
    </div>
  </footer>
</body>
</html>
'''
open(out, 'w').write(head + '<main><article class="doc">\n' + '\n'.join(body) + '\n' + foot)
