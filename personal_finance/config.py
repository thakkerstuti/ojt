import os
from pathlib import Path


BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)


USERS_CSV = DATA_DIR / "users.csv"
ACCOUNTS_CSV = DATA_DIR / "accounts.csv"
TRANSACTIONS_CSV = DATA_DIR / "transactions.csv"
BUDGETS_CSV = DATA_DIR / "budgets.csv"
LOG_FILE = DATA_DIR / "app.log"


# Ensure CSVs exist with headers
def ensure_csv(path: Path, headers: list[str]):
if not path.exists():
with path.open("w", newline="", encoding="utf-8") as f:
f.write(",".join(headers) + "\n")


ensure_csv(USERS_CSV, ["username","password_hash","full_name"])
ensure_csv(ACCOUNTS_CSV, ["account_id","username","name","type","balance"])
ensure_csv(TRANSACTIONS_CSV, ["tx_id","account_id","username","date","amount","category","note"])
ensure_csv(BUDGETS_CSV, ["budget_id","username","category","period","limit"])
