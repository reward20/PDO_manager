from time import time
import sys
from script import (
    script_pdo_read,
    excel_base_create,
)


if __name__ == "__main__":
    sys.dont_write_bytecode = True
    now = time()
    script_pdo_read()
    excel_base_create()
    print(time() - now)
