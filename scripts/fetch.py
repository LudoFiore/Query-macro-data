#!/usr/bin/env python3
"""
Ponte dati per il Modulo C (processo_precedenti.md).

Gira su GitHub Actions, dove la rete non e' ristretta, e deposita CSV in data/
che l'ambiente di analisi legge via raw.githubusercontent.com.

Nessuna API key necessaria: FRED espone i CSV pubblici via fredgraph.
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
UA = {"User-Agent": "Mozilla/5.0 (ponte-dati-macro)"}
LOG = []

# --------------------------------------------------------------------- FRED
# Serie del NUCLEO e del SECONDO STRATO della SOP, col blocco di appartenenza.
# Blocchi 1-8 = nucleo. Blocco 91 = secondo strato (storia corta).
SERIE = {
    # 1 - lavoro
    "UNRATE": 1, "CIVPART": 1, "PAYEMS": 1, "ICSA": 1, "CCSA": 1,
    # 2 - attivita' reale
    "GDPC1": 2, "INDPRO": 2, "PNFI": 2, "NEWORDER": 2, "A191RL1Q225SBEA": 2,
    # 3 - prezzi
    "CPIAUCSL": 3, "CPILFESL": 3, "PCEPILFE": 3, "PCEPI": 3,
    # 4 - politica monetaria e tassi
    "FEDFUNDS": 4, "TB3MS": 4, "GS1": 4, "GS2": 4, "GS10": 4,
    "T10Y3M": 4, "T10Y2Y": 4, "REAINTRATREARAT10Y": 4,
    # 5/6 - valutazione e utili (complemento a Shiller)
    "SP500": 5, "CP": 6, "CPATAX": 6,
    # 7 - credito
    "AAA": 7, "BAA": 7, "BAA10Y": 7, "BUSLOANS": 7, "TOTBKCR": 7,
    "BAMLH0A0HYM2": 7, "DRSFRMACBS": 7,
    # 8 - fiscale ed esterno
    "FYFSGDA188S": 8, "GFDEGDQ188S": 8, "NETEXP": 8,
    "DTWEXBGS": 8, "TWEXBGSMTH": 8,
    # 91 - secondo strato
    "JTSJOL": 91, "JTSQUR": 91, "VIXCLS": 91, "DRTSCILM": 91,
    "CSUSHPINSA": 91, "MORTGAGE30US": 91, "UMCSENT": 91, "NFCI": 91,
}


def fred(sid):
    url = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=" + sid
    r = requests.get(url, headers=UA, timeout=60)
    r.raise_for_status()
    df = pd.read_csv(io.StringIO(r.text))
    df.columns = ["date", "value"]
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["value"] = pd.to_numeric(df["value"], errors="coerce")
    return df.dropna(subset=["date"])


frames = []
for sid, blocco in SERIE.items():
    try:
        d = fred(sid)
        d["serie"] = sid
        d["blocco"] = blocco
        frames.append(d)
        LOG.append("OK      %-20s %6d oss.  %s -> %s"
                   % (sid, len(d), d.date.min().date(), d.date.max().date()))
    except Exception as e:
        LOG.append("FALLITA %-20s %s: %s" % (sid, type(e).__name__, e))
    time.sleep(0.6)

if frames:
    allf = pd.concat(frames, ignore_index=True)[["serie", "blocco", "date", "value"]]
    allf.to_csv(os.path.join(OUT, "fred_serie.csv"), index=False)
    cop = (allf.groupby("serie")
           .agg(blocco=("blocco", "first"), inizio=("date", "min"),
                fine=("date", "max"), n=("value", "size"))
           .reset_index())
    cop.to_csv(os.path.join(OUT, "fred_copertura.csv"), index=False)

# ------------------------------------------------------------------ SHILLER
# Il link a ie_data.xls porta un ?ver= che cambia: si legge dalla pagina.
def shiller():
    p = requests.get("https://shillerdata.com/", headers=UA, timeout=60)
    p.raise_for_status()
    m = re.findall(r"https://[^\"']*ie_data\.xls[^\"']*", p.text)
    if not m:
        raise RuntimeError("link ie_data.xls non trovato nella pagina")
    src = m[0].replace("&amp;", "&")
    x = requests.get(src, headers=UA, timeout=120)
    x.raise_for_status()
    xl = pd.ExcelFile(io.BytesIO(x.content))
    sheet = next((s for s in xl.sheet_names if s.strip().lower() == "data"),
                 xl.sheet_names[0])
    raw = xl.parse(sheet, header=None)
    hdr = next(i for i in range(min(20, len(raw)))
               if str(raw.iloc[i, 0]).strip().lower().startswith("date"))
    df = xl.parse(sheet, skiprows=hdr)
    df = df[pd.to_numeric(df.iloc[:, 0], errors="coerce").notna()]
    return df, src


try:
    sh, src = shiller()
    sh.to_csv(os.path.join(OUT, "shiller_ie_data.csv"), index=False)
    LOG.append("OK      %-20s %6d righe  fonte: %s" % ("shiller_ie_data", len(sh), src[:70]))
except Exception as e:
    LOG.append("FALLITA %-20s %s: %s" % ("shiller_ie_data", type(e).__name__, e))

# -------------------------------------------------------- KEN FRENCH settori
try:
    u = ("https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/"
         "12_Industry_Portfolios_CSV.zip")
    z = zipfile.ZipFile(io.BytesIO(requests.get(u, headers=UA, timeout=120).content))
    with z.open(z.namelist()[0]) as fh:
        txt = fh.read().decode("latin-1")
    with open(os.path.join(OUT, "french_12_industry.txt"), "w") as f:
        f.write(txt)
    LOG.append("OK      %-20s %6d righe" % ("french_12_industry", len(txt.splitlines())))
except Exception as e:
    LOG.append("FALLITA %-20s %s: %s" % ("french_12_industry", type(e).__name__, e))

# ---------------------------------------------------------------------- LOG
stamp = dt.datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
ok = sum(1 for l in LOG if l.startswith("OK"))
ko = sum(1 for l in LOG if l.startswith("FALLITA"))
with open(os.path.join(OUT, "MANIFEST.md"), "w") as f:
    f.write("# Manifest del ponte dati\n\nAggiornamento: **%s**\n\n" % stamp)
    f.write("Riuscite: %d · Fallite: %d\n\n" % (ok, ko))
    f.write("Ogni riga sotto e' l'esito verificato del prelievo. Una serie FALLITA "
            "e' un dato ASSENTE: non va imputato, non va sostituito con un proxy, "
            "va dichiarato assente nel run.\n\n```\n")
    f.write("\n".join(LOG))
    f.write("\n```\n")

print("\n".join(LOG))
print("\n%d riuscite, %d fallite" % (ok, ko))
sys.exit(0 if ok else 1)
