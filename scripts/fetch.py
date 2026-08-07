#!/usr/bin/env python3
"""
Ponte dati per il Modulo C (processo_precedenti.md) — v3.

Esito del run del 07/08/2026: FRED va in ReadTimeout dai runner GitHub
(blocco silenzioso degli indirizzi da data center). French funziona.
Shiller falliva per un difetto mio: il sito e' generato via JavaScript e
nell'HTML grezzo il link ha le barre protette (https:\\/\\/...).

Questa versione: (1) sonda piu' fonti alternative per la macro, DBnomics
in testa, e usa la prima che risponde; (2) estrae il link di Shiller in
modo tollerante; (3) resta diagnostica — stampa tutto mentre procede.
"""
import io
import os
import re
import sys
import time
import json
import zipfile
import datetime as dt

import requests
import pandas as pd

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")
os.makedirs(OUT, exist_ok=True)
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                    "(KHTML, like Gecko) Chrome/126.0 Safari/537.36"}
T = (10, 25)
LOG = []

# La chiave FRED arriva dai secret del repository, mai dal codice.
FRED_KEY = os.environ.get("FRED_API_KEY", "").strip()


def say(m):
    print(m, flush=True)
    LOG.append(m)


SERIE = {
    "UNRATE": 1, "CIVPART": 1, "PAYEMS": 1, "ICSA": 1, "CCSA": 1,
    "GDPC1": 2, "INDPRO": 2, "PNFI": 2, "NEWORDER": 2,
    "CPIAUCSL": 3, "CPILFESL": 3, "PCEPILFE": 3, "PCEPI": 3,
    "FEDFUNDS": 4, "TB3MS": 4, "GS1": 4, "GS2": 4, "GS10": 4,
    "T10Y3M": 4, "T10Y2Y": 4,
    "SP500": 5, "CP": 6, "CPATAX": 6,
    "AAA": 7, "BAA": 7, "BAA10Y": 7, "BUSLOANS": 7, "TOTBKCR": 7,
    "BAMLH0A0HYM2": 7, "DRSFRMACBS": 7,
    "GFDEGDQ188S": 8, "NETEXP": 8, "DTWEXBGS": 8,
    "JTSJOL": 91, "JTSQUR": 91, "VIXCLS": 91, "DRTSCILM": 91,
    "CSUSHPINSA": 91, "MORTGAGE30US": 91, "UMCSENT": 91, "NFCI": 91,
}

# ==========================================================================
# 1. SONDAGGIO DELLE FONTI MACRO
# ==========================================================================
say("=" * 72)
say("SONDAGGIO FONTI MACRO — quale risponde da questo runner?")
say("=" * 72)


def prova(nome, url, controllo):
    t0 = time.time()
    try:
        r = requests.get(url, headers=UA, timeout=T)
        el = time.time() - t0
        esito = controllo(r)
        say("  %-22s HTTP %-4s %5.1fs %8d byte  %s"
            % (nome, r.status_code, el, len(r.content), esito))
        # nota: si stampa il NOME della fonte, mai l'URL: conterrebbe la chiave
        return esito == "UTILIZZABILE"
    except Exception as e:
        say("  %-22s FALLITO dopo %5.1fs  %s"
            % (nome, time.time() - t0, type(e).__name__))
        return False


def c_csv(r):
    return "UTILIZZABILE" if (r.status_code == 200 and b"DATE" in r.content[:200].upper()) else "formato inatteso"


def c_fredapi(r):
    try:
        n = len(r.json().get("observations", []))
        return "UTILIZZABILE" if n else "nessuna osservazione"
    except Exception:
        return "non e' JSON"


def c_json(r):
    try:
        d = r.json()
        n = len(d.get("series", {}).get("docs", []))
        return "UTILIZZABILE" if n else "nessuna serie nella risposta"
    except Exception:
        return "non e' JSON"


FONTI = []
if FRED_KEY:
    FONTI.append(("FRED API ufficiale",
                  "https://api.stlouisfed.org/fred/series/observations"
                  "?series_id=UNRATE&file_type=json&api_key=" + FRED_KEY,
                  c_fredapi))
else:
    say("  (nessuna chiave FRED nei secret: salto l'API ufficiale)")

FONTI += [
    ("FRED fredgraph", "https://fred.stlouisfed.org/graph/fredgraph.csv?id=UNRATE", c_csv),
    ("DBnomics v22", "https://api.db.nomics.world/v22/series/FRED/UNRATE?observations=1", c_json),
    ("DBnomics search", "https://api.db.nomics.world/v22/search?q=UNRATE&limit=1", c_json),
]

VIA = None
for nome, url, ctrl in FONTI:
    if prova(nome, url, ctrl) and VIA is None:
        VIA = nome
    time.sleep(1)

say("")
if VIA:
    say("  --> fonte macro scelta: %s" % VIA)
else:
    say("  !! NESSUNA FONTE MACRO RISPONDE.")
    say("  !! Il prelievo macro da GitHub Actions non e' percorribile.")
    say("  !! Ripiego obbligato: eseguire questo script dal computer di casa.")

# ==========================================================================
# 2. PRELIEVO MACRO
# ==========================================================================
frames = []


def da_fred(sid):
    r = requests.get("https://fred.stlouisfed.org/graph/fredgraph.csv?id=" + sid,
                     headers=UA, timeout=T)
    r.raise_for_status()
    d = pd.read_csv(io.StringIO(r.text))
    d.columns = ["date", "value"]
    return d


def da_fredapi(sid):
    r = requests.get("https://api.stlouisfed.org/fred/series/observations",
                     params={"series_id": sid, "file_type": "json",
                             "api_key": FRED_KEY},
                     headers=UA, timeout=T)
    r.raise_for_status()
    o = r.json()["observations"]
    if not o:
        raise RuntimeError("nessuna osservazione")
    return pd.DataFrame({"date": [x["date"] for x in o],
                         "value": [x["value"] for x in o]})


def da_dbnomics(sid):
    r = requests.get("https://api.db.nomics.world/v22/series/FRED/%s?observations=1" % sid,
                     headers=UA, timeout=T)
    r.raise_for_status()
    docs = r.json()["series"]["docs"]
    if not docs:
        raise RuntimeError("serie assente su DBnomics")
    doc = docs[0]
    return pd.DataFrame({"date": doc["period"], "value": doc["value"]})


PRELIEVO = {"FRED API ufficiale": da_fredapi,
            "FRED fredgraph": da_fred,
            "DBnomics v22": da_dbnomics,
            "DBnomics search": da_dbnomics}

if VIA:
    fn = PRELIEVO[VIA]
    say("")
    say("=" * 72)
    say("PRELIEVO MACRO — %d serie via %s" % (len(SERIE), VIA))
    say("=" * 72)
    ko = 0
    for i, (sid, blocco) in enumerate(SERIE.items(), 1):
        t0 = time.time()
        try:
            d = fn(sid)
            d["date"] = pd.to_datetime(d["date"], errors="coerce")
            d["value"] = pd.to_numeric(d["value"], errors="coerce")
            d = d.dropna(subset=["date"])
            d["serie"], d["blocco"] = sid, blocco
            frames.append(d[["serie", "blocco", "date", "value"]])
            say("[%2d/%d] OK      %-18s %6d oss.  %s -> %s  (%.1fs)"
                % (i, len(SERIE), sid, len(d), d.date.min().date(),
                   d.date.max().date(), time.time() - t0))
            ko = 0
        except Exception as e:
            say("[%2d/%d] FALLITA %-18s %s  (%.1fs)"
                % (i, len(SERIE), sid, type(e).__name__, time.time() - t0))
            ko += 1
            if ko >= 5:
                say("\n  !! 5 fallimenti consecutivi: interrompo il prelievo macro.")
                break
        time.sleep(0.3)

if frames:
    allf = pd.concat(frames, ignore_index=True)
    allf.to_csv(os.path.join(OUT, "macro_serie.csv"), index=False)
    (allf.groupby("serie")
     .agg(blocco=("blocco", "first"), inizio=("date", "min"),
          fine=("date", "max"), n=("value", "size"))
     .reset_index()
     .to_csv(os.path.join(OUT, "macro_copertura.csv"), index=False))
    say("\n  scritte %d serie in data/macro_serie.csv" % allf.serie.nunique())

# ==========================================================================
# 3. SHILLER — estrazione tollerante del link
# ==========================================================================
say("")
say("=" * 72)
say("SHILLER")
say("=" * 72)
try:
    t0 = time.time()
    p = requests.get("https://shillerdata.com/", headers=UA, timeout=T)
    p.raise_for_status()
    testo = p.text.replace("\\/", "/").replace("&amp;", "&")
    cand = re.findall(r"https?://[^\s\"'<>\\]*ie_data[^\s\"'<>\\]*\.xls[^\s\"'<>\\]*", testo)
    cand += re.findall(r"https?://[^\s\"'<>\\]*blobby[^\s\"'<>\\]*\.xls[^\s\"'<>\\]*", testo)
    say("  candidati trovati nella pagina: %d" % len(cand))

    # La pagina e' resa via JavaScript: nell'HTML grezzo il link puo' mancare.
    # Indirizzi noti, provati in coda a quelli eventualmente trovati.
    # Se il file venisse spostato, questi falliscono e il manifest lo dichiara:
    # nessun dato viene mai inventato.
    NOTI = [
        "https://img1.wsimg.com/blobby/go/e5e77e0b-59d1-44d9-ab25-4763ac982e53/"
        "downloads/e27e58c1-8ae0-488c-a976-a298708c7175/ie_data.xls",
        "http://www.econ.yale.edu/~shiller/data/ie_data.xls",
        "https://raw.githubusercontent.com/datasets/s-and-p-500/main/data/data.csv",
    ]
    cand = list(dict.fromkeys(list(cand) + NOTI))
    say("  candidati totali da provare: %d" % len(cand))
    if not cand:
        raise RuntimeError("nessun candidato disponibile")
    ultimo = None
    for src in dict.fromkeys(cand):
        try:
            x = requests.get(src, headers=UA, timeout=(10, 90))
            x.raise_for_status()
            if src.lower().endswith(".csv"):
                sh = pd.read_csv(io.BytesIO(x.content))
                sh.to_csv(os.path.join(OUT, "shiller_ie_data.csv"), index=False)
                say("  OK      shiller (RIPIEGO CSV) %6d righe  (%.1fs)  %s"
                    % (len(sh), time.time() - t0, src[:60]))
                say("  ATTENZIONE: ripiego GitHub — utili e CAPE si fermano a meta' 2023.")
                ultimo = None
                break
            xl = pd.ExcelFile(io.BytesIO(x.content))
            sh_name = next((s for s in xl.sheet_names if s.strip().lower() == "data"),
                           xl.sheet_names[0])
            raw = xl.parse(sh_name, header=None)
            hdr = next(i for i in range(min(25, len(raw)))
                       if str(raw.iloc[i, 0]).strip().lower().startswith("date"))
            sh = xl.parse(sh_name, skiprows=hdr)
            sh = sh[pd.to_numeric(sh.iloc[:, 0], errors="coerce").notna()]
            sh.to_csv(os.path.join(OUT, "shiller_ie_data.csv"), index=False)
            say("  OK      shiller ie_data    %6d righe  (%.1fs)  %s"
                % (len(sh), time.time() - t0, src[:60]))
            ultimo = None
            break
        except Exception as e:
            ultimo = e
    if ultimo:
        raise ultimo
except Exception as e:
    say("  FALLITA shiller            %s: %s" % (type(e).__name__, str(e)[:100]))

# ==========================================================================
# 4. KEN FRENCH — settori (gia' funzionante)
# ==========================================================================
say("")
say("=" * 72)
say("KEN FRENCH")
say("=" * 72)
try:
    t0 = time.time()
    u = ("https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/"
         "12_Industry_Portfolios_CSV.zip")
    z = zipfile.ZipFile(io.BytesIO(requests.get(u, headers=UA, timeout=(10, 90)).content))
    with z.open(z.namelist()[0]) as fh:
        txt = fh.read().decode("latin-1")
    with open(os.path.join(OUT, "french_12_industry.txt"), "w") as f:
        f.write(txt)
    say("  OK      french 12 industry %6d righe  (%.1fs)"
        % (len(txt.splitlines()), time.time() - t0))
except Exception as e:
    say("  FALLITA french             %s: %s" % (type(e).__name__, str(e)[:100]))

# ==========================================================================
# 5. MANIFEST
# ==========================================================================
stamp = dt.datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
ok = sum(1 for l in LOG if " OK " in l)
kk = sum(1 for l in LOG if "FALLITA" in l or "FALLITO" in l)
with open(os.path.join(OUT, "MANIFEST.md"), "w") as f:
    f.write("# Manifest del ponte dati\n\nAggiornamento: **%s**\n\n" % stamp)
    f.write("Fonte macro: **%s**\n\n" % (VIA or "NESSUNA — prelievo macro non riuscito"))
    f.write("Riuscite: %d · Fallite: %d\n\n" % (ok, kk))
    f.write("Una serie FALLITA e' un dato ASSENTE: non va imputato, non va "
            "sostituito con un proxy, va dichiarato assente nel run.\n\n```\n")
    f.write("\n".join(LOG))
    f.write("\n```\n")

say("")
say("TOTALE: %d riuscite, %d fallite" % (ok, kk))
sys.exit(0)
