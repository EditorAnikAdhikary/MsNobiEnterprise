#!/usr/bin/env python3
"""Generates the static site into ./site. Edit content here, run `python3 build.py`."""
import html, os, shutil, sys
OUT = sys.argv[1] if len(sys.argv) > 1 else "site"
esc = lambda s: html.escape(s, quote=True)
def b(bn, en, tag="span", cls=""):
    c = f' class="{cls}"' if cls else ""
    return f'<{tag}{c} data-en="{esc(en)}">{bn}</{tag}>'

PHONES = ["01711-574939", "01920-197070", "01710-749976"]
ADDR = ("পুরবালী ব্যাংকের পিছনে, হাইস্পীড ঘাট, নওয়াপাড়া, যশোর, বাংলাদেশ",
        "Behind Purbali Bank, High Speed Ghat, Noapara, Jashore, Bangladesh")
NAME = ("মেসার্স নবী এন্টারপ্রাইজ ও মেসার্স ঝিমীক ট্রান্সপোর্ট এজেন্সি", "M/s Nabi Enterprises & M/s Jhimik Transport Agency")

PRODUCTS = [  # slug, bn, en, desc bn, desc en
 ("fertilizer", "সার", "Fertilizer", "কৃষি ও মাঠের ফসলের জন্য সার সরবরাহ।", "Fertilizer supplied for agricultural and field use."),
 ("cement", "সিমেন্ট", "Cement", "নির্মাণ প্রকল্পের জন্য সিমেন্ট সরবরাহ।", "Cement supplied for construction projects."),
 ("coal", "কয়লা", "Coal", "শিল্প ও বাণিজ্যিক ব্যবহারের জন্য কয়লা সরবরাহ।", "Coal supplied for industrial and commercial use."),
 ("rice", "চাল", "Rice", "বাণিজ্যিক পরিমাণে চাল সরবরাহ।", "Rice supplied in commercial quantities."),
 ("wheat", "গম", "Wheat", "ব্যবসা ও পাইকারি সরবরাহের জন্য গম।", "Wheat for trading and bulk supply."),
 ("stone", "পাথর", "Stone", "নির্মাণ কাজের জন্য পাথর সরবরাহ।", "Stone supplied for construction work."),
 ("oil-cake", "খৈল", "Oil Cake", "পশুখাদ্য ও কৃষি ব্যবহারের জন্য খৈল সরবরাহ।", "Oil cake supplied for feed and agricultural use."),
]
NAV = [("home", "/", "হোম", "Home"), ("about", "/about/", "আমাদের সম্পর্কে", "About Us"),
       ("nabi", "/nabi-enterprises/", "নবী এন্টারপ্রাইজ", "Nabi Enterprises"), ("products", "/products/", "পণ্যের তালিকা", "Products"),
       ("jhimik", "/jhimik-transport/", "ঝিমীক ট্রান্সপোর্ট", "Jhimik Transport"), ("gallery", "/gallery/", "গ্যালারি", "Gallery"),
       ("contact", "/contact/", "যোগাযোগ", "Contact Us")]

# image registry: path -> (alt bn, alt en)
IMGS = {}
def pic(path, bn, en, cls=""):
    IMGS[path] = (bn, en)
    return (f'<figure class="ph {cls}"><img src="/assets/images/{path}" alt="{esc(bn)}" data-alt-en="{esc(en)}" '
            f'loading="lazy" decoding="async" onerror="this.remove()"></figure>')

def tel(n): return f'<a href="tel:{n.replace("-", "")}">{n}</a>'

def layout(url, key, tb, te, db, de, body, depth_prefix=""):
    nav = "".join(f'<li><a href="{u}"{" aria-current=\"page\"" if k == key else ""}>{b(x, y)}</a></li>' for k, u, x, y in NAV)
    foot_links = "".join(f'<li><a href="{u}">{b(x, y)}</a></li>' for k, u, x, y in NAV)
    return f'''<!DOCTYPE html>
<html lang="bn" data-title-en="{esc(te)}" data-desc-en="{esc(de)}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{tb}</title>
<meta name="description" content="{esc(db)}">
<meta property="og:title" content="{esc(tb)}"><meta property="og:description" content="{esc(db)}"><meta property="og:type" content="website"><meta property="og:locale" content="bn_BD"><meta property="og:locale:alternate" content="en_US">
<meta name="theme-color" content="#071D38">
<link rel="icon" href="/assets/logo-mark.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Hind+Siliguri:wght@400;500;600;700&family=Inter:wght@400;500;600&family=Montserrat:wght@600;700;800&display=swap">
<link rel="stylesheet" href="/css/style.css">
</head>
<body>
<a class="skip" href="#main">{b("মূল অংশে যান", "Skip to content")}</a>
<header class="site"><div class="wrap bar">
<a class="brand" href="/" aria-label="{esc(NAME[1])}"><img src="/assets/logo-mark.svg" width="46" height="46" alt=""><span><b>NABI &amp; JHIMIK</b><small>{b("এন্টারপ্রাইজ ও ট্রান্সপোর্ট", "Enterprises &amp; Transport")}</small></span></a>
<nav id="nav" aria-label="Main"><ul>{nav}</ul></nav>
<div class="tools"><div class="lang" role="group" aria-label="Language"><button type="button" data-l="bn" aria-pressed="true">বাংলা</button><button type="button" data-l="en" aria-pressed="false">English</button></div>
<a class="btn gold call" href="tel:01711574939">{b("কল করুন", "Call Now")}</a>
<button class="burger" id="burger" type="button" aria-label="Menu" aria-expanded="false" aria-controls="nav">☰</button></div>
</div></header>
<main id="main">
{body}
</main>
<footer class="site"><div class="wrap"><div class="fg">
<div><a class="brand" href="/"><img src="/assets/logo-mark.svg" width="46" height="46" alt=""><span><b>NABI &amp; JHIMIK</b></span></a>
<p>{b("বাণিজ্য, সরবরাহ ও পরিবহনে দু’টি পরিপূরক প্রতিষ্ঠান।", "Two associated businesses in trade, supply and transportation.")}</p></div>
<div><h4>{b("পাতাসমূহ", "Pages")}</h4><ul>{foot_links}</ul></div>
<div><h4>{b("প্রতিষ্ঠান", "Businesses")}</h4><ul><li><a href="/nabi-enterprises/">{b("মেসার্স নবী এন্টারপ্রাইজ", "M/s Nabi Enterprises")}</a></li><li><a href="/jhimik-transport/">{b("মেসার্স ঝিমীক ট্রান্সপোর্ট এজেন্সি", "M/s Jhimik Transport Agency")}</a></li></ul>
<h4 style="margin-top:22px">{b("প্রোপ্রাইটর", "Proprietor")}</h4><p>{b("মোঃ মিলন মোল্লা", "Md. Milon Molla")}</p></div>
<div><h4>{b("যোগাযোগ", "Contact")}</h4><ul><li>{b(*ADDR)}</li><li>{tel(PHONES[0])} · {tel(PHONES[1])}</li><li>{b("অফিস: ", "Office: ")}{tel(PHONES[2])}</li></ul></div>
</div><div class="copy">{b("© ২০২৬ " + NAME[0] + "। সর্বস্বত্ব সংরক্ষিত।", "© 2026 " + NAME[1] + ". All rights reserved.")}</div></div></footer>
<script src="/js/main.js" defer></script>
</body>
</html>
'''

def hero(img, imgbn, imgen, h1, p, ctas="", crumb="", small=False):
    return (f'<section class="hero{" sm" if small else ""}">{pic(img, imgbn, imgen, "bg")}<div class="wrap">{crumb}'
            f'<h1>{h1}</h1><p>{p}</p>{ctas}</div></section>')
def crumb(*parts):
    return '<nav class="crumb" aria-label="Breadcrumb"><a href="/">' + b("হোম", "Home") + "</a> / " + " / ".join(parts) + "</nav>"
def btn(href, bn, en, cls="gold"): return f'<a class="btn {cls}" href="{href}">{b(bn, en)}</a>'
def head(eb_bn, eb_en, h_bn, h_en):
    return f'<span class="eb">{b(eb_bn, eb_en)}</span><h2>{b(h_bn, h_en)}</h2>'

PIC = {  # product images
 s: pic(f"products/{s}.jpg", f"{bn}", f"{en}") for s, bn, en, _, _ in PRODUCTS}
def pcard(p):
    s, bn, en, dbn, den = p
    return (f'<article class="pc">{pic(f"products/{s}.jpg", bn, en)}<div class="pb"><h3>{b(bn, en)}</h3><small>{b(en, bn)}</small>'
            f'<p>{b(dbn, den)}</p><div class="row">{btn(f"/products/{s}/", "বিস্তারিত", "View Details", "line")}{btn("/contact/", "জিজ্ঞাসা", "Enquiry")}</div></div></article>')

def bizcards():
    return f'''<div class="c2"><article class="bc">{pic("nabi-enterprises/warehouse.jpg", "পণ্য গুদাম ও সরবরাহ", "Commodity warehouse and supply")}<div class="pb"><span class="tag">{b("বাণিজ্য ও সরবরাহ", "Trading &amp; Supply")}</span><h3>{b("মেসার্স নবী এন্টারপ্রাইজ", "M/s Nabi Enterprises")}</h3><p>{b("বিভিন্ন বাণিজ্যিক ও শিল্প পণ্য সরবরাহে নিয়োজিত প্রতিষ্ঠান।", "A business focused on trading and supplying various commercial and industrial commodities.")}</p>{btn("/nabi-enterprises/", "বিস্তারিত দেখুন", "Explore Nabi Enterprises", "line")}</div></article>
<article class="bc j">{pic("transport/truck-freight.jpg", "পণ্যবাহী ট্রাক", "Freight truck")}<div class="pb"><span class="tag">{b("সড়ক ও নৌপথে পরিবহন", "Road &amp; Waterway Transportation")}</span><h3>{b("মেসার্স ঝিমীক ট্রান্সপোর্ট এজেন্সি", "M/s Jhimik Transport Agency")}</h3><p>{b("সড়ক ও নৌপথে বাণিজ্যিক মালামাল পরিবহন সেবা।", "Transportation services for commercial goods through road and waterway networks.")}</p>{btn("/jhimik-transport/", "বিস্তারিত দেখুন", "Explore Jhimik Transport", "line")}</div></article></div>'''

def owner():
    return f'''<div class="two"><div class="pt">{pic("about/proprietor-portrait.jpg", "মোঃ মিলন মোল্লা (প্রতিকৃতি)", "Md. Milon Molla (portrait)", "portrait")}</div><div>
{head("প্রোপ্রাইটর", "Proprietor", "মোঃ মিলন মোল্লা", "Md. Milon Molla")}
<p>{b("মেসার্স নবী এন্টারপ্রাইজ ও মেসার্স ঝিমীক ট্রান্সপোর্ট এজেন্সির প্রোপ্রাইটর। হাইস্পীড ঘাট, নওয়াপাড়া, যশোর থেকে উভয় প্রতিষ্ঠান পরিচালিত।", "Proprietor of M/s Nabi Enterprises and M/s Jhimik Transport Agency. Both businesses operate from High Speed Ghat, Noapara, Jashore.")}</p></div></div>'''

def modes(links=True):
    def blk(cls, img, ibn, ien, hbn, hen, pbn, pen):
        return f'<div class="tb {cls}">{pic(img, ibn, ien, "bg")}<div class="t"><h3>{b(hbn, hen)}</h3><p>{b(pbn, pen)}</p></div></div>'
    return ('<div class="tr">' +
        blk("road", "transport/truck-freight.jpg", "পণ্যবাহী ট্রাক", "Freight truck", "সড়ক পরিবহন", "Road Transportation", "ভারী পণ্যবাহী ট্রাকের মাধ্যমে বাণিজ্যিক মালামাল পরিবহন।", "Commercial goods carried by heavy-duty cargo trucks.") +
        blk("water", "transport/cargo-vessel.jpg", "কার্গো ভেসেল", "Cargo vessel", "নৌপথ পরিবহন", "Waterway Transportation", "নদী ও নৌপথে কার্গো ভেসেলের মাধ্যমে মালামাল পরিবহন।", "Goods moved by cargo vessel along rivers and waterways.") + '</div>')

def band():
    return f'''<section class="band"><div class="wrap"><h2>{b("আসুন, একসাথে গড়ে তুলি ব্যবসার নতুন সম্ভাবনা", "Let’s Build Business Together")}</h2><p>{b("ব্যবসায়িক ও পরিবহন বিষয়ক জিজ্ঞাসার জন্য যোগাযোগ করুন।", "Contact us for business and transportation enquiries.")}</p>{btn("/contact/", "আজই যোগাযোগ করুন", "Contact Us Today")}</div></section>'''

PAGES = {}
# HOME
PAGES["index.html"] = layout("/", "home", NAME[0], "M/s Nabi Enterprises & Jhimik Transport Agency | Noapara, Jashore",
 "সার, সিমেন্ট, কয়লা, চাল, গম, পাথর ও খৈল সরবরাহ এবং সড়ক ও নৌপথে মালামাল পরিবহন। নওয়াপাড়া, যশোর।",
 "Supply of fertilizer, cement, coal, rice, wheat, stone and oil cake, and goods transport by road and waterway. Noapara, Jashore.",
 hero("hero/cargo-ship-port.jpg", "বন্দরে বাণিজ্যিক কার্গো জাহাজ", "Commercial cargo ship at a seaport",
      b("বিশ্বাস, বাণিজ্য ও পরিবহনে নির্ভরতার নাম", "Building Trust Through Trade &amp; Transportation"),
      b("নবী এন্টারপ্রাইজ ও ঝিমীক ট্রান্সপোর্ট এজেন্সি সড়ক ও নৌপথে বাণিজ্য, সরবরাহ ও পরিবহন সেবা প্রদান করে।", "Nabi Enterprises and Jhimik Transport Agency provide trading, supply and transportation services through road and waterway networks."),
      f'<div class="cta">{btn("/about/", "আমাদের সম্পর্কে জানুন", "About Us")}{btn("/contact/", "যোগাযোগ করুন", "Contact Us", "ghost")}</div>',
      f'<span class="eb">{b("নওয়াপাড়া, যশোর", "Noapara, Jashore")}</span>') +
 f'<section><div class="wrap">{head("আমাদের প্রতিষ্ঠান", "Our Businesses", "দু’টি প্রতিষ্ঠান, একই নির্ভরতা", "Two businesses, one standard of reliability")}{bizcards()}</div></section>'
 f'<section class="alt"><div class="wrap">{head("ব্যবসার বৈশিষ্ট্য", "Business Highlights", "আমরা যা করি", "What we do")}<div class="vals"><div><b>{b("সাতটি পণ্য", "Seven products")}</b>{b("সার, সিমেন্ট, কয়লা, চাল, গম, পাথর ও খৈল।", "Fertilizer, cement, coal, rice, wheat, stone and oil cake.")}</div><div><b>{b("সড়ক পরিবহন", "Road transport")}</b>{b("ট্রাকের মাধ্যমে মালামাল পরিবহন।", "Goods carried by truck.")}</div><div><b>{b("নৌপথ পরিবহন", "Waterway transport")}</b>{b("কার্গো ভেসেলের মাধ্যমে মালামাল পরিবহন।", "Goods carried by cargo vessel.")}</div></div></div></section>'
 f'<section><div class="wrap">{head("পণ্য", "Products", "নির্বাচিত পণ্য", "Featured products")}<div class="grid">{"".join(pcard(p) for p in PRODUCTS[:4])}</div><p class="mt">{btn("/products/", "সম্পূর্ণ তালিকা দেখুন", "View Full Catalog", "line")}</p></div></section>'
 f'<section class="alt"><div class="wrap">{head("পরিবহন", "Transportation", "সড়ক ও নৌপথে নির্ভরযোগ্য পরিবহন", "Moving goods by road and by water")}{modes()}<p class="mt">{btn("/jhimik-transport/", "পরিবহন সেবা দেখুন", "View Transport Services", "line")}</p></div></section>'
 f'<section><div class="wrap">{owner()}</div></section>' + band())

PAGES["about/index.html"] = layout("/about/", "about", "আমাদের সম্পর্কে | " + NAME[0], "About Us | Nabi Enterprises & Jhimik Transport Agency",
 "মেসার্স নবী এন্টারপ্রাইজ ও মেসার্স ঝিমীক ট্রান্সপোর্ট এজেন্সির পরিচিতি।", "About M/s Nabi Enterprises and M/s Jhimik Transport Agency.",
 hero("hero/port-operations.jpg", "বন্দরে কার্গো কার্যক্রম", "Cargo operations at a port", b("আমাদের সম্পর্কে", "About Us"), b("একই ঠিকানা থেকে পরিচালিত দু’টি পরিপূরক প্রতিষ্ঠান।", "Two complementary businesses operated from one address."), "", crumb(b("আমাদের সম্পর্কে", "About Us")), True) +
 f'<section><div class="wrap two"><div>{head("পরিচিতি", "Who We Are", "বাণিজ্য, সরবরাহ ও পরিবহন", "Trade, supply and transport")}<p>{b("মেসার্স নবী এন্টারপ্রাইজ সার, সিমেন্ট, কয়লা, চাল, গম, পাথর ও খৈল সরবরাহ করে। মেসার্স ঝিমীক ট্রান্সপোর্ট এজেন্সি সড়ক ও নৌপথে মালামাল পরিবহন সেবা দেয়। উভয় প্রতিষ্ঠান মোঃ মিলন মোল্লার মালিকানাধীন।", "M/s Nabi Enterprises supplies fertilizer, cement, coal, rice, wheat, stone and oil cake. M/s Jhimik Transport Agency provides goods transportation by road and waterway. Both are owned by Md. Milon Molla.")}</p></div>{pic("about/industrial-supply.jpg", "শিল্প ও বাণিজ্যিক সরবরাহ", "Industrial and commercial supply")}</div></section>'
 f'<section class="alt"><div class="wrap">{head("প্রতিষ্ঠান", "Businesses", "আমাদের দুই প্রতিষ্ঠান", "Our two businesses")}{bizcards()}</div></section>'
 f'<section><div class="wrap">{owner()}<div class="vals"><div><b>{b("বিশ্বাস", "Trust")}</b>{b("গ্রাহকের সাথে স্বচ্ছ লেনদেন।", "Transparent dealings with customers.")}</div><div><b>{b("নির্ভরতা", "Reliability")}</b>{b("সরবরাহ ও পরিবহনে দায়িত্বশীলতা।", "Responsibility in supply and transport.")}</div><div><b>{b("পেশাদারিত্ব", "Professionalism")}</b>{b("স্পষ্ট যোগাযোগ ও সততা।", "Clear communication and integrity.")}</div></div></div></section>' + band())

PAGES["nabi-enterprises/index.html"] = layout("/nabi-enterprises/", "nabi", "মেসার্স নবী এন্টারপ্রাইজ | বাণিজ্য ও সরবরাহ", "M/s Nabi Enterprises | Trading & Supply",
 "সার, সিমেন্ট, কয়লা, চাল, গম, পাথর ও খৈল সরবরাহকারী প্রতিষ্ঠান।", "Supplier of fertilizer, cement, coal, rice, wheat, stone and oil cake.",
 hero("nabi-enterprises/warehouse.jpg", "পণ্য গুদাম ও সরবরাহ", "Commodity warehouse and supply", b("মেসার্স নবী এন্টারপ্রাইজ", "M/s Nabi Enterprises"), b("বিভিন্ন বাণিজ্যিক ও শিল্প পণ্য ক্রয়-বিক্রয় ও সরবরাহে নিয়োজিত প্রতিষ্ঠান।", "A commercial trading and supply enterprise."), f'<div class="cta">{btn("/products/", "পণ্যের তালিকা", "Product Catalog")}{btn("/contact/", "জিজ্ঞাসা করুন", "Enquire", "ghost")}</div>', crumb(b("নবী এন্টারপ্রাইজ", "Nabi Enterprises")), True) +
 f'<section><div class="wrap">{head("সরবরাহ", "Supply", "আমরা যা সরবরাহ করি", "What we supply")}<div class="grid">{"".join(pcard(p) for p in PRODUCTS)}</div><p class="mt">{btn("/products/", "সম্পূর্ণ পণ্য তালিকা", "Complete Catalog", "line")}</p></div></section>' + band())

PAGES["products/index.html"] = layout("/products/", "products", "পণ্যের তালিকা | " + NAME[0], "Product Catalog | Nabi Enterprises",
 "সার, সিমেন্ট, কয়লা, চাল, গম, পাথর ও খৈল — পণ্যের তালিকা।", "Product catalog: fertilizer, cement, coal, rice, wheat, stone and oil cake.",
 hero("hero/port-operations.jpg", "বন্দরে কার্গো কার্যক্রম", "Cargo operations at a port", b("পণ্যের তালিকা", "Product Catalog"), b("মেসার্স নবী এন্টারপ্রাইজ সরবরাহকৃত সাতটি পণ্য।", "Seven products supplied by M/s Nabi Enterprises."), "", crumb(b("পণ্য", "Products")), True) +
 f'<section><div class="wrap"><div class="grid">{"".join(pcard(p) for p in PRODUCTS)}</div></div></section>' + band())

for i, (s, bn, en, dbn, den) in enumerate(PRODUCTS):
    rel = [p for p in PRODUCTS if p[0] != s]
    rel = (rel[i:] + rel[:i])[:3]
    PAGES[f"products/{s}/index.html"] = layout(f"/products/{s}/", "products", f"{bn} | " + NAME[0], f"{en} | M/s Nabi Enterprises", dbn, den,
     hero(f"products/{s}.jpg", bn, en, b(bn, en), b(dbn, den), "", crumb(f'<a href="/products/">{b("পণ্য", "Products")}</a>', b(bn, en)), True) +
     f'<section><div class="wrap two">{pic(f"products/{s}.jpg", bn, en)}<div><span class="eb">{b(en, bn)}</span><h2>{b(bn, en)}</h2><p>{b(dbn, den)}</p><p>{b("মেসার্স নবী এন্টারপ্রাইজ, নওয়াপাড়া, যশোর থেকে সরবরাহ করা হয়। স্পেসিফিকেশন, মূল্য ও মজুদ সম্পর্কে জানতে সরাসরি যোগাযোগ করুন।", "Supplied by M/s Nabi Enterprises, Noapara, Jashore. For specifications, prices and availability, please contact us directly.")}</p><div class="row">{btn("/contact/", "জিজ্ঞাসা করুন", "Send Enquiry")}{btn("/products/", "তালিকায় ফিরুন", "Back to Catalog", "line")}</div></div></div></section>'
     f'<section class="alt"><div class="wrap">{head("সংশ্লিষ্ট", "Related", "সংশ্লিষ্ট পণ্য", "Related products")}<div class="grid">{"".join(pcard(p) for p in rel)}</div></div></section>')

PAGES["jhimik-transport/index.html"] = layout("/jhimik-transport/", "jhimik", "মেসার্স ঝিমীক ট্রান্সপোর্ট এজেন্সি | সড়ক ও নৌপথে পরিবহন", "M/s Jhimik Transport Agency | Road & Waterway Transport",
 "সড়ক ও নৌপথে বাণিজ্যিক মালামাল পরিবহন সেবা।", "Commercial goods transportation by road and waterway.",
 hero("hero/cargo-ship-port.jpg", "বন্দরে বাণিজ্যিক কার্গো জাহাজ", "Commercial cargo ship at a seaport", b("মেসার্স ঝিমীক ট্রান্সপোর্ট এজেন্সি", "M/s Jhimik Transport Agency"), b("সড়ক ও নৌপথে বাণিজ্যিক মালামাল পরিবহন সেবা।", "Transportation of commercial goods through road and waterway networks."), f'<div class="cta">{btn("/contact/", "পরিবহন জিজ্ঞাসা", "Transport Enquiry")}</div>', crumb(b("ঝিমীক ট্রান্সপোর্ট", "Jhimik Transport")), True) +
 f'<section class="road"><div class="wrap">{head("সড়ক", "Road", "সড়ক পরিবহন", "Road Transportation")}<p>{b("ভারী পণ্যবাহী ট্রাকের মাধ্যমে বাণিজ্যিক মালামাল পরিবহন।", "Commercial goods carried by heavy-duty cargo trucks.")}</p><div class="trio">{pic("transport/truck-freight.jpg", "পণ্যবাহী ট্রাক", "Freight truck")}{pic("transport/truck-loading.jpg", "ট্রাকে মাল বোঝাই", "Loading cargo onto a truck")}</div></div></section>'
 f'<section class="water"><div class="wrap">{head("নৌপথ", "Waterway", "নৌপথ পরিবহন", "Waterway Transportation")}<p>{b("নদী ও নৌপথে কার্গো ভেসেলের মাধ্যমে মালামাল পরিবহন।", "Goods moved by cargo vessel along rivers and waterways.")}</p><div class="trio">{pic("transport/cargo-vessel.jpg", "কার্গো ভেসেল", "Cargo vessel")}{pic("transport/river-port.jpg", "নদীবন্দর", "River port")}</div></div></section>'
 f'<section><div class="wrap"><p class="note">{b("বহরের আকার, রুট ও সময়সূচির তথ্য যাচাই সাপেক্ষে পরে যুক্ত হবে। বিস্তারিত জানতে কল করুন।", "Fleet, route and schedule details will be added once verified. Please call for specifics.")}</p></div></section>' + band())

GAL = [("hero/cargo-ship-port.jpg", "কার্গো জাহাজ", "Cargo ship"), ("hero/port-operations.jpg", "বাণিজ্যিক বন্দর", "Commercial port"), ("transport/truck-freight.jpg", "ট্রাক", "Truck"), ("transport/truck-loading.jpg", "সড়ক পরিবহন", "Road transportation"), ("transport/cargo-vessel.jpg", "নৌপথ পরিবহন", "Waterway transportation"), ("transport/river-port.jpg", "নদীবন্দর", "River port"), ("nabi-enterprises/warehouse.jpg", "গুদাম", "Warehouse"), ("about/industrial-supply.jpg", "শিল্প সরবরাহ", "Industrial supply")] + [(f"products/{s}.jpg", bn, en) for s, bn, en, _, _ in PRODUCTS]
PAGES["gallery/index.html"] = layout("/gallery/", "gallery", "গ্যালারি | " + NAME[0], "Gallery | Nabi Enterprises & Jhimik Transport Agency",
 "জাহাজ, ট্রাক, বন্দর ও পণ্যের ছবির গ্যালারি।", "Gallery of ships, trucks, ports and products.",
 hero("hero/port-operations.jpg", "বন্দরে কার্গো কার্যক্রম", "Cargo operations at a port", b("গ্যালারি", "Gallery"), b("পণ্য ও পরিবহনের ছবি।", "Photographs of our products and transport."), "", crumb(b("গ্যালারি", "Gallery")), True) +
 '<section><div class="wrap"><div class="gal">' + "".join(f'<button type="button" class="gi" data-src="/assets/images/{p}" data-bn="{esc(bn)}" data-en="{esc(en)}" aria-label="{esc(bn)}">{pic(p, bn, en)}</button>' for p, bn, en in GAL) + '</div></div></section>')

PAGES["contact/index.html"] = layout("/contact/", "contact", "যোগাযোগ | " + NAME[0], "Contact Us | Nabi Enterprises & Jhimik Transport Agency",
 "ঠিকানা: " + ADDR[0] + "। ফোন: " + ", ".join(PHONES), "Address: " + ADDR[1] + ". Phone: " + ", ".join(PHONES),
 hero("hero/cargo-ship-port.jpg", "বন্দরে বাণিজ্যিক কার্গো জাহাজ", "Commercial cargo ship at a seaport", b("যোগাযোগ", "Contact Us"), b("ব্যবসায়িক ও পরিবহন বিষয়ক জিজ্ঞাসার জন্য যোগাযোগ করুন।", "Contact us for business and transportation enquiries."), "", crumb(b("যোগাযোগ", "Contact Us")), True) +
 f'''<section><div class="wrap two top"><div class="ci">
<div><b>{b("প্রতিষ্ঠান", "Businesses")}</b>{b("মেসার্স নবী এন্টারপ্রাইজ", "M/s Nabi Enterprises")}<br>{b("মেসার্স ঝিমীক ট্রান্সপোর্ট এজেন্সি", "M/s Jhimik Transport Agency")}</div>
<div><b>{b("প্রোপ্রাইটর", "Proprietor")}</b>{b("মোঃ মিলন মোল্লা", "Md. Milon Molla")}</div>
<div><b>{b("ঠিকানা", "Address")}</b>{b(*ADDR)}</div>
<div><b>{b("ফোন", "Phone")}</b>{tel(PHONES[0])} · {tel(PHONES[1])}<br>{b("অফিস: ", "Office: ")}{tel(PHONES[2])}</div>
<div><b>{b("মানচিত্র", "Map")}</b>{b("যাচাইকৃত স্থানাঙ্ক না থাকায় মানচিত্র যুক্ত করা হয়নি।", "Not shown: no verified coordinates are available.")}</div></div>
<form id="enq" novalidate><label>{b("নাম", "Name")}<input name="name" required autocomplete="name"></label>
<label>{b("ফোন নম্বর", "Phone")}<input name="phone" type="tel" required autocomplete="tel"></label>
<label>{b("ইমেইল", "Email")}<input name="email" type="email" autocomplete="email"></label>
<label>{b("বিষয়", "Subject")}<input name="subject"></label>
<label>{b("বার্তা", "Message")}<textarea name="msg" rows="5" required></textarea></label>
<button class="btn gold" type="submit">{b("জমা দিন", "Submit")}</button>
<div class="note" id="enq-note" role="status" hidden data-bn="এই ফর্মটি এখনও কোনো সার্ভার বা ইমেইল সেবার সাথে যুক্ত নয়; আপনার বার্তা পাঠানো হয়নি। অনুগ্রহ করে ফোনে যোগাযোগ করুন।" data-en="This form is not yet connected to a server or email service; your message was NOT sent. Please contact us by phone."></div></form></div></section>''')

PAGES["404.html"] = layout("/404.html", "", "পাতা পাওয়া যায়নি", "Page not found", "পাতা পাওয়া যায়নি।", "Page not found.",
 f'<section><div class="wrap"><h1>{b("পাতা পাওয়া যায়নি", "Page not found")}</h1><p class="mt">{btn("/", "হোমে ফিরুন", "Back to Home")}</p></div></section>')

CSS = open("style.css", encoding="utf-8").read(); JS = open("main.js", encoding="utf-8").read()
LOGO = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="64" height="64" role="img" aria-label="Nabi &amp; Jhimik"><rect x="1.5" y="1.5" width="61" height="61" fill="#071D38" stroke="#D6A84B" stroke-width="2.5"/><path d="M14 48V16l14 22V16M50 16v24c0 6-4 8-8 8s-6-2-8-4" fill="none" stroke="#fff" stroke-width="4.5" stroke-linejoin="round"/><path d="M8 54q6-5 12 0t12 0 12 0 12 0" fill="none" stroke="#D6A84B" stroke-width="2.5"/></svg>'''
LOGO_LIGHT = LOGO.replace('fill="#071D38" stroke="#D6A84B"', 'fill="#fff" stroke="#D6A84B"').replace('stroke="#fff"', 'stroke="#071D38"')
HORIZ = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 330 64" role="img" aria-label="Nabi &amp; Jhimik"><g>''' + LOGO.split(">", 1)[1].rsplit("</svg>", 1)[0] + '''</g><text x="78" y="32" font-family="Montserrat,Arial,sans-serif" font-weight="700" font-size="22" letter-spacing="2" fill="#071D38">NABI &amp; JHIMIK</text><text x="78" y="52" font-family="Montserrat,Arial,sans-serif" font-weight="500" font-size="10.5" letter-spacing="3.2" fill="#D6A84B">ENTERPRISES &amp; TRANSPORT</text></svg>'''

if os.path.isdir(OUT): shutil.rmtree(OUT)
def w(path, data):
    p = os.path.join(OUT, path); os.makedirs(os.path.dirname(p) or OUT, exist_ok=True); open(p, "w", encoding="utf-8").write(data)
for p, d in PAGES.items(): w(p, d)
w("css/style.css", CSS); w("js/main.js", JS)
w("assets/logo-mark.svg", LOGO); w("assets/logo-mark-light.svg", LOGO_LIGHT); w("assets/logo-horizontal.svg", HORIZ)
for p in IMGS: os.makedirs(os.path.join(OUT, "assets/images", os.path.dirname(p)), exist_ok=True)
manifest = ["# Required photographs (not yet included)\n", "Save each file at the path shown, landscape, about 1600px wide, JPEG under ~300 KB. Licensed sources: Unsplash, Pexels, Pixabay. Record the photographer and licence in `CREDITS.md`.\n\n| File (under assets/images/) | Subject |\n|---|---|"]
manifest += [f"| `{p}` | {en} |" for p, (bn, en) in sorted(IMGS.items())]
w("assets/images/MANIFEST.md", "\n".join(manifest) + "\n")
print(len(PAGES), "pages;", len(IMGS), "image slots")
