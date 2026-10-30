import argparse, logging, os
from logging.handlers import RotatingFileHandler
from pathlib import Path
import pandas as pd
from .validation import validate_sales
from .db import connect, ensure_schema, upsert_sales

def configure_logging():
    Path("logs").mkdir(exist_ok=True)
    level = getattr(logging, os.getenv("LOG_LEVEL", "INFO").upper(), logging.INFO)
    logging.basicConfig(level=level, format="%(asctime)s %(levelname)s %(message)s", handlers=[logging.StreamHandler(), RotatingFileHandler("logs/pipeline.log", maxBytes=1_000_000, backupCount=3, encoding="utf-8")])

def run(input_path: str):
    logger = logging.getLogger(__name__)
    logger.info("Iniciando ETL: %s", input_path)
    raw = pd.read_csv(input_path, dtype={"order_id":"string", "customer_id":"string"})
    valid, invalid = validate_sales(raw)
    Path("data").mkdir(exist_ok=True)
    if not invalid.empty:
        invalid.to_csv("data/rejeitados.csv", index=False)
        logger.warning("%s registros rejeitados; detalhes em data/rejeitados.csv", len(invalid))
    else:
        Path("data/rejeitados.csv").unlink(missing_ok=True)
    if valid.empty:
        logger.warning("Nenhum registro válido para carregar")
        return {"lidos":len(raw), "validos":0, "invalidos":len(invalid)}
    with connect() as conn:
        ensure_schema(conn)
        upsert_sales(conn, valid)
    logger.info("Carga concluída: %s registros válidos processados", len(valid))
    return {"lidos":len(raw), "validos":len(valid), "invalidos":len(invalid)}

if __name__ == "__main__":
    configure_logging()
    parser=argparse.ArgumentParser(description="Pipeline ETL de vendas")
    parser.add_argument("--input", default="data/vendas.csv")
    args=parser.parse_args()
    try: print(run(args.input))
    except Exception:
        logging.exception("Falha no pipeline")
        raise
