#!/usr/bin/env python3
"""
Ponte dati per il Modulo C (processo_precedenti.md) — v2, diagnostica.

Differenze dalla v1: stampa ogni esito SUBITO, timeout brevi, un solo
ritentativo, e un test preliminare che abortisce in fretta se la fonte
non risponde affatto. Meglio fallire in un minuto sapendo perche', che
restare appesi mezz'ora senza sapere nulla.
"""
import io
import os
import re
import sys
import time
import zipfile
import datetime as dt

import requests
import pandas as pd

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")
os.makedirs(OUT, exist_ok=True)
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                    "(KHTML, like Gecko) Chrome/126.0 Safari/537.36"}
TIMEOUT = (10, 25)          # (connessione, lettura) — corti di proposito
LOG = []


def say(msg):
    """Stampa subito: senza flush il log di Actions resta muto fino alla fine."""
    print(msg, flush=True)
    LOG.append(msg)


# --------------------------------------------------------- TEST PRELIMINARE
say("=" * 70)
say("TEST PRELIMINARE — la fonte risponde?")
say("=" * 70)

CANDIDATI = [
    ("fredgraph CSV", "https://fred.stlouisfed.org/graph/fredgraph.csv?id=UNRATE"),
    ("fred data txt", "https://fred.stlouisfed.org/data/UNRATE.txt"),
]
VIA = None
for nome, url in CANDIDATI:
    t0 = time.time()
    try:
        r = requests.get(url, headers=UA, timeout=TIMEOUT)
        say("  %-16s HTTP %s  %5.1fs  %8d byte"
            % (nome, r.status_code, time.time() - t0, len(r.content)))
        if r.status_code == 200 and len(r.content) > 500 and VIA is None:
            VIA = (nome, url)
    except Exception as e:
        say("  %-16s FALLITO dopo %5.1fs  %s"
            % (nome, time.time() - t0, type(e).__name__))

if VIA is None:
    say("")
    say("!! NESSUN CANALE FRED RISPONDE DA QUESTO RUNNER.")
    say("!! Il ponte via GitHub Actions non e' percorribile per FRED.")
    say("!! Proseguo comunque con Shiller e French, per sapere cosa funziona.")
else:
    say("")
    say("  --> canale utilizzabile: %s" % VIA[0])

# ------------------------------------------------------------------- SERIE
SERIE = {
    "UNRATE": 1, "CIVPART": 1, "PAYEMS": 1, "ICSA": 1, "CCSA": 1,
    "GDPC1": 2, "INDPRO": 2, "PNFI": 2, "NEWORDER": 2, "A191RL1Q225SBEA": 2,
    "CPIAUCSL": 3, "CPILFESL": 3, "PCEPILFE": 3, "PCEPI": 3,
    "FEDFUNDS": 4, "TB3MS": 4, "GS1": 4, "GS2": 4, "GS10": 4,
    "T10Y3M": 4, "T10Y2Y": 4, "REAINTRATREARAT10Y": 4,
    "SP500": 5, "CP": 6, "CPATAX": 6,
    "AAA": 7, "BAA": 7, "BAA10Y": 7, "BUSLOANS": 7, "TOTBKCR": 7,
    "BAMLH0A0HYM2": 7, "DRSFRMACBS": 7,
    "FYFSGDA188S": 8, "GFDEGDQ188S": 8, "NETEXP": 8,
    "DTWEXBGS": 8, "TWEXBGSMTH": 8,
    "JTSJOL": 91, "JTSQUR": 91, "VIXCLS": 91, "DRTSCILM": 91,
    "CSUSHPINSA": 91, "MORTGAGE30US": 91, "UMCSENT": 91, "NFCI": 91,
}


def fred(sid):
    url = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=" + sid
    r = requests.get(url, headers=UA, timeout=TIMEOUT)
    r.raise_for_status()
    df = pd.read_csv(io.StringIO(r.text))
    df.columns = ["date", "value"]
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["value"] = pd.to_numeric(df["value"], errors="coerce")
    return df.dropna(subset=["date"])


frames = []
if VIA is not None:
    say("")
    say("=" * 70)
    say("PRELIEVO — %d serie" % len(SERIE))
    say("=" * 70)
    ko_consecutivi = 0
    for i, (sid, blocco) in enumerate(SERIE.items(), 1):
        riuscita = False
        for tentativo in (1, 2):
            t0 = time.time()
            try:
                d = fred(sid)
                d["serie"], d["blocco"] = sid, blocco
                frames.append(d)
                say("[%2d/%d] OK      %-20s %6d oss.  %s -> %s  (%.1fs)"
                    % (i, len(SERIE), sid, len(d), d.date.min().date(),
                       d.date.max().date(), time.time() - t0))
                riuscita = True
                ko_consecutivi = 0
                break
            except Exception as e:
                if tentativo == 2:
                    say("[%2d/%d] FALLITA %-20s %s dopo %.1fs"
                        % (i, len(SERIE), sid, type(e).__name__, time.time() - t0))
                else:
                    time.sleep(2)
        if not riuscita:
            ko_consecutivi += 1
            if ko_consecutivi >= 5:
                say("")
                say("!! 5 fallimenti consecutivi: interrompo il prelievo FRED.")
                break
        time.sleep(0.2)

if frames:
    allf = pd.concat(frames, ignore_index=True)[["serie", "blocco", "date", "value"]]
    allf.to_csv(os.path.join(OUT, "fred_serie.csv"), index=False)
    (allf.groupby("serie")
     .agg(blocco=("blocco", "first"), inizio=("date", "min"),
          fine=("date", "max"), n=("value", "size"))
     .reset_index()
     .to_csv(os.path.join(OUT, "fred_copertura.csv"), index=False))
    say("")
    say("  scritte %d serie in data/fred_serie.csv" % allf.serie.nunique())

# ----------------------------------------------------------------- SHILLER
say("")
say("=" * 70)
say("SHILLER e FRENCH")
say("=" * 70)
try:
    t0 = time.time()
    p = requests.get("https://shillerdata.com/", headers=UA, timeout=TIMEOUT)
    p.raise_for_status()
    m = re.findall(r"https://[^\"']*ie_data\.xls[^\"']*", p.text)
    if not m:
        raise RuntimeError("link ie_data.xls non trovato nella pagina")
    src = m[0].replace("&amp;", "&")
    x = requests.get(src, headers=UA, timeout=(10, 90))
    x.raise_for_status()
    xl = pd.ExcelFile(io.BytesIO(x.content))
    sheet = next((s for s in xl.sheet_names if s.strip().lower() == "data"),
                 xl.sheet_names[0])
    raw = xl.parse(sheet, header=None)
    hdr = next(i for i in range(min(20, len(raw)))
               if str(raw.iloc[i, 0]).strip().lower().startswith("date"))
    sh = xl.parse(sheet, skiprows=hdr)
    sh = sh[pd.to_numeric(sh.iloc[:, 0], errors="coerce").notna()]
    sh.to_csv(os.path.join(OUT, "shiller_ie_data.csv"), index=False)
    say("  OK      shiller ie_data      %6d righe  (%.1fs)" % (len(sh), time.time() - t0))
except Exception as e:
    say("  FALLITA shiller              %s: %s" % (type(e).__name__, str(e)[:90]))

try:
    t0 = time.time()
    u = ("https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/"
         "12_Industry_Portfolios_CSV.zip")
    z = zipfile.ZipFile(io.BytesIO(requests.get(u, headers=UA, timeout=(10, 90)).content))
    with z.open(z.namelist()[0]) as fh:
        txt = fh.read().decode("latin-1")
    with open(os.path.join(OUT, "french_12_industry.txt"), "w") as f:
        f.write(txt)
    say("  OK      french 12 industry   %6d righe  (%.1fs)"
        % (len(txt.splitlines()), time.time() - t0))
except Exception as e:
    say("  FALLITA french               %s: %s" % (type(e).__name__, str(e)[:90]))

# ---------------------------------------------------------------- MANIFEST
stamp = dt.datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
ok = sum(1 for l in LOG if " OK " in l)
ko = sum(1 for l in LOG if "FALLITA" in l)
with open(os.path.join(OUT, "MANIFEST.md"), "w") as f:
    f.write("# Manifest del ponte dati\n\nAggiornamento: **%s**\n\n" % stamp)
    f.write("Riuscite: %d · Fallite: %d\n\n" % (ok, ko))
    f.write("Una serie FALLITA e' un dato ASSENTE: non va imputato, non va "
            "sostituito con un proxy, va dichiarato assente nel run.\n\n```\n")
    f.write("\n".join(LOG))
    f.write("\n```\n")

say("")
say("TOTALE: %d riuscite, %d fallite" % (ok, ko))
sys.exit(0)
