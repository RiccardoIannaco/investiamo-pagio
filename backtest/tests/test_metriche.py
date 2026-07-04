import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

import pandas as pd
import pytest

from metriche import (
    cagr,
    max_drawdown,
    peggior_anno,
    simula_portafoglio,
    volatilita_annualizzata,
)


def serie_mensile(valori, inizio="2020-01-31"):
    idx = pd.date_range(inizio, periods=len(valori), freq="ME")
    return pd.Series([float(v) for v in valori], index=idx)


def test_cagr_crescita_costante_1pc_al_mese():
    s = serie_mensile([100 * 1.01**i for i in range(25)])
    assert cagr(s) == pytest.approx(1.01**12 - 1)


def test_volatilita_serie_costante_e_zero():
    s = serie_mensile([100] * 12)
    assert volatilita_annualizzata(s) == pytest.approx(0.0)


def test_max_drawdown_picco_120_minimo_90():
    s = serie_mensile([100, 120, 90, 130])
    assert max_drawdown(s) == pytest.approx(90 / 120 - 1)


def test_peggior_anno_meno_20_percento():
    # 2020 piatto (0%), 2021 chiude a -20% rispetto a fine 2020
    s = serie_mensile([100] * 12 + [80] * 12, inizio="2020-01-31")
    assert peggior_anno(s) == pytest.approx(-0.20)


def test_simula_50_50_un_asset_sale_10pc():
    idx = pd.date_range("2020-01-31", periods=13, freq="ME")
    prezzi = pd.DataFrame(
        {"A": [100.0] * 13, "B": [100.0] + [110.0] * 12}, index=idx
    )
    serie = simula_portafoglio(prezzi, {"A": 0.5, "B": 0.5})
    assert serie.iloc[0] == pytest.approx(10_000)
    assert serie.iloc[1] == pytest.approx(10_500)  # 5000 + 5000 * 1.1
    assert serie.iloc[-1] == pytest.approx(10_500)  # poi tutto fermo


def test_simula_ribilanciamento_cambia_il_risultato():
    # B raddoppia a ogni cambio d'anno, A fermo: col ribilanciamento a inizio
    # anno i guadagni di B vengono in parte spostati su A.
    idx = pd.date_range("2020-01-31", periods=25, freq="ME")
    prezzi = pd.DataFrame(
        {"A": [100.0] * 25, "B": [100.0 * 2 ** (i // 12) for i in range(25)]},
        index=idx,
    )
    serie = simula_portafoglio(prezzi, {"A": 0.5, "B": 0.5})
    # Anno 1: 5000 + 5000*2 = 15000. Ribilanciato a 7500/7500.
    # Anno 2: 7500 + 7500*2 = 22500.
    assert serie.iloc[12] == pytest.approx(15_000)
    assert serie.iloc[24] == pytest.approx(22_500)
