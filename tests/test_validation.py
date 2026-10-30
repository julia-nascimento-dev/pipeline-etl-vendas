import pandas as pd
import pytest
from src.validation import validate_sales

def sample(**changes):
    row={"order_id":"V1","order_date":"2026-01-01","customer_id":"C1","product":"Livro","quantity":2,"unit_price":10.0,"region":"Sul"}
    row.update(changes)
    return pd.DataFrame([row])

def test_valid_row_is_accepted():
    valid, invalid=validate_sales(sample())
    assert len(valid)==1 and invalid.empty
    assert valid.iloc[0]["quantity"]==2

def test_invalid_date_is_rejected():
    valid, invalid=validate_sales(sample(order_date="ontem"))
    assert valid.empty
    assert "data_invalida" in invalid.iloc[0]["rejection_reason"]

def test_non_positive_quantity_is_rejected():
    valid, invalid=validate_sales(sample(quantity=0))
    assert valid.empty
    assert "quantidade_deve_ser_positiva" in invalid.iloc[0]["rejection_reason"]

def test_missing_column_raises_error():
    with pytest.raises(ValueError, match="Colunas obrigatórias ausentes"):
        validate_sales(pd.DataFrame({"order_id":["V1"]}))

def test_duplicate_business_key_is_rejected():
    frame=pd.concat([sample(),sample()], ignore_index=True)
    valid, invalid=validate_sales(frame)
    assert valid.empty and len(invalid)==2
