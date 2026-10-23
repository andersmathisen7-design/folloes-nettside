"""
Firmasidene fra folloes.no: forsiden, tjenestene, om oss, referanser og kontakt.
Teksten ligger i firma_innhold.py. Toppen, bunnen og stilen er de samme som på bjørkeved-sidene (build.py).

build.py kaller write_all(build) og får tilbake adressene som skal i sitemap.xml.
"""
import firma_innhold as F
from firma_bilder import BILDER, OG

B = None  # build-modulen, settes av write_all()


def esc(t):
    return B.esc(t)


def img(key, alt, sizes="(min-width: 900px) 33vw, 100vw", cls="", eager=False):
    """<img> med WebP i to størrelser når bildet finnes i stort format."""
    if not key or key not in BILDER:
        return ""
    v = BILDER[key]
    w, h = v[800]
    srcset = ", ".join(f"/img/firma/{key}-{bw}.webp {bw}w" for bw in sorted(v))
    load = 'fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
    c = f' class="{cls}"' if cls else ""
    return (f'<img{c} src="/img/firma/{key}-800.webp" srcset="{srcset}" sizes="{sizes}" '
            f'width="{w}" height="{h}" alt="{esc(alt)}" {load}>')


def preload(key):
    v = BILDER[key]
    srcset = ", ".join(f"/img/firma/{key}-{bw}.webp {bw}w" for bw in sorted(v))
    return f'<link rel="preload" as="image" href="/img/firma/{key}-800.webp" imagesrcset="{srcset}" imagesizes="100vw">'


def paras(texts):
    """Avsnitt; linjer som starter med «- » blir punktliste, og nettadresser blir lenker."""
    out, items = [], []
    def link(t):
        return B.re.sub(r"(https?://[^\s<]+?)([.,]?)(?=\s|$)", r'<a href="\1" rel="noopener">\1</a>\2', esc(t))
    for t in texts:
        if t.startswith("- "):
            items.append(f"<li>{link(t[2:])}</li>")
            continue
        if items:
            out.append(f'<ul class="checks dark">{"".join(items)}</ul>'); items = []
        out.append(f"<p>{link(t)}</p>")
    if items:
        out.append(f'<ul class="checks dark">{"".join(items)}</ul>')
    return "".join(out)


def og(key):
    """Delingsbilde i JPEG 1200×630 hvis det finnes for bildet, ellers firmabildet."""
    return f"/img/firma/og-{key}.jpg" if key in OG else ""


def svc_url(s):
    return f"/{s['slug']}/"


def services():
    return F.SERVICES


def real_services():
    """Tjenestene som har egen side her (bjørkeved har sin egen del av nettstedet)."""
    return [s for s in F.SERVICES if s["slug"] != "salg-av-bjorkeved"]


# ---------------------------------------------------------------- byggeklosser

ICONS = {
    # Enkle strektegninger, arver fargen.
    "Vår": '<path d="M12 21v-8m0 0c0-4 3-6 7-6 0 4-3 6-7 6Zm0 0C12 9 9 7 5 7c0 4 3 6 7 6Z"/>',
    "Sommer": '<circle cx="12" cy="12" r="4"/><path d="M12 2v2m0 16v2M4.9 4.9l1.4 1.4m11.4 11.4 1.4 1.4M2 12h2m16 0h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/>',
    "Høst": '<path d="M5 19c8 0 14-6 14-14C11 5 5 10 5 19Zm0 0 7-7"/>',
    "Vinter": '<path d="M12 2v20M4 7l16 10M20 7 4 17M9 3l3 3 3-3M9 21l3-3 3 3"/>',
    "tel": '<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8 9.9a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2Z"/>',
    "mail": '<rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 6-10 7L2 6"/>',
    "pin": '<path d="M20 10c0 6-8 12-8 12S4 16 4 10a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/>',
    "doc": '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8Z"/><path d="M14 2v6h6M8 13h8M8 17h5"/>',
}


def icon(name, cls="ico"):
    return (f'<svg class="{cls}" viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" '
            f'stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS[name]}</svg>')


def crumbs(*trail):
    parts = ['<a href="/">Forsiden</a>'] + [f'<a href="{p}">{esc(n)}</a>' if p else esc(n) for n, p in trail]
    return f'<nav class="crumbs" aria-label="Brødsmuler">{" › ".join(parts)}</nav>'


def page_hero(h1, lead, key, kicker="", crumb="", ctas=True, tall=False, cta_href="#kontakt"):
    cta = ""
    if ctas:
        cta = f"""<div class="hero-cta">
        <a class="btn btn-lg" href="{cta_href}">Få et uforpliktende tilbud</a>
        <a class="btn btn-ghost light btn-lg" href="{B.tel_href()}" data-track="tel">Ring {B.CO['phone_display']}</a>
      </div>"""
    return f"""
<section class="phero{' phero-tall' if tall else ''} on-dark">
  {img(key, "", sizes="100vw", cls="phero-bg", eager=True)}
  <div class="wrap phero-in">
    {crumb}
    {f'<p class="kicker">{esc(kicker)}</p>' if kicker else ''}
    <h1>{esc(h1)}</h1>
    {f'<p class="lead">{esc(lead)}</p>' if lead else ''}
    {cta}
  </div>
</section>"""


def service_cards(items, h="h3"):
    cards = []
    for s in items:
        cards.append(f"""<li class="svc-card">
      <a href="{svc_url(s)}">
        {img(s.get('card_img'), "", sizes="(min-width: 1000px) 360px, (min-width: 640px) 50vw, 100vw")}
        <span class="svc-body">
          <{h}>{esc(s['name'])}</{h}>
          <span class="svc-text">{esc(s['card'])}</span>
          <span class="svc-more">{'Se priser og bestill' if s['slug'] == 'salg-av-bjorkeved' else 'Les mer'} <span aria-hidden="true">→</span></span>
        </span>
      </a>
    </li>""")
    return f'<ul class="svc-grid">{"".join(cards)}</ul>'


def contact_form(selected=""):
    opts = ['<option value="Generell henvendelse">Velg tjeneste (valgfritt)</option>']
    for s in services():
        sel = " selected" if s["name"] == selected else ""
        opts.append(f'<option{sel}>{esc(s["name"])}</option>')
    opts.append('<option>Annet</option>')
    return f"""<form id="kontaktskjema" class="form card contact-form" novalidate>
      <p class="contact-form-h">Send oss en melding</p>
      <p class="muted small">Vi tar kontakt så snart vi kan.</p>
      <label for="k-navn">Navn</label>
      <input id="k-navn" name="navn" autocomplete="name" required>
      <div class="row2">
        <div><label for="k-tel">Telefon</label><input id="k-tel" name="telefon" type="tel" inputmode="tel" autocomplete="tel"></div>
        <div><label for="k-epost">E-post</label><input id="k-epost" name="epost" type="email" autocomplete="email"></div>
      </div>
      <p class="muted small field-hint">Fyll ut telefon eller e-post, så vi kan svare deg.</p>
      <label for="k-tjeneste">Hva gjelder det?</label>
      <select id="k-tjeneste" name="tjeneste">{"".join(opts)}</select>
      <label for="k-melding">Melding</label>
      <textarea id="k-melding" name="melding" rows="4" required placeholder="Fortell kort hva du trenger hjelp med, og hvor eiendommen ligger."></textarea>
      <input class="hp" name="_honey" tabindex="-1" autocomplete="off" aria-hidden="true">
      <button class="btn btn-block btn-lg" type="submit">Send melding</button>
      <p class="form-msg" id="k-msg" role="status" aria-live="polite"></p>
      <p class="muted small">Vi bruker opplysningene bare til å svare deg. Les <a href="/personvernerklaering/">personvernerklæringen</a>.</p>
    </form>"""


def contact_section(selected="", h2="Kom i kontakt med oss"):
    CO = B.CO
    return f"""
<section id="kontakt" class="section contact on-dark">
  <div class="wrap contact-grid">
    <div>
      <p class="kicker">Gratis befaring</p>
      <h2>{esc(h2)}</h2>
      <p class="lead">Har du spørsmål eller ønsker et tilbud? Ring oss, send e-post eller fyll ut skjemaet, så tar vi kontakt.</p>
      <ul class="contact-cards">
        <li><a href="{B.tel_href()}" data-track="tel">{icon("tel")}<span><strong>Ring oss</strong>{CO['phone_display']}</span></a></li>
        <li><a href="mailto:{CO['email']}">{icon("mail")}<span><strong>Send e-post</strong>{CO['email']}</span></a></li>
      </ul>
    </div>
    {contact_form(selected)}
  </div>
</section>"""


def ved_promo():
    P = B.P
    return f"""
<section class="section ved-promo">
  <div class="wrap ved-promo-grid">
    <picture class="ved-promo-img">
      <source type="image/webp" srcset="/img/bjorkeved-levering-follo-768.webp 768w, /img/bjorkeved-levering-follo-1536.webp 1536w" sizes="(min-width: 900px) 50vw, 100vw">
      <img src="/img/bjorkeved-levering-follo-768.jpg" width="768" height="512" alt="Sjåfør fra {esc(B.CO['legal_name'])} leverer sekker med bjørkeved" loading="lazy" decoding="async">
    </picture>
    <div>
      <p class="kicker">Bjørkeved</p>
      <h2>Tørr bjørkeved levert på døra</h2>
      <p>Vi kjører tørr bjørkeved hjem til deg i hele Follo, og bærer den inn hvis du vil. Velg antall sekker og leveringsdag, så ser du prisen med en gang.</p>
      <p class="ved-price"><strong>{P['price']} kr</strong> per 40-liters sekk</p>
      <div class="hero-cta">
        <a class="btn btn-lg" href="{B.VED}#bestill">Bestill bjørkeved</a>
        <a class="btn btn-ghost btn-lg" href="{B.VED}#priser">Se priser</a>
      </div>
    </div>
  </div>
</section>"""


def quotes(items):
    out = []
    for r in items:
        text = "".join(f"<p>{esc(t)}</p>" for t in r["quote"])
        out.append(f"""<figure class="quote card">
      <blockquote>{text}</blockquote>
      <figcaption><strong>{esc(r['name'])}</strong><span>{esc(r['role'])}</span></figcaption>
    </figure>""")
    return f'<div class="quotes">{"".join(out)}</div>'


def service_ld(s):
    return {
        "@context": "https://schema.org",
        "@type": "Service",
        "name": s["name"],
        "description": s["desc"],
        "serviceType": s["name"],
        "url": f"{B.URL}{svc_url(s)}",
        "provider": {"@id": f"{B.URL}/#business"},
        "areaServed": {"@type": "AdministrativeArea", "name": "Follo"},
    }


def title(t):
    t = t.strip()
    return t if "Follo Eiendomsservice" in t else f"{t} | {B.CO['legal_name']}"


# ---------------------------------------------------------------- sidene

def page_forside():
    CO = B.CO
    seasons = "".join(f"""<li>{icon(x['name'], 'ico ico-lg')}<h3>{esc(x['name'])}</h3><p>{esc(x['text'])}</p></li>""" for x in F.SEASONS)
    intro_text = "".join(f"<p>{esc(t)}</p>" for t in F.INTRO["text"])
    intro_list = "".join(f"<li>{esc(t)}</li>" for t in F.INTRO["list"])
    hero = f"""
<section class="phero phero-tall on-dark">
  {img("ansatte", "", sizes="100vw", cls="phero-bg", eager=True)}
  <div class="wrap phero-in">
    <p class="kicker">{esc(CO['legal_name'])}</p>
    <h1>Vaktmester- og vedlikeholdstjenester i Follo</h1>
    <p class="lead">Vi holder eiendommen ryddig, ren og trygg hele året, for privatpersoner, borettslag og bedrifter i Ås og resten av Follo.</p>
    <div class="hero-cta">
      <a class="btn btn-lg" href="#kontakt">Få et uforpliktende tilbud</a>
      <a class="btn btn-ghost light btn-lg" href="{B.tel_href()}" data-track="tel">Ring {CO['phone_display']}</a>
    </div>
    <ul class="hero-points">
      <li>Gratis befaring</li><li>Fast avtale eller enkeltoppdrag</li><li>Brøyteberedskap døgnet rundt</li>
    </ul>
  </div>
</section>
<section class="seasons-wrap">
  <ul class="wrap seasons">{seasons}</ul>
</section>"""
    intro = f"""
<section class="section">
  <div class="wrap intro-grid">
    <div>
      <p class="kicker">Om oss</p>
      <h2>{esc(F.INTRO['h2'])}</h2>
      {intro_text}
      <a class="btn" href="/om-oss/">Les mer om oss</a>
    </div>
    <div class="checkbox-card on-dark">
      <h3>{esc(F.INTRO['list_h3'])}</h3>
      <ul class="checks">{intro_list}</ul>
    </div>
  </div>
</section>"""
    svc = f"""
<section class="section alt" id="tjenester">
  <div class="wrap">
    <div class="section-head center">
      <p class="kicker">Tjenester</p>
      <h2>Våre tjenester</h2>
      <p class="muted">For rene og pene arealer både innendørs og utendørs. Vi tar små og store oppdrag.</p>
    </div>
    {service_cards(services())}
  </div>
</section>"""
    refs = ""
    if F.REFERENCES:
        refs = f"""
<section class="section">
  <div class="wrap">
    <div class="section-head center">
      <p class="kicker">Referanser</p>
      <h2>Dette sier kundene våre</h2>
    </div>
    {quotes(F.REFERENCES[:2])}
    <p class="center"><a href="/referanser/">Se alle referanser →</a></p>
  </div>
</section>"""
    body = hero + intro + svc + ved_promo() + refs + contact_section()
    desc = ("Vaktmester- og vedlikeholdstjenester i Follo: brøyting og strøing, feiing og spyling, gartner, renhold, "
            "HMS, matteutleie, trefelling og bjørkeved. For private, borettslag og bedrifter.")
    ld = B.ld_tags(B.business_ld(), {
        "@context": "https://schema.org", "@type": "WebSite", "name": CO["legal_name"], "url": f"{B.URL}/"})
    return (B.head(f"Vaktmester og vedlikehold i Follo | {CO['legal_name']}", desc, "/", ld,
                   section="firma", preload=preload("ansatte"))
            + body + B.footer("firma"))


def page_tjenester():
    path = "/tjenester/"
    body = page_hero("Tjenester", "Vaktmester, vintertjenester, renhold, gartner og mer. Velg en tjeneste for å lese mer, eller ta kontakt for et tilbud.",
                     "feiemaskin-2", crumb=crumbs(("Tjenester", ""))) + f"""
<section class="section alt">
  <div class="wrap">{service_cards(services(), h="h2")}</div>
</section>""" + contact_section()
    ld = B.ld_tags(B.breadcrumb_ld("Tjenester", path, parents=()))
    return (B.head(title("Tjenester"), "Alle tjenestene til Follo Eiendomsservice AS: vaktmester, vintertjenester, feiing og spyling, gartner, renhold, HMS, matteutleie, trefelling og bjørkeved.",
                   path, ld, section="firma", preload=preload("feiemaskin-2")) + body + B.footer("firma"))


def garasjevask_ekstra(s):
    P = s["pris"]
    inngar = "".join(f"<li>{esc(t)}</li>" for t in P["inngar"])
    tabs = "".join(
        f"""<div class="card price-card"><h3>{esc(t['navn'])}</h3>
      <div class="table-wrap"><table><thead><tr><th>Antall plasser</th><th>Pris per plass</th></tr></thead><tbody>{"".join(f"<tr><td>{esc(a)}</td><td>{esc(b)}</td></tr>" for a, b in t['rader'])}</tbody></table></div>
      <p class="muted small">{esc(t['min'])}</p></div>""" for t in P["tabeller"])
    rab = "".join(f"<li><strong>{esc(a)}</strong> {esc(b)} rabatt</li>" for a, b in P["rabatter"])
    risiko = "".join(f"<li>{esc(t)}</li>" for t in s["risiko"])
    forb = "".join(f"<li>{esc(t)}</li>" for t in s["forberedelser"])
    return f"""
<section class="section alt" id="priser">
  <div class="wrap">
    <div class="section-head center"><p class="kicker">Priser</p><h2>Forutsigbar pris, enkelt forklart</h2><p class="muted">{esc(P['intro'])}</p></div>
    <div class="price-grid">{tabs}</div>
    <div class="price-grid">
      <div class="card price-card"><h3>Hva inngår i en standard garasjevask</h3><ul class="check-list">{inngar}</ul></div>
      <div class="card price-card"><h3>Rabatt ved binding</h3><ul class="check-list">{rab}</ul><p class="muted small">{esc(P['kjoring'])}</p></div>
    </div>
  </div>
</section>
<section class="section" id="priskalkulator">
  <div class="wrap">
    <div class="section-head center"><p class="kicker">Priskalkulator</p><h2>Få en veiledende pris</h2><p class="muted">Én parkeringsplass tilsvarer ca. 25 m². Prisen er veiledende. Endelig avtale bekreftes etter befaring.</p></div>
    <form class="card form gv-calc" id="gv-calc" novalidate>
      <label for="gv-underlag">Underlag</label>
      <select id="gv-underlag"><option value="betong">Betongunderlag (én operatør)</option><option value="asfalt">Asfaltunderlag (to personer)</option></select>
      <div class="row2">
        <div><label for="gv-plasser">Antall parkeringsplasser</label><input id="gv-plasser" type="number" min="1" inputmode="numeric" value="50"></div>
        <div><label for="gv-km">Kjørelengde én vei fra Ås (km)</label><input id="gv-km" type="number" min="0" inputmode="numeric" value="20"></div>
      </div>
      <label for="gv-binding">Binding (rabatt på veiledende total)</label>
      <select id="gv-binding"><option value="0">Ingen binding</option><option value="0.10">2 år (10 %)</option><option value="0.15">3 år (15 %)</option><option value="0.20">5 år (20 %)</option></select>
      <div class="gv-result" id="gv-result" role="status" aria-live="polite"></div>
      <a class="btn btn-block" href="#kontakt" id="gv-send">Be om tilbud</a>
    </form>
  </div>
</section>
<section class="section alt">
  <div class="wrap price-grid">
    <div class="card price-card"><h2 class="h3">Risiko og hensyn</h2><ul class="check-list">{risiko}</ul></div>
    <div class="card price-card"><h2 class="h3">Forberedelser for kunde</h2><ul class="check-list">{forb}</ul></div>
  </div>
</section>
<script>
(function(){{
var T={{betong:[[50,230],[150,220],[400,205]],asfalt:[[50,270],[100,255],[200,235]]}},MIN=8500,KM=13;
var f=document.getElementById("gv-calc"),r=document.getElementById("gv-result"),last="";
function fmt(n){{return Math.round(n).toLocaleString("nb-NO")+" kr";}}
function calc(){{
 var u=document.getElementById("gv-underlag").value,n=Math.max(0,Math.floor(+document.getElementById("gv-plasser").value||0)),
 km=Math.max(0,+document.getElementById("gv-km").value||0),d=+document.getElementById("gv-binding").value,t=T[u],p=null;
 for(var i=0;i<t.length;i++){{if(n<=t[i][0]){{p=t[i][1];break;}}}}
 if(!n){{r.textContent="Fyll inn antall parkeringsplasser.";last="";return;}}
 if(p===null){{r.textContent="Over "+t[t.length-1][0]+" plasser: pris på forespørsel.";last="Garasjevask, "+n+" plasser ("+u+"). Ønsker pris.";return;}}
 var vask=Math.max(MIN,n*p),kjor=km*KM,sum=(vask+kjor)*(1-d);
 r.innerHTML="<strong>Veiledende pris: "+fmt(sum)+"</strong><br><span class='muted small'>Vask "+fmt(vask)+(vask===MIN&&n*p<MIN?" (minstepris)":"")+" + kjøring "+fmt(kjor)+(d?", rabatt "+Math.round(d*100)+" %":"")+".</span>";
 last="Garasjevask, "+n+" plasser ("+u+"), "+km+" km fra Ås, veiledende pris "+fmt(sum)+". Ønsker tilbud.";
}}
f.addEventListener("input",calc);f.addEventListener("submit",function(e){{e.preventDefault();}});
document.getElementById("gv-send").addEventListener("click",function(){{var m=document.getElementById("k-melding");if(m&&last&&!m.value)m.value=last;}});
calc();
}})();
</script>"""


def page_service(s):
    path = svc_url(s)
    hero = page_hero(s["h1"], s.get("lead", ""), s.get("hero_img") or s.get("card_img"),
                     crumb=crumbs(("Tjenester", "/tjenester/"), (s["name"], "")),
                     cta_href="#priskalkulator" if s.get("pris") else "#kontakt")
    blocks = []
    for i, sec in enumerate(s.get("sections", [])):
        text = paras(sec.get("text", []))
        pic = img(sec.get("img"), "", sizes="(min-width: 900px) 50vw, 100vw", cls="split-img") if sec.get("img") else ""
        flip = " flip" if i % 2 else ""
        blocks.append(f"""<div class="split{flip}{'' if pic else ' no-img'}">
      <div><h2>{esc(sec['h2'])}</h2>{text}<a class="btn btn-sm" href="#kontakt">Ta kontakt</a></div>
      {pic}
    </div>""")
    tasks = ""
    if s.get("tasks"):
        items = "".join(f"""<li>{img(t.get('img'), "", sizes="(min-width: 1000px) 280px, 50vw")}<h3>{esc(t['name'])}</h3></li>""" for t in s["tasks"])
        tasks = f"""
<section class="section alt">
  <div class="wrap">
    <div class="section-head center"><p class="kicker">{esc(s['name'])}</p><h2>Vi kan hjelpe deg med</h2></div>
    <ul class="task-grid">{items}</ul>
  </div>
</section>"""
    others = [x for x in services() if x["slug"] != s["slug"]]
    links = "".join(f'<li><a href="{svc_url(x)}">{esc(x["name"])}</a></li>' for x in others)
    more = f"""
<section class="section">
  <div class="wrap">
    <h2 class="h3">Andre tjenester</h2>
    <ul class="pill-links">{links}</ul>
  </div>
</section>"""
    body = (hero + f'\n<section class="section"><div class="wrap splits">{"".join(blocks)}</div></section>'
            + (garasjevask_ekstra(s) if s.get("pris") else "") + tasks + contact_section(selected=s["name"]) + more)
    ld = B.ld_tags(service_ld(s), B.breadcrumb_ld(s["name"], path, parents=(("Tjenester", "/tjenester/"),)))
    key = s.get("hero_img") or s.get("card_img")
    return (B.head(title(s["title"]), s["desc"], path, ld, section="firma",
                   og_image=og(key), preload=preload(key)) + body + B.footer("firma"))


def page_om_oss():
    path = "/om-oss/"
    A = F.ABOUT
    text = "".join(f"<p>{esc(t)}</p>" for t in A["text"])
    lst = "".join(f"<li>{esc(t)}</li>" for t in F.INTRO["list"])
    body = page_hero(A["h1"], A.get("lead", ""), "ansatte", crumb=crumbs((A["h1"], ""))) + f"""
<section class="section">
  <div class="wrap intro-grid">
    <div><p class="kicker">{esc(B.CO['legal_name'])}</p><h2>{esc(F.INTRO['h2'])}</h2>{text}</div>
    <div class="checkbox-card on-dark"><h3>{esc(F.INTRO['list_h3'])}</h3><ul class="checks">{lst}</ul></div>
  </div>
</section>
<section class="section alt">
  <div class="wrap">
    <div class="section-head center"><p class="kicker">Referanser</p><h2>Dette sier kundene våre</h2></div>
    {quotes(F.REFERENCES)}
  </div>
</section>""" + contact_section()
    ld = B.ld_tags(B.breadcrumb_ld(A["h1"], path, parents=()))
    return (B.head(title("Om oss"), "Follo Eiendomsservice AS (tidligere Min Eiendomsservice AS) leverer vaktmester- og vedlikeholdstjenester til private, borettslag og bedrifter i Follo.",
                   path, ld, section="firma", preload=preload("ansatte")) + body + B.footer("firma"))


def page_referanser():
    path = "/referanser/"
    body = page_hero("Referanser", "Vi har utført mange forskjellige oppdrag for borettslag, bedrifter og privatpersoner. Her er noe av det kundene sier.",
                     "feiemaskin-5", crumb=crumbs(("Referanser", ""))) + f"""
<section class="section alt">
  <div class="wrap">{quotes(F.REFERENCES)}</div>
</section>""" + contact_section()
    ld = B.ld_tags(B.breadcrumb_ld("Referanser", path, parents=()))
    return (B.head(title("Referanser"), "Hva kundene sier om Follo Eiendomsservice AS: styreledere i borettslag om vaktmestertjenester, renhold og snømåking.",
                   path, ld, section="firma", preload=preload("feiemaskin-5")) + body + B.footer("firma"))


def page_kontakt():
    path = "/kontakt-oss/"
    CO = B.CO
    maps = esc("https://www.google.com/maps/search/?api=1&query=" + f"{CO['street']}, {CO['postal_code']} {CO['city']}".replace(" ", "+"))
    body = f"""
<section class="section">
  <div class="wrap">
    {crumbs(("Kontakt oss", ""))}
    <h1>Kontakt oss</h1>
    <p class="lead">Ring, send e-post eller fyll ut skjemaet, så tar vi kontakt.</p>
    <div class="contact-page">
      <ul class="info-cards">
        <li><a href="{B.tel_href()}" data-track="tel">{icon("tel")}<span><strong>Ring oss</strong>{CO['phone_display']}</span></a></li>
        <li><a href="mailto:{CO['email']}">{icon("mail")}<span><strong>Send e-post</strong>{CO['email']}</span></a></li>
        <li><a href="{maps}" rel="noopener">{icon("pin")}<span><strong>Adresse</strong>{esc(CO['street'])}, {CO['postal_code']} {esc(CO['city'])}</span></a></li>
        <li><div>{icon("doc")}<span><strong>Org.nr.</strong>{CO['org_nr']}</span></div></li>
      </ul>
      <div id="kontakt">{contact_form()}</div>
    </div>
    <p class="muted">Vil du bestille ved? Bruk <a href="{B.VED}#bestill">bestillingsskjemaet for bjørkeved</a>, der ser du pris og ledige leveringsdager med en gang.</p>
  </div>
</section>"""
    ld = B.ld_tags(B.business_ld(), B.breadcrumb_ld("Kontakt oss", path, parents=()))
    return (B.head(title("Kontakt oss"), f"Kontakt Follo Eiendomsservice AS i Ås: ring {CO['phone_display']}, send e-post til {CO['email']} eller bruk kontaktskjemaet.",
                   path, ld, section="firma") + body + B.footer("firma"))


def page_takk():
    body = f"""
<section class="section">
  <div class="wrap narrow center">
    <h1>Takk for henvendelsen!</h1>
    <p class="lead">Vi har fått meldingen din og tar kontakt så snart vi kan.</p>
    <p>Haster det? Ring <a href="{B.tel_href()}">{B.CO['phone_display']}</a>.</p>
    <p><a class="btn" href="/">Til forsiden</a> <a class="btn btn-ghost" href="/tjenester/">Se tjenestene</a></p>
  </div>
</section>"""
    return B.head(title("Takk for henvendelsen"), "Henvendelsen er mottatt.", "/takk-for-din-henvendelse/",
                  noindex=True, section="firma") + body + B.footer("firma")


def write_all(build):
    global B
    B = build
    B.write("index.html", page_forside())
    B.write("tjenester/index.html", page_tjenester())
    for s in real_services():
        B.write(f"{s['slug']}/index.html", page_service(s))
    B.write("om-oss/index.html", page_om_oss())
    B.write("referanser/index.html", page_referanser())
    B.write("kontakt-oss/index.html", page_kontakt())
    B.write("takk-for-din-henvendelse/index.html", page_takk())
    return (["/", "/tjenester/"] + [svc_url(s) for s in real_services()]
            + ["/om-oss/", "/referanser/", "/kontakt-oss/"])
