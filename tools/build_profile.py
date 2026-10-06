"""Generate the GitHub-safe artwork. Requires fontTools only for this authoring step.

All display lettering is outlined from the bundled OFL font. SVG images need no
font downloads, scripts, foreignObject, or build step on GitHub.
"""
from pathlib import Path
from html import escape
from urllib.request import urlretrieve
import json
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'assets'

def authoring_font(name,url):
    cache=ROOT/'.qa'/name
    if not cache.exists():
        cache.parent.mkdir(parents=True,exist_ok=True)
        try:
            urlretrieve(url,cache)
        except Exception as exc:
            raise RuntimeError(f'Could not fetch authoring font {name}. Keep the .qa cache or run once with network access.') from exc
    return cache

FONT_PATH = authoring_font('SpaceGrotesk.ttf','https://raw.githubusercontent.com/google/fonts/main/ofl/spacegrotesk/SpaceGrotesk%5Bwght%5D.ttf')
_raw_font = TTFont(FONT_PATH)
_axes = {a.axisTag for a in _raw_font['fvar'].axes} if 'fvar' in _raw_font else set()
FONT = instantiateVariableFont(_raw_font, {'wght':700} if 'wght' in _axes else {}, inplace=True)
GLYPHS = FONT.getGlyphSet()
CMAP = FONT.getBestCmap()
UPM = FONT['head'].unitsPerEm

# Secondary type system: Archivo for role/body copy. It is used only at
# authoring time; generated SVGs contain paths, never the font file.
BODY_FONT_PATH = authoring_font('IBMPlexSans.ttf','https://raw.githubusercontent.com/google/fonts/main/ofl/ibmplexsans/IBMPlexSans%5Bwdth%2Cwght%5D.ttf')
_body_raw = TTFont(BODY_FONT_PATH)
_body_axes = {a.axisTag for a in _body_raw['fvar'].axes} if 'fvar' in _body_raw else set()
_body_loc = {}
if 'wght' in _body_axes: _body_loc['wght']=400
if 'wdth' in _body_axes: _body_loc['wdth']=100
BODY_FONT = instantiateVariableFont(_body_raw, _body_loc, inplace=True)
BODY_GLYPHS = BODY_FONT.getGlyphSet()
BODY_CMAP = BODY_FONT.getBestCmap()
BODY_UPM = BODY_FONT['head'].unitsPerEm

_role_raw = TTFont(BODY_FONT_PATH)
_role_axes = {a.axisTag for a in _role_raw['fvar'].axes} if 'fvar' in _role_raw else set()
_role_loc = {}
if 'wght' in _role_axes: _role_loc['wght']=600
if 'wdth' in _role_axes: _role_loc['wdth']=100
ROLE_FONT = instantiateVariableFont(_role_raw, _role_loc, inplace=True)
ROLE_GLYPHS = ROLE_FONT.getGlyphSet()
ROLE_CMAP = ROLE_FONT.getBestCmap()
ROLE_UPM = ROLE_FONT['head'].unitsPerEm

CSS = '''
.tile{fill:#000000;stroke:#303943;stroke-width:1}
.ink{fill:#F4F6F8}.muted{fill:#A4ADB7}.dim{fill:#8A949F}.accent-cyan{fill:#69C8FF}.accent-lime{fill:#8DFF78}
.page{fill:#F4F6F8}.page-muted{fill:#A4ADB7}
.body{font-family:Arial,Helvetica,sans-serif}.mono{font-family:Consolas,"Liberation Mono",monospace}
.line{fill:none;stroke:#46525E;stroke-width:1}.guide{fill:none;stroke:#303943;stroke-width:1;stroke-dasharray:2 6}
.cyan{fill:none;stroke:#69C8FF;stroke-width:2}.lime{fill:none;stroke:#8DFF78;stroke-width:2}.handle{fill:none;stroke:#707E8B;stroke-width:1}
.node{fill:#000000;stroke:#69C8FF;stroke-width:1.5}.control{fill:#000000;stroke:#8A949F;stroke-width:1}
.pulse{animation:pulse 12s ease-in-out infinite}.cursor{animation:blink 1.15s steps(1,end) infinite}.signal{animation:signalPulse 14s ease-in-out infinite}
.draw{stroke-dasharray:1000;stroke-dashoffset:0;animation:draw 1.8s cubic-bezier(.22,1,.36,1) both}
@keyframes draw{from{stroke-dashoffset:1000}to{stroke-dashoffset:0}}
@keyframes pulse{0%,20%,100%{opacity:.65}55%{opacity:1}}
@keyframes signalPulse{0%,8%,100%{opacity:.32}18%,42%{opacity:1}52%,92%{opacity:.32}}
@keyframes blink{0%,60%,100%{opacity:1}61%,85%{opacity:.15}}
@media(prefers-color-scheme:light){.page{fill:#171D23}.page-muted{fill:#4D5965}}
@media(prefers-reduced-motion:reduce){*{animation:none!important;transition:none!important}.draw{stroke-dashoffset:0}.moving{display:none}}
'''

def path(d, cls='line', **attrs):
    a=' '.join(f'{k.replace("_","-")}="{escape(str(v),quote=True)}"' for k,v in attrs.items())
    return f'<path d="{d}" class="{cls}" {a}/>'

def _outline(s,x,y,size,cls,glyphs,cmap,upm,**attrs):
    pen=SVGPathPen(glyphs, ntos=lambda n: f'{n:.2f}'.rstrip('0').rstrip('.'))
    pos=0
    for ch in s:
        name=cmap.get(ord(ch))
        if name is None:
            raise KeyError(f'font is missing glyph {ch!r} in {s!r}')
        glyphs[name].draw(TransformPen(pen,(1,0,0,1,pos,0)))
        pos+=glyphs[name].width
    a=' '.join(f'{k.replace("_","-")}="{escape(str(v),quote=True)}"' for k,v in attrs.items() if k not in ('font_weight','letter_spacing'))
    return f'<g data-lettering="{escape(s,quote=True)}" class="{cls}" aria-label="{escape(s,quote=True)}" {a}><title>{escape(s)}</title><path transform="translate({x} {y}) scale({size/upm:.6f} {-size/upm:.6f})" d="{pen.getCommands()}"/></g>'

def text(s,x,y,size=17,cls='body muted',**attrs):
    if 'body' in cls.split():
        return _outline(s,x,y,size,cls,BODY_GLYPHS,BODY_CMAP,BODY_UPM,**attrs)
    a=' '.join(f'{k.replace("_","-")}="{escape(str(v),quote=True)}"' for k,v in attrs.items())
    return f'<text x="{x}" y="{y}" font-size="{size}" class="{cls}" {a}>{escape(s)}</text>'

def display(s,x,y,size,cls='ink'):
    pen=SVGPathPen(GLYPHS, ntos=lambda n: f'{n:.2f}'.rstrip('0').rstrip('.'))
    pos=0
    for ch in s:
        name=CMAP[ord(ch)]
        GLYPHS[name].draw(TransformPen(pen,(1,0,0,1,pos,0)))
        pos+=GLYPHS[name].width
    return f'<g data-lettering="{escape(s,quote=True)}" class="{cls}" aria-label="{escape(s,quote=True)}"><title>{escape(s)}</title><path transform="translate({x} {y}) scale({size/UPM:.6f} {-size/UPM:.6f})" d="{pen.getCommands()}"/></g>'

def advance(s,size):
    return sum(GLYPHS[CMAP[ord(ch)]].width for ch in s)*size/UPM

def display_sequence(parts,x,y,size):
    out=[];pos=x
    label=''.join(part for part,_ in parts)
    for part,cls in parts:
        out.append(display(part,pos,y,size,cls))
        pos+=advance(part,size)
    return f'<g data-lettering="{escape(label,quote=True)}" aria-label="{escape(label,quote=True)}"><title>{escape(label)}</title>'+''.join(out)+'</g>'

def role_advance(s,size):
    return sum(ROLE_GLYPHS[ROLE_CMAP[ord(ch)]].width for ch in s)*size/ROLE_UPM

def role_sequence(parts,x,y,size):
    out=[];pos=x
    label=''.join(part for part,_ in parts)
    for part,cls in parts:
        out.append(_outline(part,pos,y,size,cls,ROLE_GLYPHS,ROLE_CMAP,ROLE_UPM))
        pos+=role_advance(part,size)
    return f'<g data-lettering="{escape(label,quote=True)}" aria-label="{escape(label,quote=True)}"><title>{escape(label)}</title>'+''.join(out)+'</g>'

def lines(strings,x,y,size=17,leading=25,cls='body muted'):
    return ''.join(text(s,x,y+i*leading,size,cls) for i,s in enumerate(strings))

def custom_mark(x,y,scale=1):
    # Personal </Cy> wordmark: geometric code delimiters + a motion-built C/y.
    # Intentionally not set in the display font.
    white='#F4F6F8'
    c=path('M72 16 L18 64 L72 112','',fill='none',stroke=white,stroke_width=24,stroke_linecap='square',stroke_linejoin='miter')
    c+=path('M165 6 L128 122','',fill='none',stroke=white,stroke_width=27,stroke_linecap='square')
    c+=path('M173 8 L136 120','',fill='none',stroke='#69C8FF',stroke_width=5,stroke_linecap='square',opacity='.95')
    c+=path('M322 24 C288 2 226 12 210 66 C194 120 246 147 321 120','',fill='none',stroke=white,stroke_width=29,stroke_linecap='square')
    c+=path('M349 22 L400 78 L452 22 M400 78 L381 138','',fill='none',stroke=white,stroke_width=28,stroke_linecap='square',stroke_linejoin='bevel')
    c+=path('M492 16 L546 64 L492 112','',fill='none',stroke=white,stroke_width=24,stroke_linecap='square',stroke_linejoin='miter')
    c+='<rect x="375" y="133" width="11" height="11" fill="#8DFF78"/>'
    return f'<g data-lettering="&lt;/Cy&gt;" aria-label="&lt;/Cy&gt;" transform="translate({x} {y}) scale({scale})"><title>&lt;/Cy&gt;</title>{c}</g>'

def heading_accent(x,y):
    # Two broken registration shards: solid bodies with tapered, low-opacity
    # tips facing the central break. Their glow is weaker than the card cuts.
    cbody=f'M{x} {y-1} H{x+25} V{y+1} H{x} Z'
    ctip=f'M{x+25} {y-1} L{x+30} {y} L{x+25} {y+1} Z'
    lbody=f'M{x+38} {y-1} H{x+48} V{y+1} H{x+38} Z'
    ltip=f'M{x+38} {y-1} L{x+33} {y} L{x+38} {y+1} Z'
    glow=path(cbody,'',fill='#31586B',opacity='.22',filter='url(#edgeBlur)')
    glow+=path(ctip,'',fill='#31586B',opacity='.12',filter='url(#edgeBlur)')
    glow+=path(lbody,'',fill='#45683F',opacity='.20',filter='url(#edgeBlur)')
    glow+=path(ltip,'',fill='#45683F',opacity='.11',filter='url(#edgeBlur)')
    cyan=path(cbody,'',fill='#69C8FF')+path(ctip,'',fill='#69C8FF',opacity='.34')
    lime=path(lbody,'',fill='#8DFF78')+path(ltip,'',fill='#8DFF78',opacity='.34')
    return glow+cyan+lime

def tile_d(x,y,w,h,cut=28):
    return f'M{x} {y} H{x+w-cut} L{x+w} {y+cut} V{y+h} H{x+cut} L{x} {y+h-cut} Z'

def tile(x,y,w,h,cut=28):
    d=tile_d(x,y,w,h,cut)
    # Slight black lift against GitHub's #0d1117 canvas.
    shadow=path(d,'',fill='#000000',stroke='none',opacity='.66',filter='url(#tileShadow)')
    base=path(d,'tile')
    # Partial inner bevels keep the plane machined instead of making a second border.
    inner=path(f'M{x+4} {y+4} H{x+w-cut-12}','',fill='none',stroke='#17212A',stroke_width=1,opacity='.82')
    inner+=path(f'M{x+w-4} {y+cut+12} V{y+h-16}','',fill='none',stroke='#141D25',stroke_width=1,opacity='.72')
    return shadow+base+inner

def tile_accents(x,y,w,h,cut=28):
    # Cyan energizes the upper-right cut; lime answers from the opposite
    # lower-left cut. The under-strokes are deliberately desaturated.
    c1=f'M{x+w-cut} {y} L{x+w} {y+cut}'
    c2=f'M{x+cut} {y+h} L{x} {y+h-cut}'
    glow=path(c1,'',fill='none',stroke='#31586B',stroke_width=7,opacity='.34',filter='url(#edgeBlur)')
    glow+=path(c2,'',fill='none',stroke='#45683F',stroke_width=7,opacity='.30',filter='url(#edgeBlur)')
    return glow+path(c1,'cyan')+path(c2,'lime')

def safe(x,y,w,h,items):
    return f'<g data-box="{x},{y},{w},{h}">{items}</g>'

def node(x,y,color='#69C8FF',r=3):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{color}"/>'

def anchor(x,y):
    return f'<rect x="{x-4}" y="{y-4}" width="8" height="8" class="node"/>'

def control(x,y):
    return f'<circle cx="{x}" cy="{y}" r="3" class="control"/>'

def matrix(x,y,cols,rows,step=9,opacity=.34):
    """Registration texture, aligned to a real panel or drawing extent."""
    return f'<g fill="#46525E" opacity="{opacity}">'+''.join(f'<circle cx="{x+i*step}" cy="{y+j*step}" r=".85"/>' for i in range(cols) for j in range(rows))+'</g>'

def port(x,y,color='#8A949F'):
    return f'<rect x="{x-4}" y="{y-4}" width="8" height="8" fill="#000000" stroke="{color}" stroke-width="1"/>'+node(x,y,color,1.4)

def workspace_map(x,y,scale=1):
    """Hexus's four stated concerns, drawn as a shared workspace bus."""
    c=path('M0 12 H14 V84 M14 12 H30 M14 36 H30 M14 60 H30 M14 84 H30','line')+port(0,12,'#8DFF78')
    for i,label in enumerate(['PROJECTS','AGENTS','TOOLS','MACHINE']):
        c+=port(30,12+i*24)+text(label,44,16+i*24,10,'mono dim',letter_spacing=1)
    return f'<g transform="translate({x} {y}) scale({scale})">{c}</g>'

def rill_track(x,y):
    c=path('M0 22 H160','line')
    c+=path('M0 22 C12 22 12 7 24 7 C36 7 36 37 48 37 C60 37 60 7 72 7 C84 7 84 37 96 37 C108 37 108 22 120 22 H160','cyan',opacity='.65')
    c+=path('M0 48 H160 M80 2 V53','guide')+port(0,48)+port(160,48)+port(80,48)+node(96,37,'#69C8FF',2.6)
    return f'<g transform="translate({x} {y})">{c}</g>'

def approval_path(x,y):
    c=path('M0 0 H20 L34 14 H60','line')
    c+=port(0,0)+port(34,14)+port(60,14)
    return f'<g transform="translate({x} {y})">{c}</g>'

def svg(name,w,h,desc,content,extra=''):
    defs='<defs><filter id="edgeBlur" x="-100%" y="-100%" width="300%" height="300%"><feGaussianBlur stdDeviation="3"/></filter><filter id="tileShadow" x="-12%" y="-12%" width="124%" height="130%"><feGaussianBlur stdDeviation="3"/><feOffset dx="0" dy="3"/></filter></defs>'
    result=f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title desc">\n<title id="title">{escape(desc.split(". ")[0])}</title>\n<desc id="desc">{escape(desc)}</desc>\n{defs}\n<style>{CSS}{extra}</style>\n{content}\n</svg>\n'
    if 'mobile' in name:
        result=result.replace('font-size="16" class="body', 'font-size="18" class="body').replace('font-size="15" class="body', 'font-size="17" class="body')
    OUT.joinpath(name+'.svg').write_text(result,encoding='utf-8')
    if name.startswith(('hero','motion','projects')):
        static='*{animation:none!important;transition:none!important}.moving{display:none!important}.draw{stroke-dashoffset:0!important}'
        OUT.joinpath(name+'-still.svg').write_text(result.replace('</style>',static+'</style>'),encoding='utf-8')

def terminal_cycle(x,y,size=14):
    build='cargo build --release'
    test='cargo test --workspace'

    def down(cmd):
        return [cmd[:n] for n in range(len(cmd),-1,-1)]

    def up(cmd):
        return [cmd[:n] for n in range(0,len(cmd)+1)]

    # ~3s holds, then ~200ms/character typing/backspacing.
    frames=[build]*14 + down(build)[1:] + up(test)[1:] + [test]*14 + down(test)[1:] + up(build)[1:]
    n=len(frames)
    css='.term-frame{opacity:0}.term-f0{opacity:1}'
    parts=[]
    char_advance=8.42*(size/14)

    for i,cmd in enumerate(frames):
        start=100*i/n
        end=100*(i+1)/n
        eps=.015
        if i==0:
            keys=f'0%,{end-eps:.3f}%{{opacity:1}}{end:.3f}%,100%{{opacity:0}}'
        elif i==n-1:
            keys=f'0%,{start-eps:.3f}%{{opacity:0}}{start:.3f}%,100%{{opacity:1}}'
        else:
            keys=f'0%,{start-eps:.3f}%{{opacity:0}}{start:.3f}%,{end-eps:.3f}%{{opacity:1}}{end:.3f}%,100%{{opacity:0}}'
        css += f'@keyframes tf{i}{{{keys}}}.term-f{i}{{animation:tf{i} 24s steps(1,end) infinite}}'
        label='> '+cmd
        caret_x=x+len(label)*char_advance+2.5
        parts.append(
            f'<g class="term-frame term-f{i}">'
            + text(label,x,y,size,'mono muted')
            + f'<rect x="{caret_x:.2f}" y="{y-size+3:.2f}" width="2" height="{size-3}" fill="#69C8FF" class="cursor"/>'
            + '</g>'
        )
    return ''.join(parts),css

def pen_curve():
    d='M930 100 C846 62 715 78 714 164 C713 250 845 253 921 215'
    content=path('M714 62 V253 M930 62 V253 M684 100 H958 M684 215 H958','guide')
    content+=path('M930 100 L846 62 M714 164 L715 78 M714 164 L713 250 M921 215 L845 253','handle')
    content+=path(d,'cyan draw',pathLength='1000')
    content+=''.join(control(x,y) for x,y in [(846,62),(715,78),(713,250),(845,253)])
    content+=anchor(930,100)+f'<rect x="710" y="160" width="8" height="8" fill="#000000" stroke="#8DFF78" stroke-width="1.5"/>'+anchor(921,215)
    content+=f'<circle r="3" fill="#F4F6F8" class="moving"><animateMotion dur="12s" repeatCount="indefinite" path="{d}"/></circle>'
    # Pen nib, precisely located at the selected anchor; not a decorative orbit.
    content+=path('M930 100 L946 106 L951 119 L938 114 Z','',fill='#F4F6F8')+path('M930 100 L942 110','',stroke='#000000',stroke_width=1)+node(942,110,'#000000',1.8)
    content+=text('P0',940,90,9,'mono dim')+text('P1',727,172,9,'mono dim')+text('P2',932,233,9,'mono dim')
    return content

def hero(mobile=False):
    if not mobile:
        c=matrix(942,286,5,9,9,.5)
        c+=path('M8 72 V8 H176 M832 8 H898 L940 50 V76 M8 302 V342 L52 386 H156','line',opacity='.6')
        c+=path('M156 386 H250 V410 H352 M940 82 H982 V150 H966 M900 414 H824 V426 H742','line',opacity='.26')
        c+=node(250,410,'#46525E',1.2)+node(982,150,'#46525E',1.2)
        c+=tile(24,24,900,346,36)+tile_accents(24,24,900,346,36)
        c+=path('M54 105 V81 H78 M514 81 H538 V105 M54 239 V263 H78 M514 263 H538 V239','line',opacity='.75')
        c+=path('M62 225 H578','guide',opacity='.65')
        c+=matrix(616,104,3,16,8,.27)
        c+=path('M888 24 L924 60','',stroke='#69C8FF',stroke_width=2)
        role=role_sequence([('Software developer ','ink'),('&','accent-lime'),(' motion graphics designer','ink')],62,299,22)
        c+=safe(60,50,600,296,text('ALI SH  /  MR-CYREX',62,70,12,'mono dim',letter_spacing=1.5)+display_sequence([('<','ink'),('/','accent-cyan'),('Cy>','ink')],52,224,182)+role+text('Mostly Rust. I build tools I wish existed, then obsess over how they feel.',62,338,16,'body muted'))
        c+=pen_curve()
        c+=text('PATH / CUBIC',716,286,10,'mono dim',letter_spacing=1.4)
        c+=path('M684 280 H698 V266 M956 280 H972 V264','line')
        c+=tile(596,345,380,66,20)+tile_accents(596,345,380,66,20)
        c+=node(623,379,'#8DFF78',4)
        terminal,terminal_css=terminal_cycle(644,384,14)
        c+=safe(640,360,304,34,terminal)
        # The console physically overlaps the identity; no arbitrary line to nowhere.
        svg('hero',1000,436,'Ali Sh / Mr-CyReX. Software developer & motion graphics designer. I build native tools, internal software, and systems I actually use.',c,terminal_css)
    else:
        c=path('M4 70 V6 H116 M320 6 H390 L416 32 V68','line',opacity='.65')
        c+=tile(12,16,396,520,26)
        c+=matrix(38,350,8,15,9,.45)
        c+=path('M382 16 L408 42','',stroke='#69C8FF',stroke_width=2)
        c+=safe(34,34,350,280,text('ALI SH  /  MR-CYREX',36,53,11.5,'mono dim',letter_spacing=1)+display('</Cy>',29,161,112)+lines(['Software developer &','motion graphics designer'],36,209,20,27,'body ink')+lines(['I build native tools, internal software,','and systems I actually use.'],36,280,16,24))
        c+='<g transform="translate(-480 280) scale(.9)">'+pen_curve()+'</g>'
        c+=tile(38,514,358,60,18)+node(59,544,'#8DFF78',3)
        c+=safe(75,526,294,32,text('> cargo build --release',78,549,13,'mono muted'))
        c+='<rect x="259" y="539" width="3" height="11" fill="#69C8FF" class="cursor"/>'
        svg('hero-mobile',420,594,'Ali Sh / Mr-CyReX. Software developer & motion graphics designer. I build native tools, internal software, and systems I actually use.',c)

def rail(name,label,mobile=False,description=None):
    w=420 if mobile else 1000
    size=30 if mobile else 34
    end=404 if mobile else 976
    c=display(label,16 if mobile else 24,44,size,'page')
    if not mobile:
        c+=heading_accent(24,4)
    if label=='Stack':
        start=130 if mobile else 160
        c+=path(f'M{start} 35 H{end} V54','line')
        if not mobile:
            c+=f'<circle r="2.3" fill="#69C8FF" class="moving signal"><animateMotion dur="16s" begin="1.5s" repeatCount="indefinite" path="M160 35 H976"/></circle>'
        h=64
    else:
        start=300 if mobile else 346
        c+=path(f'M{start} 35 H{end} V58','line')
        if not mobile:
            c+=f'<circle r="2.3" fill="#8DFF78" class="moving signal"><animateMotion dur="17s" begin="4s" repeatCount="indefinite" path="M346 35 H976"/></circle>'
        if mobile:
            c+=lines(["Most of what I'm building right now is private,",'so the public graph is only part of it.'],16,81,15,23,'body page-muted');h=128
        else:
            c+=text("Most of this work is private, so GitHub only gets to count part of it.",24,81,16,'body page-muted');h=112
    svg(name+('-mobile' if mobile else ''),w,h,description or label,c)

def projects(mobile=False):
    if not mobile:
        c=heading_accent(24,4)+display("What I'm building",24,48,40,'page')+text('Most of my current work is private. These are the pieces I can actually show.',24,81,16,'body page-muted')
        c+=path('M180 104 H236 V92 H304 M842 92 H976 V128 H954 M8 414 H70 V438 H104 M610 692 H632 V730 H764','line',opacity='.23')
        c+=node(236,92,'#46525E',1.15)+node(632,730,'#46525E',1.15)
        # Ports connect exact tile edges. Branches name relationships, not dependencies.
        c+=matrix(28,466,6,22,9,.48)+matrix(914,104,8,4,9,.36)
        c+=path('M8 168 V104 H124 M16 654 V706 L44 734 H166 M864 730 H992 V634','line',opacity='.65')
        c+=path('M572 244 H590 L612 266 H628','line')
        c+=path('M284 370 V390 L262 412 H242 L220 434 V450 M284 390 H564 L604 430 H778 L806 458 V502','line')
        c+=port(284,390)
        c+='<circle r="2.2" fill="#69C8FF" class="moving"><animateMotion dur="12s" begin="2s" repeatCount="indefinite" path="M572 244 H590 L612 266 H628"/></circle>'
        c+='<circle r="2.2" fill="#69C8FF" class="moving"><animateMotion dur="15s" begin="5s" repeatCount="indefinite" path="M284 370 V390 L262 412 H242 L220 434 V450"/></circle>'
        c+='<circle r="2.2" fill="#8DFF78" class="moving"><animateMotion dur="16s" begin="8s" repeatCount="indefinite" path="M284 390 H564 L604 430 H778 L806 458 V502"/></circle>'
        c+=text('NATIVE UI / MOTION',240,437,11.5,'mono page-muted')
        c+=text('INTERNAL TOOLS',826,474,11,'mono page-muted')
        c+=tile(24,120,548,250,32)+tile_accents(24,120,548,250,32)
        c+=path('M40 140 H62 M520 160 V142 H502','line',opacity='.8')
        c+=safe(56,150,484,198,display('Hexus',52,219,72)+lines(['The thing I spend most of my time on:','my own work harness for projects, agents,','tools, and the machine.'],56,265,18,25)+text('RUST · GPUI · SQLITE',56,343,12,'mono dim',letter_spacing=1))
        c+=workspace_map(388,155,.92)
        c+=tile(628,154,348,254,28)+tile_accents(628,154,348,254,28)
        c+=path('M794 201 H836 V225 H814 M802 207 L808 213 L802 219 M816 220 H826','line')
        c+=safe(658,183,286,198,display('CC MCP',658,226,34)+lines(['Built because screenshot-click guessing','got old. Agents get real Windows','controls instead.'],660,276,15.5,23)+text('RUST · WINDOWS · IPC · MCP',660,365,11,'mono dim'))
        c+=tile(104,450,506,204,28)+tile_accents(104,450,506,204,28)
        c+=rill_track(388,478)
        c+=safe(134,480,444,148,display('Rill',132,520,52)+lines(['My excuse to keep pushing GPUI, Rive,','window motion, and native desktop UX','a little harder.'],136,561,17,25))
        c+=tile(652,502,324,212,26)+tile_accents(652,502,324,212,26)
        c+=approval_path(878,538)
        c+=safe(680,530,264,158,display('OpsDesk',680,555,34)+lines(['A proper internal-tool demo for work','that still lives in spreadsheets.'],684,592,15.5,23)+lines(['Roles, approvals, imports,','audit trails, local data.'],684,648,15.5,23))
        for x,y in [(572,244),(628,266),(284,370),(220,450),(806,502)]:c+=port(x,y)
        svg('projects',1000,750,"What I'm building. Hexus is the main project, with Computer Control MCP, Rill and OpsDesk as related branches.",c)
    else:
        c=display("What I'm",16,43,36,'page')+display('building',16,84,36,'page')
        c+=lines(['Most of it is private; these are the parts','that best explain what I work on.'],16,118,16,23,'body page-muted')
        c+=matrix(4,472,2,64,9,.28)
        c+=path('M204 414 V426 L190 440 H40 L26 454 V1054 M26 492 H46 M26 772 H46 M26 1016 H46','line')
        c+=tile(12,176,396,238,26)
        c+=safe(34,200,350,186,display('Hexus',32,255,60)+lines(['The thing I spend most of my time on —','my workspace for projects, agents, tools,','and the machine itself.'],36,298,16,24)+text('RUST · GPUI · SQLITE',36,382,11.5,'mono dim'))
        c+=workspace_map(270,207,.67)
        c+=tile(46,466,362,240,24)
        c+=safe(68,490,316,192,display('Computer Control',68,519,28)+display('MCP',68,552,28)+lines(['I built this because screenshot-click','guessing got annoying. Now agents','get actual controls.'],70,591,16,24)+text('RUST · WINDOWS · IPC · MCP',70,678,11,'mono dim'))
        c+=tile(46,744,362,208,24)
        c+='<g transform="translate(268 774) scale(.6)">'+rill_track(0,0)+'</g>'
        c+=safe(68,766,316,158,display('Rill',66,802,44)+lines(['A music player I keep rebuilding','whenever I want to push GPUI · Rive ·','window motion a little harder.'],70,848,16,24))
        c+=tile(46,990,362,210,24)
        c+=approval_path(308,1030)
        c+=safe(66,1010,318,166,display('OpsDesk',66,1047,34)+lines(['A demo for business work that still','gets trapped in spreadsheets.'],70,1087,16,24)+lines(['Roles, approvals, imports, audit trails,','local data.'],70,1145,16,24))
        for x,y in [(204,414),(46,492),(46,772),(46,1016)]:c+=port(x,y)
        # End the common bus on the last branch, never below it.
        c=c.replace('V1054','V1016')
        svg('projects-mobile',420,1224,"What I'm building. Hexus, Computer Control MCP, Rill and OpsDesk.",c)

def graph():
    # Exact cubic-bezier(.22, 1, .36, 1), plus its control polygon.
    c=path('M-20 36 V-24 H54 M246 -24 H318 L328 -14 V40 M328 190 V270 H252 M58 270 H-20 V210','line',opacity='.65')
    c+=matrix(260,170,6,5,8,.3)
    c+=path('M0 186 V14 M0 186 H300','line')
    c+=path('M0 100 H300 M150 14 V186','guide')
    c+=path('M0 186 L66 14 M300 14 H108','handle')
    c+=path('M0 186 C66 14 108 14 300 14','cyan')
    c+=f'<rect x="-4" y="182" width="8" height="8" fill="#000000" stroke="#8DFF78" stroke-width="1.5"/>'+anchor(300,14)+control(66,14)+control(108,14)
    c+=path('M0 222 H300','line')
    c+=path('M75 216 V228 M150 216 V228 M225 216 V228','line')
    c+=path('M0 216 L6 222 L0 228 L-6 222 Z M300 216 L306 222 L300 228 L294 222 Z','',fill='#8A949F')
    c+=text('0',0,252,11,'mono page-muted')+text('1',294,252,11,'mono page-muted')
    c+=text('TIME',130,252,11,'mono page-muted',letter_spacing=1)
    c+=text('POSITION',0,2,11,'mono page-muted',letter_spacing=1)
    c+=text('.22, 1, .36, 1',182,2,10,'mono page-muted')
    c+='<g class="moving playhead">'+path('M0 8 V229','',stroke='#8DFF78',stroke_width=1,opacity='.7')+'</g>'
    c+='<circle r="3.5" fill="#F4F6F8" class="moving point"/>'
    frames=[];heads=[]
    for i in range(21):
        t=i/20;u=1-t;x=3*u*u*t*66+3*u*t*t*108+t**3*300;y=u**3*186+(1-u**3)*14;p=10+t*70
        frames.append(f'{p:g}%{{transform:translate({x:.2f}px,{y:.2f}px)}}')
        heads.append(f'{p:g}%{{transform:translateX({x:.2f}px)}}')
    extra='@keyframes point{0%,10%{transform:translate(0px,186px)}'+''.join(frames)+'80%,100%{transform:translate(300px,14px)}}'
    extra+='@keyframes head{0%,10%{transform:translateX(0px)}'+''.join(heads)+'80%,100%{transform:translateX(300px)}}'
    extra+='@keyframes traceVisibility{0%,90%{opacity:1}95%,100%{opacity:0}}.point{animation:point 12s linear infinite,traceVisibility 12s linear infinite}.playhead{animation:head 12s linear infinite,traceVisibility 12s linear infinite}'
    return c,extra

def motion(mobile=False):
    g,css=graph()
    if not mobile:
        c=heading_accent(24,4)+display('Motion still shapes',24,59,42,'page')+display('how I build.',24,106,42,'page')
        c+=path('M536 104 H602 V84 H626 M552 278 H620 V294 H690','line',opacity='.23')+matrix(572,150,4,8,8,.18)
        c+=node(602,84,'#46525E',1.15)+node(620,294,'#46525E',1.15)
        c+=safe(24,134,546,160,lines(['Hierarchy, timing, transitions, responsiveness,','and visual polish are engineering concerns to me —'],24,165,17,27,'body page-muted')+text('not decoration added at the end.',24,229,17,'body page-muted'))
        c+='<g transform="translate(650 40)">'+g+'</g>'
        svg('motion',1000,334,'Motion still shapes how I build. Hierarchy, timing, transitions, responsiveness, and visual polish are engineering concerns to me, not decoration added at the end.',c,css)
    else:
        c=display('Motion graphics',16,44,34,'page')+display('came first.',16,84,34,'page')
        c+=lines(['Before software took over most of my time,','I was doing motion graphics and video editing.'],16,126,16,24,'body page-muted')
        c+=lines(['I still care way too much about timing, rhythm,','hierarchy, and transitions.'],16,185,16,24,'body page-muted')
        c+=text('Now I just apply the same brain to software.',16,247,16,'body page-muted')
        c+='<g transform="translate(52 307)">'+g+'</g>'
        svg('motion-mobile',420,590,'Motion graphics came first. Timing, rhythm, hierarchy, and transitions, applied to software.',c,css)

for mobile in [False,True]:
    hero(mobile);rail('stack','Stack',mobile);projects(mobile);motion(mobile);rail('activity','GitHub activity',mobile)
print('Generated 10 responsive SVG assets and 6 reduced-motion variants.')
