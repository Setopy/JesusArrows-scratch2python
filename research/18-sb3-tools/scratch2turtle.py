"""scratch2turtle.py - turn a Scratch 3 project into readable Python turtle code.

Proof of concept for a parent showing a child "here is YOUR Scratch project
as Python". Standard library only. Reads either a project.json or a .sb3
(which is just a zip with project.json inside).

    python3 scratch2turtle.py square.json
    python3 scratch2turtle.py MyGame.sb3 --colab     # header for ColabTurtlePlus

It deliberately covers only the blocks a beginner uses with the pen and
turtle: motion, pen, simple looks (say -> print), control, variables,
operators, ask/answer, broadcasts, key presses and My Blocks. Anything else is
written out as a "# TODO" comment so nothing is silently lost.
"""
import json
import re
import sys
import zipfile

HATS = {"event_whenflagclicked", "event_whenkeypressed",
        "event_whenbroadcastreceived", "procedures_definition"}

# Statement blocks: opcode -> template. {NAME} is replaced by the Python
# expression of the input (or field) called NAME.
STATEMENTS = {
    "motion_movesteps":       "forward({STEPS})",
    "motion_turnright":       "right({DEGREES})",
    "motion_turnleft":        "left({DEGREES})",
    "motion_gotoxy":          "goto({X}, {Y})",
    "motion_pointindirection": "setheading(90 - {DIRECTION})   # Scratch 0 = up, turtle 0 = right",
    "motion_changexby":       "setx(xcor() + {DX})",
    "motion_changeyby":       "sety(ycor() + {DY})",
    "motion_setx":            "setx({X})",
    "motion_sety":            "sety({Y})",
    "looks_say":              "print({MESSAGE})",
    "looks_sayforsecs":       "print({MESSAGE})\nsleep({SECS})",
    "looks_think":            "print({MESSAGE})   # think",
    "looks_show":             "showturtle()",
    "looks_hide":             "hideturtle()",
    "pen_penDown":            "pendown()",
    "pen_penUp":              "penup()",
    "pen_clear":              "clear()",
    "pen_setPenSizeTo":       "pensize({SIZE})",
    "pen_setPenColorToColor": "pencolor({COLOR})",
    "control_wait":           "sleep({DURATION})",
    "control_stop":           "return   # stop",
    "sensing_askandwait":     "answer = input({QUESTION})",
}

REPORTERS = {
    "operator_add":      "({NUM1} + {NUM2})",
    "operator_subtract": "({NUM1} - {NUM2})",
    "operator_multiply": "({NUM1} * {NUM2})",
    "operator_divide":   "({NUM1} / {NUM2})",
    "operator_mod":      "({NUM1} % {NUM2})",
    "operator_lt":       "{OPERAND1} < {OPERAND2}",
    "operator_gt":       "{OPERAND1} > {OPERAND2}",
    "operator_equals":   "{OPERAND1} == {OPERAND2}",
    "operator_and":      "({OPERAND1} and {OPERAND2})",
    "operator_or":       "({OPERAND1} or {OPERAND2})",
    "operator_not":      "not {OPERAND}",
    "operator_join":     "{STRING1} + {STRING2}",   # str() added below when needed
    "operator_random":   "randint({FROM}, {TO})",
    "operator_round":    "round({NUM})",
    "motion_xposition":  "xcor()",
    "motion_yposition":  "ycor()",
    "motion_direction":  "(90 - heading())",
    "sensing_answer":    "answer",
}


def py_name(text):
    """'draw polygon %s' -> 'draw_polygon'; 'my score' -> 'my_score'."""
    text = re.sub(r"%[sbn]", "", text)
    text = re.sub(r"\W+", "_", text.strip().lower()).strip("_")
    if not text or text[0].isdigit():
        text = "v_" + text
    return text


def bare(expr):
    """Drop one pair of outer brackets: forward((a + b)) -> forward(a + b)."""
    if expr.startswith("(") and expr.endswith(")"):
        depth = 0
        for i, ch in enumerate(expr):
            depth += ch == "("
            depth -= ch == ")"
            if depth == 0 and i < len(expr) - 1:
                return expr
        return expr[1:-1]
    return expr


def literal(value):
    """Scratch stores numbers as text. Give back 100 rather than '100'."""
    s = str(value)
    try:
        f = float(s)
        if s.strip() and f.is_integer() and "e" not in s.lower():
            return str(int(f))
        if s.strip():
            return repr(f)
    except ValueError:
        pass
    return repr(s)


class Converter:
    def __init__(self, target):
        self.blocks = target["blocks"]
        self.name = target["name"]
        self.uses = set()          # names we must import
        self.globals = set()       # Scratch variables written to
        self.todo = set()

    # ----- inputs -------------------------------------------------------
    def value(self, block, name):
        """Python expression for input or field `name` of `block`."""
        if name in block.get("inputs", {}):
            item = block["inputs"][name]
            ref = item[1]          # [shadowType, blockId-or-primitive, (shadow)]
            return self.expr(ref)
        if name in block.get("fields", {}):
            return repr(block["fields"][name][0])
        return "None"

    def expr(self, ref):
        if ref is None:
            return "None"
        if isinstance(ref, list):              # compressed primitive
            code = ref[0]
            if code in (4, 5, 6, 7, 8):        # numbers / angle
                return literal(ref[1])
            if code == 9:                      # colour '#ff0000'
                return repr(ref[1])
            if code == 10:                     # text (may still be a number)
                return literal(ref[1])
            if code == 11:                     # broadcast
                return repr(ref[1])
            if code in (12, 13):               # variable / list reporter
                return py_name(ref[1])
            return repr(ref)
        b = self.blocks[ref]
        op = b["opcode"]
        if op == "argument_reporter_string_number" or op == "argument_reporter_boolean":
            return py_name(b["fields"]["VALUE"][0])
        if op == "data_variable":
            return py_name(b["fields"]["VARIABLE"][0])
        if op == "operator_random":
            self.uses.add("randint")
        if op == "operator_join":
            parts = [self.value(b, k) for k in ("STRING1", "STRING2")]
            parts = [p if p[:1] in "'\"" else f"str({p})" for p in parts]
            return " + ".join(parts)
        if op in REPORTERS:
            tmpl = REPORTERS[op]
            return re.sub(r"\{(\w+)\}", lambda m: self.value(b, m.group(1)), tmpl)
        # shadow menus such as motion_goto_menu keep their value in a field
        if b.get("shadow") and b.get("fields"):
            return repr(next(iter(b["fields"].values()))[0])
        self.todo.add(op)
        return f"None  # TODO {op}"

    # ----- statements ---------------------------------------------------
    def stack(self, block_id, depth):
        """Lines for a chain of blocks joined by `next`."""
        lines = []
        pad = "    " * depth
        while block_id:
            b = self.blocks[block_id]
            lines += [pad + l for l in self.statement(b, depth)]
            block_id = b["next"]
        return lines

    def body(self, block, key, depth):
        sub = block.get("inputs", {}).get(key)
        inner = self.stack(sub[1], depth + 1) if sub and sub[1] else []
        return inner or ["    " * (depth + 1) + "pass"]

    def statement(self, b, depth):
        op = b["opcode"]
        if op == "control_repeat":
            return [f"for count in range({self.value(b, 'TIMES')}):"] + \
                   [l[4 * depth:] for l in self.body(b, "SUBSTACK", depth)]
        if op == "control_forever":
            return ["while True:"] + [l[4 * depth:] for l in self.body(b, "SUBSTACK", depth)]
        if op == "control_repeat_until":
            return [f"while not ({self.value(b, 'CONDITION')}):"] + \
                   [l[4 * depth:] for l in self.body(b, "SUBSTACK", depth)]
        if op == "control_wait_until":
            self.uses.add("sleep")
            return [f"while not ({self.value(b, 'CONDITION')}):", "    sleep(0.03)"]
        if op in ("control_if", "control_if_else"):
            out = [f"if {self.value(b, 'CONDITION')}:"] + \
                  [l[4 * depth:] for l in self.body(b, "SUBSTACK", depth)]
            if op == "control_if_else":
                out += ["else:"] + [l[4 * depth:] for l in self.body(b, "SUBSTACK2", depth)]
            return out
        if op == "data_setvariableto":
            v = py_name(b["fields"]["VARIABLE"][0]); self.globals.add(v)
            return [f"{v} = {self.value(b, 'VALUE')}"]
        if op == "data_changevariableby":
            v = py_name(b["fields"]["VARIABLE"][0]); self.globals.add(v)
            return [f"{v} = {v} + {self.value(b, 'VALUE')}"]
        if op in ("event_broadcast", "event_broadcastandwait"):
            msg = b["inputs"]["BROADCAST_INPUT"][1]
            name = msg[1] if isinstance(msg, list) else "message"
            return [f"when_i_receive_{py_name(name)}()   # broadcast"]
        if op == "procedures_call":
            m = b["mutation"]
            ids = json.loads(m.get("argumentids", "[]"))
            args = ", ".join(bare(self.value(b, i)) for i in ids)
            return [f"{py_name(m['proccode'])}({args})"]
        if op in STATEMENTS:
            if op in ("control_wait", "looks_sayforsecs"):
                self.uses.add("sleep")
            if op == "sensing_askandwait":
                self.globals.add("answer")
            text = re.sub(r"\{(\w+)\}", lambda m: bare(self.value(b, m.group(1))), STATEMENTS[op])
            return text.split("\n")
        self.todo.add(op)
        return [f"# TODO: no Python yet for Scratch block '{op}'"]

    # ----- scripts ------------------------------------------------------
    def scripts(self):
        hats = [(bid, b) for bid, b in self.blocks.items()
                if b.get("topLevel") and b["opcode"] in HATS]
        # keep Scratch's left-to-right, top-to-bottom order of scripts
        hats.sort(key=lambda kv: (kv[1].get("x", 0), kv[1].get("y", 0)))
        loose = [b["opcode"] for b in self.blocks.values()
                 if b.get("topLevel") and b["opcode"] not in HATS]
        return hats, loose


def header(colab):
    if colab:
        return ["from ColabTurtlePlus.Turtle import *", "clearscreen()", ""]
    return ["from turtle import *", ""]


def convert(project, colab=False):
    out, uses = [], set()
    variables = []
    for target in project["targets"]:
        for name, value in target.get("variables", {}).values():
            variables.append(f"{py_name(name)} = {literal(value)}"
                             + ("   # variable for all sprites" if target["isStage"] else ""))
    if variables:
        out += ["# Scratch variables"] + variables + [""]
    for target in project["targets"]:
        c = Converter(target)
        hats, loose = c.scripts()
        if not hats:
            continue
        flags = [h for h in hats if h[1]["opcode"] == "event_whenflagclicked"]
        others = [h for h in hats if h[1]["opcode"] != "event_whenflagclicked"]
        sprite = [f"# ---- Sprite: {c.name} ----"]

        # Simplest case (most beginner projects): one green-flag script and
        # nothing else.  Write it flat, no functions, like a first Python program.
        if len(flags) == 1 and not others:
            sprite += ["# when green flag clicked"] + c.stack(flags[0][1]["next"], 0)
        else:
            calls, keys = [], []
            for n, (bid, b) in enumerate(hats):
                op = b["opcode"]
                c.globals = set()
                if op == "procedures_definition":
                    proto = c.blocks[b["inputs"]["custom_block"][1]]
                    m = proto["mutation"]
                    params = ", ".join(py_name(a) for a in json.loads(m["argumentnames"]))
                    fname = py_name(m["proccode"])
                    shown = m["proccode"]
                    for a in json.loads(m["argumentnames"]):
                        shown = re.sub(r"%[sbn]", f"({a})", shown, count=1)
                    sprite.append(f"# My Block: define {shown}")
                    sprite.append(f"def {fname}({params}):")
                elif op == "event_whenflagclicked":
                    fname = f"when_flag_clicked_{len(calls) + 1}"
                    calls.append(fname)
                    sprite.append(f"def {fname}():")
                elif op == "event_whenkeypressed":
                    key = b["fields"]["KEY_OPTION"][0]
                    fname = f"when_{py_name(key)}_key_pressed"
                    keys.append((fname, key))
                    sprite.append(f"def {fname}():")
                else:  # when I receive
                    fname = f"when_i_receive_{py_name(b['fields']['BROADCAST_OPTION'][0])}"
                    sprite.append(f"def {fname}():")
                body = c.stack(b["next"], 1)
                if c.globals:
                    body = ["    global " + ", ".join(sorted(c.globals))] + body
                sprite += (body or ["    pass"]) + [""]
            for fname, key in keys:
                sprite.append(f"onkey({fname}, {key!r})")
            if keys:
                sprite.append("listen()")
            sprite += [f"{f}()   # the green flag" for f in calls]
        if loose:
            sprite.append(f"# (skipped {len(loose)} loose block(s) with no hat: "
                          + ", ".join(sorted(set(loose))) + ")")
        if c.todo:
            sprite.append("# Blocks not translated yet: " + ", ".join(sorted(c.todo)))
        uses |= c.uses
        out += sprite + [""]
    imports = []
    if "sleep" in uses:
        imports.append("from time import sleep")
    if "randint" in uses:
        imports.append("from random import randint")
    head = header(colab)
    head = head[:1] + imports + head[1:]
    return "\n".join(head + out).rstrip() + "\n"


def load(path):
    if path.endswith(".sb3"):
        with zipfile.ZipFile(path) as z:
            return json.loads(z.read("project.json"))
    with open(path, encoding="utf-8") as f:
        return json.load(f)


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        sys.exit(__doc__)
    print(convert(load(args[0]), colab="--colab" in sys.argv), end="")
