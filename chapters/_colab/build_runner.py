"""Pack every chapters/NN-colab-tests.py piece into one-line Colab cells that run them all."""
import re, json, zlib, base64, pathlib, sys
here = pathlib.Path(__file__).resolve().parent.parent
pieces = []
for f in sorted(here.glob("[01][0-9]-colab-tests.py")):
    chunks = re.split(r"^# %%[ \t]*(.*)$", f.read_text(), flags=re.M)
    for name, code in zip(chunks[1::2], chunks[2::2]):
        m = re.search(r"needs typing:\s*(.*)", code, re.I)
        answers = []
        if m:
            t = m.group(1)
            eg = re.search(r"e\.g\.\s*([^)]*)", t)
            src = eg.group(1) if eg else re.split(r"\(|\+", t)[0]
            answers = [a.strip() for a in re.split(r",|\bor\b", src) if a.strip()]
        skip = None
        if "while True" in code: skip = "uses while True (stop button by design)"
        if "zipfile" in code or "open(" in code: skip = "reads a local file"
        pieces.append({"file": f.name[:2], "name": name.strip(), "code": code, "answers": answers, "skip": skip})
runner = r'''
import builtins, time, json, traceback, itertools
_P = json.loads(PIECES)
_real_sleep, _real_input = time.sleep, builtins.input
class _StopInput(Exception): pass
results = []
_ns = {}
for p in _P:
    ns = _ns.setdefault(p["file"], {"__name__": "__main__"})
    tag = p["file"] + " | " + p["name"][:60]
    if p["skip"]:
        results.append(("SKIP", tag, p["skip"])); continue
    ans = itertools.cycle(p["answers"] or ["5", "yes", "left", "3"])
    calls = [0]
    def _inp(prompt=""):
        calls[0] += 1
        if calls[0] > 40: raise _StopInput()
        a = next(ans); print(prompt + a); return a
    builtins.input = _inp
    time.sleep = lambda s: None
    try:
        exec(compile(p["code"], tag, "exec"), ns)
        results.append(("PASS", tag, ""))
    except _StopInput:
        results.append(("PASS", tag, "stopped after 40 typed answers"))
    except Exception as e:
        tb = traceback.extract_tb(e.__traceback__)
        line = next((fr.lineno for fr in reversed(tb) if fr.filename == tag), "?")
        results.append(("FAIL", tag, f"line {line}: {type(e).__name__}: {e}"))
    finally:
        builtins.input, time.sleep = _real_input, _real_sleep
from IPython.display import clear_output
clear_output()
n = {k: sum(r[0] == k for r in results) for k in ("PASS", "FAIL", "SKIP")}
print("=== RESULTS", n, "===")
for r in results:
    if r[0] != "PASS" or r[2]: print(r[0], "|", r[1], "|", r[2])
print("=== END ===")
'''
groups = {"A": ["00","01","02","03","04"], "B": ["05","06","07"], "C": ["08","09","10","11"]}
out = here / "_colab"
for g, files in groups.items():
    sel = [p for p in pieces if p["file"] in files]
    src = "PIECES = " + repr(json.dumps(sel)) + "\n" + runner
    b = base64.b64encode(zlib.compress(src.encode(), 9)).decode()
    cell = f"exec(__import__('zlib').decompress(__import__('base64').b64decode('{b}')).decode())"
    (out / f"cell_{g}.txt").write_text(cell)
    (out / f"runner_{g}.py").write_text(src)
    print(g, len(sel), "pieces,", len(cell), "chars")
