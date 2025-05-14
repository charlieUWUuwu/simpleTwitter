import os
import sys

check_only = "--check" in sys.argv

# black 格式化或檢查
os.system(f"black . {'--check' if check_only else ''}")

# isort 排序或檢查
os.system(f"isort . {'--check-only' if check_only else ''}")
