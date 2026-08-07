# Manifest del ponte dati

Aggiornamento: **2026-08-07 13:50 UTC**

Riuscite: 1 · Fallite: 1

Una serie FALLITA e' un dato ASSENTE: non va imputato, non va sostituito con un proxy, va dichiarato assente nel run.

```
======================================================================
TEST PRELIMINARE — la fonte risponde?
======================================================================
  fredgraph CSV    FALLITO dopo  25.1s  ReadTimeout
  fred data txt    FALLITO dopo  25.0s  ReadTimeout

!! NESSUN CANALE FRED RISPONDE DA QUESTO RUNNER.
!! Il ponte via GitHub Actions non e' percorribile per FRED.
!! Proseguo comunque con Shiller e French, per sapere cosa funziona.

======================================================================
SHILLER e FRENCH
======================================================================
  FALLITA shiller              RuntimeError: link ie_data.xls non trovato nella pagina
  OK      french 12 industry     5240 righe  (0.9s)
```
