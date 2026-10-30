from __future__ import annotations
import pandas as pd

REQUIRED = ["order_id", "order_date", "customer_id", "product", "quantity", "unit_price", "region"]


def validate_sales(frame: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Return (valid, invalid); invalid rows include a rejection_reason column."""
    missing = sorted(set(REQUIRED) - set(frame.columns))
    if missing:
        raise ValueError(f"Colunas obrigatórias ausentes: {', '.join(missing)}")

    data = frame[REQUIRED].copy()
    for col in ["order_id", "customer_id", "product", "region"]:
        data[col] = data[col].astype("string").str.strip()
    data["order_date"] = pd.to_datetime(data["order_date"], errors="coerce").dt.date
    data["quantity"] = pd.to_numeric(data["quantity"], errors="coerce")
    data["unit_price"] = pd.to_numeric(data["unit_price"], errors="coerce")

    reasons = [[] for _ in range(len(data))]
    for idx, row in enumerate(data.to_dict("records")):
        for col in ["order_id", "customer_id", "product", "region"]:
            if pd.isna(row[col]) or not str(row[col]).strip(): reasons[idx].append(f"{col}_obrigatorio")
        if pd.isna(row["order_date"]): reasons[idx].append("data_invalida")
        if pd.isna(row["quantity"]) or row["quantity"] <= 0: reasons[idx].append("quantidade_deve_ser_positiva")
        if pd.isna(row["unit_price"]) or row["unit_price"] <= 0: reasons[idx].append("preco_deve_ser_positivo")
    data["rejection_reason"] = [";".join(x) for x in reasons]
    invalid = data[data["rejection_reason"] != ""].copy()
    valid = data[data["rejection_reason"] == ""].drop(columns="rejection_reason").copy()
    if not valid.empty:
        valid["quantity"] = valid["quantity"].astype(int)
        valid["unit_price"] = valid["unit_price"].astype(float)
        if valid["order_id"].duplicated().any():
            duplicate_ids = set(valid.loc[valid["order_id"].duplicated(keep=False), "order_id"])
            duplicate_mask = valid["order_id"].isin(duplicate_ids)
            dup = valid.loc[duplicate_mask].copy()
            dup["rejection_reason"] = "order_id_duplicado_no_arquivo"
            invalid = pd.concat([invalid, dup], ignore_index=True)
            valid = valid.loc[~duplicate_mask].copy()
    return valid, invalid
