import argparse
import multiprocessing as mp
import re
from datetime import datetime
from typing import Any

from pyrage import x25519


def search(pattern: re.Pattern[Any]) -> str:
    while True:
        ident = x25519.Identity.generate()
        pub, priv = str(ident.to_public()), str(ident)
        if pattern.search(pub):
            return f"# created: {datetime.now().isoformat()}\n# public key: {pub}\n{priv}"

def cli():
    parser = argparse.ArgumentParser(
        prog='vanity-pyrage',
        description="A vanity age key generation tool powered by pyrage"
    )
    
    parser.add_argument('pattern', type=str, help='regex pattern')
    
    args = parser.parse_args()
    
    pattern_normalize: str = f"^age1{args.pattern.lstrip('^')}\\w+"
    regex = re.compile(pattern=pattern_normalize)
    
    func_args = [regex] * mp.cpu_count()
    
    with mp.Pool(mp.cpu_count()) as p:
        for r in p.imap_unordered(search, func_args):
            if r:
                print(r)
                p.terminate()
                break