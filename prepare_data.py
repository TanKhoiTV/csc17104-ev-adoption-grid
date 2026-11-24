#!/usr/bin/env python3
"""prepare_data.py -- convert the two raw .xlsx sources into tidy long CSVs.

Entry point per ADR-003 D.1. Reads:
  data/EDGAR_2026_GHG_booklet_2026.xlsx  (sheet GHG_by_sector_and_country)
  data/EV Data Explorer 2025.xlsx          (sheet GEVO_EV_2025)

Writes:
  data/processed/emissions_long.csv
  data/processed/ev_long.csv

Authority: ADR > SPECIFICATION.md > notebook. Schema, filters, encoding and
validation gates follow ADR-003 D.2-D.6. Any change to the schema must amend
ADR-003 first.
"""

from __future__ import annotations

import hashlib
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
PROCESSED = DATA / "processed"
EDGAR_PATH = DATA / "EDGAR_2026_GHG_booklet_2026.xlsx"
IEA_PATH = DATA / "EV Data Explorer 2025.xlsx"
EMISSIONS_OUT = PROCESSED / "emissions_long.csv"
EV_OUT = PROCESSED / "ev_long.csv"

# --- pins (ADR-002 D.1 / D.2) ------------------------------------------------
EDGAR_SHA256 = "BB77A0DA5735925B3A6A64BE63DADE9E71B57174D5EC6C7EFF872274DF00F88C"
IEA_SHA256 = "309C6342BB730D1B565553B6F57F6EF7A5F436D164AF81DBCC6A2DC8AB35699D"
EDGAR_SHEET = "GHG_by_sector_and_country"
IEA_SHEET = "GEVO_EV_2025"
YEAR_EDGAR = 2025

# --- country name mapping (ADR-002 D.6 / ADR-003 D.4) -------------------------
EDGAR_COUNTRY_MAP = {
    "Viet Nam": "Vietnam",
    "Thailand": "Thailand",
    "Singapore": "Singapore",
    "China": "China",
    "Japan": "Japan",
    "Germany": "Germany",
    "United States": "United States",
    "New Zealand": "New Zealand",
}
IEA_COUNTRY_MAP = {
    "Viet Nam": "Vietnam",
    "Thailand": "Thailand",
    "China": "China",
    "Japan": "Japan",
    "Germany": "Germany",
    "USA": "United States",
    "New Zealand": "New Zealand",
}
TARGET_COUNTRIES = ["China", "Germany", "Japan", "New Zealand", "Singapore",
                    "Thailand", "United States", "Vietnam"]

# --- EDGAR sector grouping (ADR-003 D.2) --------------------------------------
SECTOR_GROUP = {
    "Agriculture": "Other",
    "Buildings": "Other",
    "Fuel Production": "Other",
    "Industrial Combustion": "Industry",
    "Power Industry": "Power",
    "Processes": "Industry",
    "Transport": "Transport",
    "Waste": "Other",
}
EDGAR_SECTORS = ["Agriculture", "Buildings", "Fuel Production",
                 "Industrial Combustion", "Power Industry", "Processes",
                 "Transport", "Waste"]
MISSING_SECTORS = {
    "Singapore": {"Agriculture"},
    "Germany": {"Waste"},
    "United States": {"Waste"},
}

# --- IEA per-parameter filters (ADR-003 D.3) ----------------------------------
EV_PARAMS = ("EV sales share", "EV stock share", "EV charging points")
SHARE_MODES = {"Cars", "2 and 3 wheelers"}
SHARE_POWERTRAIN = "EV"
CHARGING_MODE = "EV"
CHARGING_POWERTRAINS = {"Publicly available fast", "Publicly available slow"}

# --- EV coverage pin (ADR-003 D.6) --------------------------------------------
EV_COVERAGE_PIN = {
    ("China", "EV sales share"): 28,
    ("China", "EV stock share"): 28,
    ("China", "EV charging points"): 18,
    ("Germany", "EV sales share"): 28,
    ("Germany", "EV stock share"): 28,
    ("Germany", "EV charging points"): 26,
    ("Japan", "EV sales share"): 22,
    ("Japan", "EV stock share"): 22,
    ("Japan", "EV charging points"): 26,
    ("New Zealand", "EV sales share"): 30,
    ("New Zealand", "EV stock share"): 30,
    ("New Zealand", "EV charging points"): 15,
    ("Thailand", "EV sales share"): 30,
    ("Thailand", "EV stock share"): 30,
    ("Thailand", "EV charging points"): 16,
    ("United States", "EV sales share"): 28,
    ("United States", "EV stock share"): 28,
    ("United States", "EV charging points"): 25,
    ("Vietnam", "EV sales share"): 16,
    ("Vietnam", "EV stock share"): 18,
    ("Vietnam", "EV charging points"): 4,
}


class ValidationError(Exception):
    pass


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest().upper()


def check_input_hashes() -> None:
    if not EDGAR_PATH.is_file():
        raise FileNotFoundError(f"Missing input file: {EDGAR_PATH}")
    if not IEA_PATH.is_file():
        raise FileNotFoundError(f"Missing input file: {IEA_PATH}")
    edgar_hash = sha256_file(EDGAR_PATH)
    iea_hash = sha256_file(IEA_PATH)
    if edgar_hash != EDGAR_SHA256:
        raise ValidationError(
            f"EDGAR SHA-256 mismatch: got {edgar_hash}, expected {EDGAR_SHA256}"
        )
    if iea_hash != IEA_SHA256:
        raise ValidationError(
            f"IEA SHA-256 mismatch: got {iea_hash}, expected {IEA_SHA256}"
        )
    print(f"[hash] EDGAR OK  {edgar_hash}")
    print(f"[hash] IEA    OK  {iea_hash}")


def build_emissions() -> pd.DataFrame:
    if set(SECTOR_GROUP) != set(EDGAR_SECTORS):
        raise ValidationError("SECTOR_GROUP must cover all 8 EDGAR sectors")
    df_raw = pd.read_excel(EDGAR_PATH, sheet_name=EDGAR_SHEET, engine="openpyxl")
    if "Substance" not in df_raw.columns or "Country" not in df_raw.columns:
        raise ValidationError("EDGAR sheet missing required columns")
    year_col = YEAR_EDGAR if YEAR_EDGAR in df_raw.columns else str(YEAR_EDGAR)
    if year_col not in df_raw.columns:
        raise ValidationError(f"EDGAR sheet missing year column {YEAR_EDGAR}")

    df = df_raw.loc[df_raw["Substance"] == "CO2",
                    ["Country", "Sector", year_col]].copy()
    df = df.rename(columns={year_col: "emissions_mt", "Country": "src_country",
                            "Sector": "sector"})

    # country mapping: keep only the 8 target countries. Out-of-scope region
    # names in the sheet are dropped by design (not an error); report the
    # count so the exclusion is observable (ADR-003 D.4).
    dropped = sorted(set(df["src_country"].unique()) - set(EDGAR_COUNTRY_MAP))
    print(f"[emissions] dropped {len(dropped)} out-of-scope region names "
          f"({len(df['src_country'].unique())} distinct in sheet, "
          f"{len(EDGAR_COUNTRY_MAP)} target)")

    # country mapping (keep only target countries; fail-fast if a target is missing)
    df = df[df["src_country"].isin(EDGAR_COUNTRY_MAP)].copy()
    df["country"] = df["src_country"].map(EDGAR_COUNTRY_MAP)

    present = set(df["country"].unique())
    missing_countries = set(TARGET_COUNTRIES) - present
    if missing_countries:
        raise ValidationError(
            f"EDGAR: target countries missing from data: {sorted(missing_countries)}"
        )

    # sector coverage
    for country, g in df.groupby("country"):
        sectors = set(g["sector"].unique())
        expected_present = set(EDGAR_SECTORS) - MISSING_SECTORS.get(country, set())
        if sectors != expected_present:
            extra = sectors - expected_present
            missing = expected_present - sectors
            raise ValidationError(
                f"EDGAR sector coverage mismatch for {country}: "
                f"missing={sorted(missing)}, extra={sorted(extra)}"
            )

    if df["emissions_mt"].isna().any():
        raise ValidationError("EDGAR emissions_mt contains NaN")

    out = pd.DataFrame({
        "country": df["country"].astype(str),
        "year": int(YEAR_EDGAR),
        "substance": "CO2",
        "sector": df["sector"].astype(str),
        "sector_group": df["sector"].map(SECTOR_GROUP),
        "emissions_mt": df["emissions_mt"].astype(float),
    })
    if out["sector_group"].isna().any():
        bad = sorted(set(out.loc[out["sector_group"].isna(), "sector"]))
        raise ValidationError(f"EDGAR: unknown sectors not in SECTOR_GROUP: {bad}")

    out["sector_group"] = out["sector_group"].astype(str)
    out = out.sort_values(["country", "year", "sector"],
                          kind="mergesort").reset_index(drop=True)

    if out.duplicated(subset=["country", "sector"]).any():
        raise ValidationError("EDGAR: duplicate (country, sector) keys")

    if len(out) != 61:
        raise ValidationError(f"EDGAR row count mismatch: got {len(out)}, expected 61")
    return out


def build_ev() -> pd.DataFrame:
    df_raw = pd.read_excel(IEA_PATH, sheet_name=IEA_SHEET, engine="openpyxl")
    required = {"region_country", "category", "parameter", "mode", "powertrain",
                "year", "unit", "value"}
    if not required.issubset(set(df_raw.columns)):
        raise ValidationError(
            f"IEA sheet missing columns: {sorted(required - set(df_raw.columns))}"
        )

    df = df_raw[df_raw["category"] == "Historical"].copy()
    df = df[df["parameter"].isin(EV_PARAMS)].copy()

    def keep_row(row) -> bool:
        param = row["parameter"]
        mode = row["mode"]
        pwt = row["powertrain"]
        unit = row["unit"]
        if param in ("EV sales share", "EV stock share"):
            return (mode in SHARE_MODES and pwt == SHARE_POWERTRAIN
                    and unit == "percent")
        if param == "EV charging points":
            return (mode == CHARGING_MODE
                    and pwt in CHARGING_POWERTRAINS
                    and unit == "charging points")
        return False

    df = df.loc[df.apply(keep_row, axis=1)].copy()

    # country mapping: keep only target countries (Singapore has 0 rows)
    df = df[df["region_country"].isin(IEA_COUNTRY_MAP)].copy()
    df["country"] = df["region_country"].map(IEA_COUNTRY_MAP)
    if df["country"].isna().any():
        raise ValidationError("IEA country mapping produced NaN (fail-fast)")

    # year must be integer and within the pinned 2010-2024 range (ADR-003 D.3)
    try:
        df["year"] = df["year"].astype(int)
    except (ValueError, TypeError) as exc:
        raise ValidationError(
            f"IEA year column contains non-integer values: {exc}"
        ) from exc
    if not df["year"].between(2010, 2024).all():
        bad = sorted(set(df.loc[~df["year"].between(2010, 2024), "year"].tolist()))
        raise ValidationError(f"IEA year outside 2010-2024: {bad}")

    expected_ev_countries = set(TARGET_COUNTRIES) - {"Singapore"}
    present = set(df["country"].unique())
    missing = expected_ev_countries - present
    if missing:
        raise ValidationError(
            f"IEA: target countries missing from data: {sorted(missing)}"
        )
    if "Singapore" in present:
        raise ValidationError("IEA: Singapore unexpectedly present (expected 0 rows)")

    if df["value"].isna().any():
        nan_n = int(df["value"].isna().sum())
        print(f"[warn] IEA value has {nan_n} NaN rows (logged, not filled)")

    out = pd.DataFrame({
        "country": df["country"].astype(str),
        "year": df["year"],
        "parameter": df["parameter"].astype(str),
        "mode": df["mode"].astype(str),
        "powertrain": df["powertrain"].astype(str),
        "value": df["value"].astype(float),
        "unit": df["unit"].astype(str),
    })
    out = out.sort_values(["country", "year", "parameter", "mode", "powertrain"],
                          kind="mergesort").reset_index(drop=True)

    keys = list(zip(out["country"], out["year"], out["parameter"],
                    out["mode"], out["powertrain"]))
    if len(keys) != len(set(keys)):
        raise ValidationError("IEA: duplicate (country, year, parameter, mode, powertrain) keys")

    if len(out) != 496:
        raise ValidationError(f"IEA row count mismatch: got {len(out)}, expected 496")

    counts = out.groupby(["country", "parameter"]).size().to_dict()
    for key, expected in EV_COVERAGE_PIN.items():
        got = counts.get(key, 0)
        if got != expected:
            raise ValidationError(
                f"IEA coverage mismatch for {key}: got {got}, expected {expected}"
            )
    extra = set(counts) - set(EV_COVERAGE_PIN)
    if extra:
        raise ValidationError(f"IEA unexpected (country, parameter) pairs: {sorted(extra)}")

    if sum(EV_COVERAGE_PIN.values()) != 496:
        raise ValidationError("EV_COVERAGE_PIN total must be 496")

    return out


def main() -> int:
    print("=== prepare_data.py ===")
    check_input_hashes()

    emissions = build_emissions()
    ev = build_ev()

    PROCESSED.mkdir(parents=True, exist_ok=True)
    emissions.to_csv(EMISSIONS_OUT, index=False, encoding="utf-8",
                     lineterminator="\n", na_rep="")
    ev.to_csv(EV_OUT, index=False, encoding="utf-8",
              lineterminator="\n", na_rep="")

    print(f"\n[emissions] rows={len(emissions)} countries={emissions['country'].nunique()}")
    print(f"[ev] rows={len(ev)} countries={ev['country'].nunique()}")
    for country in sorted(set(TARGET_COUNTRIES) - set(ev["country"].unique())):
        print(f"[ev] {country}: 0 rows (absent from source; expected)")
    print("\n[ev] per (country, parameter):")
    for (country, param), n in sorted(ev.groupby(["country", "parameter"]).size().items()):
        print(f"  {country:16s} {param:22s} {n}")
    print("\n[ev] per parameter totals:")
    for param, n in sorted(ev.groupby("parameter").size().items()):
        print(f"  {param:22s} {n}")

    print(f"\n[output] {EMISSIONS_OUT}")
    print(f"  sha256 = {sha256_file(EMISSIONS_OUT)}")
    print(f"[output] {EV_OUT}")
    print(f"  sha256 = {sha256_file(EV_OUT)}")
    print("\nDONE")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:  # noqa: BLE001 - top-level entry point
        print(f"\nERROR: {type(e).__name__}: {e}", file=sys.stderr)
        sys.exit(1)
