"""Validate the released file inventory without modifying the package."""
from pathlib import Path
import hashlib
import sys

root=Path(__file__).resolve().parents[1]
failures=[]
expected=set()
for line in (root/"checksums.sha256").read_text(encoding="utf-8").splitlines():
    digest,rel=line.split("  ",1)
    expected.add(rel)
    path=root/rel
    if not path.is_file():
        failures.append("Missing: "+rel)
    elif hashlib.sha256(path.read_bytes()).hexdigest()!=digest:
        failures.append("Changed: "+rel)
actual={p.relative_to(root).as_posix() for p in root.rglob("*") if p.is_file()
        and p.name!="checksums.sha256" and "__pycache__" not in p.parts
        and ".git" not in p.relative_to(root).parts
        and not p.relative_to(root).as_posix().startswith("results/recomputed_local/")}
failures.extend("Unlisted: "+p for p in sorted(actual-expected))
if failures:
    print("\n".join(failures))
    sys.exit(1)
print(f"Verified {len(expected)} files.")
