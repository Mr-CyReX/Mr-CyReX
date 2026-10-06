"""README composition and a matching local preview; no browser-only layout tricks."""
from pathlib import Path
from html import escape
from urllib.parse import urlencode, quote

ROOT=Path(__file__).resolve().parent.parent
ASSET_REV='63ade68'

def picture(name,alt):
    reduced=''
    if name in ('hero','motion','projects'):
        reduced=f'  <source media="(max-width: 600px) and (prefers-reduced-motion: reduce)" srcset="./assets/{name}-mobile-still.svg?v={ASSET_REV}">\n  <source media="(prefers-reduced-motion: reduce)" srcset="./assets/{name}-still.svg?v={ASSET_REV}">\n'
    return f'<picture>\n{reduced}  <source media="(max-width: 600px)" srcset="./assets/{name}-mobile.svg?v={ASSET_REV}">\n  <img src="./assets/{name}.svg?v={ASSET_REV}" width="100%" alt="{escape(alt,quote=True)}">\n</picture>'

def badge(label,logo='',color='F4F6F8',secondary=False):
    query={'style':'flat-square' if secondary else 'for-the-badge','logoColor':color,'labelColor':'000000'}
    if logo: query['logo']=logo
    url='https://img.shields.io/badge/'+quote(label.replace('-','--'),safe='')+'-000000?'+urlencode(query)
    alt='Windows-native tooling' if label=='Windows' else label
    return f'<img src="{escape(url,quote=True)}" height="{22 if secondary else 26}" alt="{escape(alt,quote=True)}">'

primary=[('Rust','rust'),('GPUI',''),('SQLite','sqlite','69C8FF'),('Rive','rive','8DFF78'),('Windows',''),('PowerShell','')]
secondary=[('C++','cplusplus'),('TypeScript','typescript'),('Go','go'),('Docker','docker'),('Git','git'),('GitHub','github'),('Slint','slint')]
streak='https://streak-stats.demolab.com?'+urlencode(dict(user='Mr-CyReX',hide_border='true',background='00000000',border_radius=0,ring='69C8FF',fire='8DFF78',currStreakLabel='A4ADB7',sideLabels='A4ADB7',currStreakNum='F4F6F8',sideNums='F4F6F8',dates='8A949F',stroke='303943',card_width=440,card_height=180,disable_animations='true'))
stats='https://github-readme-stats.vercel.app/api?'+urlencode(dict(username='Mr-CyReX',hide_border='true',bg_color='00000000',title_color='F4F6F8',text_color='A4ADB7',icon_color='69C8FF',border_radius=0,hide_rank='true',show_icons='false',card_width=400,custom_title='Public GitHub stats',disable_animations='true',text_bold='false'))

sections=[]
sections.append(picture('hero','Ali Sh / Mr-CyReX — Software developer & motion graphics designer. Mostly Rust. I build tools I wish existed, then obsess over how they feel.'))
sections.append(picture('stack','Stack'))
sections.append('<p align="center">\n  '+'\n  '.join(badge(*b) for b in primary)+'\n</p>')
sections.append('<p align="center">\n  '+'\n  '.join(badge(*b,secondary=True) for b in secondary)+'\n</p>')
sections.append('<br>\n\n'+picture('projects',"What I'm building: Hexus, Computer Control MCP, Rill and OpsDesk. Full descriptions in the text version below."))
sections.append('<br>\n\n'+picture('motion','Motion still shapes how I build. Hierarchy, timing, transitions, responsiveness, and visual polish are engineering concerns, not decoration.'))
sections.append(picture('activity',"GitHub activity. Most of this work is private, so GitHub only gets to count part of it."))
sections.append('<p align="center">\n  <a href="https://github.com/Mr-CyReX?tab=overview"><img src="'+escape(streak,quote=True)+'" width="440" alt="Live GitHub contribution streak"></a>\n  <a href="https://github.com/Mr-CyReX?tab=repositories"><img src="'+escape(stats,quote=True)+'" width="400" alt="Live public GitHub statistics"></a>\n</p>')
sections.append('<p align="right">\n  <img src="https://komarev.com/ghpvc/?username=Mr-CyReX&amp;style=flat-square&amp;color=000000&amp;label=profile+views" alt="Profile views">\n  <a href="https://github.com/Mr-CyReX?tab=followers"><img src="https://img.shields.io/github/followers/Mr-CyReX?style=flat-square&amp;label=followers&amp;labelColor=000000&amp;color=000000" alt="GitHub followers"></a>\n</p>')
plain='''<details>
<summary>Profile in plain text</summary>

<p><strong>Ali Sh · Mr-CyReX · &lt;/Cy&gt;</strong><br>
Software developer &amp; motion graphics designer</p>
<p>Mostly Rust. I build tools I wish existed, then obsess over how they feel.</p>

<p><strong>Stack:</strong> Rust · GPUI · SQLite · Rive · Windows-native tooling · PowerShell.<br>
C++ · TypeScript · Go · Docker · Git · GitHub · Slint.</p>

<p>Most of my current work is private. These are the pieces I can actually show.</p>
<ul>
<li><strong>Hexus.</strong> The thing I spend most of my time on: my own work harness for projects, agents, tools, and the machine. Rust · GPUI · SQLite.</li>
<li><strong>Computer Control MCP.</strong> Built because screenshot-click guessing got old. Agents get real Windows controls instead. Rust · Windows · IPC · MCP.</li>
<li><strong>Rill.</strong> My excuse to keep pushing GPUI, Rive, window motion, and native desktop UX a little harder.</li>
<li><strong>OpsDesk.</strong> A proper internal-tool demo for work that still lives in spreadsheets. Roles, approvals, imports, audit trails, local data.</li>
</ul>
<p>Motion still shapes how I build. Hierarchy, timing, transitions, responsiveness, and visual polish are engineering concerns to me — not decoration added at the end.</p>
<p>Most of this work is private, so GitHub only gets to count part of it.</p>
</details>'''
sections.append(plain)
body='\n\n'.join(sections)+'\n'
ROOT.joinpath('README.md').write_text('<!-- Ali Sh / Mr-CyReX. Visual system: DESIGN.md. -->\n\n'+body,encoding='utf-8')
ROOT.joinpath('preview.html').write_text('''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Cy profile preview</title><style>
:root{color-scheme:dark;--canvas:#0d1117;--ink:#f0f3f6;--muted:#8A949F;scrollbar-color:#46525E var(--canvas)}
*{box-sizing:border-box}body{margin:0;background:var(--canvas);color:var(--ink);font:16px/1.5 Arial,sans-serif}
main{max-width:1000px;width:calc(100% - 32px);margin:32px auto 80px}
picture{display:block}picture img{display:block;width:100%;height:auto}
p{margin:0 0 16px}img{max-width:100%;vertical-align:middle}a{color:#69C8FF;text-underline-offset:3px;cursor:pointer}
p[align=left]{padding:0 24px;line-height:2.25}p[align=center]{text-align:center}p[align=right]{text-align:right;padding:0 24px}
summary{cursor:pointer;color:var(--muted)}details{margin:32px 24px}details p{margin-top:16px}li{margin-bottom:12px}
a:hover,summary:hover{color:var(--ink)}:focus-visible{outline:2px solid #69C8FF;outline-offset:4px}::selection{background:#69C8FF;color:#000000}
::-webkit-scrollbar{width:12px}::-webkit-scrollbar-track{background:var(--canvas)}::-webkit-scrollbar-thumb{background:#46525E;border:3px solid var(--canvas)}
@media(max-width:600px){main{width:calc(100% - 24px);margin:12px auto 40px}p[align=left],p[align=right]{padding:0 14px}details{margin:24px 14px}}
@media(forced-colors:active){:root{scrollbar-color:auto}}
</style></head><body><main>'''+body+'''</main></body></html>\n''',encoding='utf-8')
print('Generated README and matching responsive preview.')
