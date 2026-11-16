import json
import os
import random
import sys
import urllib.error
import urllib.request
ENV = os.environ.get("MAKEFUN_ENV_URL") or sys.exit("MAKEFUN_ENV_URL is not set")
BUDGET = 60000
MATE = 100000
INF = 10 ** 9
VAL = [0, 100, 320, 330, 500, 900, 20000]
PP = [0, 0, 0, 0, 0, 0, 0, 0, 50, 50, 50, 50, 50, 50, 50, 50, 10, 10, 20, 30, 30, 20, 10, 10, 5, 5, 10, 25, 25, 10, 5, 5, 0, 0, 0, 20, 20, 0, 0, 0, 5, -5, -10, 0, 0, -10, -5, 5, 5, 10, 10, -20, -20, 10, 10, 5, 0, 0, 0, 0, 0, 0, 0, 0]
PN = [-50, -40, -30, -30, -30, -30, -40, -50, -40, -20, 0, 0, 0, 0, -20, -40, -30, 0, 10, 15, 15, 10, 0, -30, -30, 5, 15, 20, 20, 15, 5, -30, -30, 0, 15, 20, 20, 15, 0, -30, -30, 5, 10, 15, 15, 10, 5, -30, -40, -20, 0, 5, 5, 0, -20, -40, -50, -40, -30, -30, -30, -30, -40, -50]
PB = [-20, -10, -10, -10, -10, -10, -10, -20, -10, 0, 0, 0, 0, 0, 0, -10, -10, 0, 5, 10, 10, 5, 0, -10, -10, 5, 5, 10, 10, 5, 5, -10, -10, 0, 10, 10, 10, 10, 0, -10, -10, 10, 10, 10, 10, 10, 10, -10, -10, 5, 0, 0, 0, 0, 5, -10, -20, -10, -10, -10, -10, -10, -10, -20]
PR = [0, 0, 0, 0, 0, 0, 0, 0, 5, 10, 10, 10, 10, 10, 10, 5, -5, 0, 0, 0, 0, 0, 0, -5, -5, 0, 0, 0, 0, 0, 0, -5, -5, 0, 0, 0, 0, 0, 0, -5, -5, 0, 0, 0, 0, 0, 0, -5, -5, 0, 0, 0, 0, 0, 0, -5, 0, 0, 0, 5, 5, 0, 0, 0]
PQ = [-20, -10, -10, -5, -5, -10, -10, -20, -10, 0, 0, 0, 0, 0, 0, -10, -10, 0, 5, 5, 5, 5, 0, -10, -5, 0, 5, 5, 5, 5, 0, -5, 0, 0, 5, 5, 5, 5, 0, -5, -10, 5, 5, 5, 5, 5, 0, -10, -10, 0, 5, 0, 0, 0, 0, -10, -20, -10, -10, -5, -5, -10, -10, -20]
PK = [-30, -40, -40, -50, -50, -40, -40, -30, -30, -40, -40, -50, -50, -40, -40, -30, -30, -40, -40, -50, -50, -40, -40, -30, -30, -40, -40, -50, -50, -40, -40, -30, -20, -30, -30, -40, -40, -30, -30, -20, -10, -20, -20, -20, -20, -20, -20, -10, 20, 20, 0, 0, 0, 0, 20, 20, 20, 30, 10, 0, 0, 10, 30, 20]
PST = [0, PP, PN, PB, PR, PQ, PK]
T = [[0] * 128 for _ in range(7)]
for _p in range(1, 7):
    for _s in range(128):
        if not (_s & 0x88):
            T[_p][_s] = VAL[_p] + PST[_p][(7 - (_s >> 4)) * 8 + (_s & 7)]
KN = [33, 31, 18, 14, -14, -18, -31, -33]
KG = [1, -1, 16, -16, 15, 17, -15, -17]
BG = [15, 17, -15, -17]
RG = [1, -1, 16, -16]
QG = BG + RG
_r = random.Random(20261116)
Z = [[_r.getrandbits(64) for _ in range(128)] for _ in range(12)]
ZT = _r.getrandbits(64)
ZC = [_r.getrandbits(64) for _ in range(16)]
ZE = [_r.getrandbits(64) for _ in range(8)]
CR = [15] * 128
CR[0] = 13
CR[7] = 14
CR[4] = 12
CR[112] = 7
CR[119] = 11
CR[116] = 3
def zi(p):
    return p - 1 if p > 0 else 5 - p
b = [0] * 128
turn = 0
castle = 0
ep = -1
half = 0
key = 0
wk = 4
bk = 116
undo = []
TT = {}
KILL = [[0, 0] for _ in range(256)]
HIST = [[0] * 128 for _ in range(12)]
nodes = 0
path = set()
hist = set()
ROOTBEST = 0
class AB(Exception):
    pass
def mk(f, t, pr):
    return f | (t << 7) | (pr << 14)
def attacked(s, w):
    u = 1 if w else -1
    for d in (-15, -17) if w else (15, 17):
        t = s + d
        if not (t & 0x88) and b[t] == u:
            return True
    for d in KN:
        t = s + d
        if not (t & 0x88) and b[t] == 2 * u:
            return True
    for d in KG:
        t = s + d
        if not (t & 0x88) and b[t] == 6 * u:
            return True
    for d in BG:
        t = s + d
        while not (t & 0x88):
            q = b[t]
            if q:
                if q == 3 * u or q == 5 * u:
                    return True
                break
            t += d
    for d in RG:
        t = s + d
        while not (t & 0x88):
            q = b[t]
            if q:
                if q == 4 * u or q == 5 * u:
                    return True
                break
            t += d
    return False
def parse_fen(fen):
    global turn, castle, ep, half, key, wk, bk
    parts = fen.split()
    for i in range(128):
        b[i] = 0
    for i, row in enumerate(parts[0].split("/")):
        r = 7 - i
        f = 0
        for c in row:
            if c.isdigit():
                f += int(c)
            else:
                s = r * 16 + f
                p = "PNBRQK".index(c.upper()) + 1
                if c.islower():
                    p = -p
                b[s] = p
                if p == 6:
                    wk = s
                elif p == -6:
                    bk = s
                f += 1
    turn = 0 if parts[1] == "w" else 1
    castle = 0
    if len(parts) > 2:
        for c in parts[2]:
            if c == "K":
                castle |= 1
            elif c == "Q":
                castle |= 2
            elif c == "k":
                castle |= 4
            elif c == "q":
                castle |= 8
    ep = -1
    if len(parts) > 3 and parts[3] != "-":
        ep = (ord(parts[3][0]) - 97) + (int(parts[3][1]) - 1) * 16
    half = int(parts[4]) if len(parts) > 4 else 0
    k = 0
    for s in range(128):
        p = b[s]
        if p:
            k ^= Z[zi(p)][s]
    if turn:
        k ^= ZT
    k ^= ZC[castle]
    if ep >= 0:
        k ^= ZE[ep & 7]
    key = k
    undo.clear()
def make(m):
    global turn, castle, ep, half, key, wk, bk
    f = m & 127
    t = (m >> 7) & 127
    pr = (m >> 14) & 7
    p = b[f]
    cap = b[t]
    cs = t
    if abs(p) == 1 and t == ep and cap == 0:
        cs = t - 16 if p > 0 else t + 16
        cap = b[cs]
    undo.append((m, cap, cs, castle, ep, half, key))
    key ^= Z[zi(p)][f]
    if cap:
        key ^= Z[zi(cap)][cs]
    np = (pr if pr else abs(p)) * (1 if p > 0 else -1)
    key ^= Z[zi(np)][t]
    b[f] = 0
    if cs != t:
        b[cs] = 0
    b[t] = np
    if abs(p) == 6:
        if p > 0:
            wk = t
        else:
            bk = t
        if abs(t - f) == 2:
            rf, rt = (f + 3, f + 1) if t > f else (f - 4, f - 1)
            r = b[rf]
            key ^= Z[zi(r)][rf] ^ Z[zi(r)][rt]
            b[rt] = r
            b[rf] = 0
    nc = castle & CR[f] & CR[t]
    if nc != castle:
        key ^= ZC[castle] ^ ZC[nc]
        castle = nc
    ne = -1
    if abs(p) == 1 and abs(t - f) == 32:
        ne = (f + t) // 2
    if ep >= 0:
        key ^= ZE[ep & 7]
    if ne >= 0:
        key ^= ZE[ne & 7]
    ep = ne
    half = 0 if cap or abs(p) == 1 else half + 1
    key ^= ZT
    turn ^= 1
def unmake():
    global turn, castle, ep, half, key, wk, bk
    m, cap, cs, c0, e0, h0, k0 = undo.pop()
    f = m & 127
    t = (m >> 7) & 127
    pr = (m >> 14) & 7
    p = b[t]
    if abs(p) == 6:
        if p > 0:
            wk = f
        else:
            bk = f
        if abs(t - f) == 2:
            rf, rt = (f + 3, f + 1) if t > f else (f - 4, f - 1)
            b[rf] = b[rt]
            b[rt] = 0
    b[f] = (1 if p > 0 else -1) if pr else p
    if cs != t:
        b[cs] = cap
        b[t] = 0
    else:
        b[t] = cap
    castle, ep, half, key = c0, e0, h0, k0
    turn ^= 1
def gen(caps):
    ms = []
    us = turn
    for s in range(128):
        if s & 0x88:
            continue
        p = b[s]
        if not p or (p > 0) != (us == 0):
            continue
        a = abs(p)
        if a == 1:
            d = 16 if us == 0 else -16
            t = s + d
            if not caps and not (t & 0x88) and b[t] == 0:
                if (t >> 4) == 7 or (t >> 4) == 0:
                    for pr in (5, 4, 3, 2):
                        ms.append(mk(s, t, pr))
                else:
                    ms.append(mk(s, t, 0))
                    if (us == 0 and (s >> 4) == 1) or (us == 1 and (s >> 4) == 6):
                        if b[s + 2 * d] == 0:
                            ms.append(mk(s, s + 2 * d, 0))
            for dd in (d - 1, d + 1):
                t = s + dd
                if t & 0x88:
                    continue
                q = b[t]
                if q and (q > 0) != (us == 0):
                    if (t >> 4) == 7 or (t >> 4) == 0:
                        for pr in (5, 4, 3, 2):
                            ms.append(mk(s, t, pr))
                    else:
                        ms.append(mk(s, t, 0))
                elif t == ep and q == 0:
                    ms.append(mk(s, t, 0))
        elif a == 2 or a == 6:
            for dd in KN if a == 2 else KG:
                t = s + dd
                if t & 0x88:
                    continue
                q = b[t]
                if q == 0:
                    if not caps:
                        ms.append(mk(s, t, 0))
                elif (q > 0) != (us == 0):
                    ms.append(mk(s, t, 0))
            if a == 6 and not caps:
                if us == 0:
                    if castle & 1 and b[5] == 0 and b[6] == 0 and b[7] == 4 and not attacked(4, False) and not attacked(5, False) and not attacked(6, False):
                        ms.append(mk(4, 6, 0))
                    if castle & 2 and b[3] == 0 and b[2] == 0 and b[1] == 0 and b[0] == 4 and not attacked(4, False) and not attacked(3, False) and not attacked(2, False):
                        ms.append(mk(4, 2, 0))
                else:
                    if castle & 4 and b[117] == 0 and b[118] == 0 and b[119] == -4 and not attacked(116, True) and not attacked(117, True) and not attacked(118, True):
                        ms.append(mk(116, 118, 0))
                    if castle & 8 and b[115] == 0 and b[114] == 0 and b[113] == 0 and b[112] == -4 and not attacked(116, True) and not attacked(115, True) and not attacked(114, True):
                        ms.append(mk(116, 114, 0))
        else:
            for dd in BG if a == 3 else RG if a == 4 else QG:
                t = s + dd
                while not (t & 0x88):
                    q = b[t]
                    if q == 0:
                        if not caps:
                            ms.append(mk(s, t, 0))
                    else:
                        if (q > 0) != (us == 0):
                            ms.append(mk(s, t, 0))
                        break
                    t += dd
    return ms
def kng(sq, ph):
    r = sq >> 4
    f = sq & 7
    mg = PK[(7 - r) * 8 + f]
    eg = 8 * (min(f, 7 - f) + min(r, 7 - r)) - 24
    return (mg * ph + eg * (6400 - ph)) // 6400
def ev():
    s = 0
    nw = nb = 0
    np = nr = nq = nm = 0
    ph = 0
    for q in range(128):
        p = b[q]
        if p:
            a = abs(p)
            if a == 6:
                continue
            if a != 1:
                ph += VAL[a]
            if p > 0:
                s += T[p][q]
                if a == 3:
                    nw += 1
                    nm += 1
                elif a == 1:
                    np += 1
                elif a == 4:
                    nr += 1
                elif a == 5:
                    nq += 1
            else:
                s -= T[a][q ^ 0x70]
                if a == 3:
                    nb += 1
                    nm += 1
                elif a == 1:
                    np += 1
                elif a == 4:
                    nr += 1
                elif a == 5:
                    nq += 1
    if nw >= 2:
        s += 30
    if nb >= 2:
        s -= 30
    if np == 0 and nr == 0 and nq == 0 and nm <= 1:
        return 0
    if ph > 6400:
        ph = 6400
    s += kng(wk, ph) - kng(bk ^ 0x70, ph)
    return s if turn == 0 else -s
def is_cap(m):
    t = (m >> 7) & 127
    if b[t]:
        return True
    return abs(b[m & 127]) == 1 and t == ep
def order_moves(ms, tt, ply):
    def sc(m):
        if m == tt:
            return 1 << 20
        f = m & 127
        t = (m >> 7) & 127
        p = b[f]
        q = b[t]
        pr = (m >> 14) & 7
        if pr:
            return 200000 + VAL[pr]
        if q or (abs(p) == 1 and t == ep):
            v = abs(q) if q else 1
            return 10000 + VAL[v] * 10 - VAL[abs(p)]
        if m == KILL[ply][0]:
            return 9000
        if m == KILL[ply][1]:
            return 8000
        return HIST[zi(p)][t]
    ms.sort(key=sc, reverse=True)
def qs(a, be, ply):
    global nodes
    nodes += 1
    if nodes >= BUDGET:
        raise AB
    if half >= 100:
        return 0
    me = turn
    ks = wk if me == 0 else bk
    incheck = attacked(ks, me == 1)
    if not incheck:
        stand = ev()
        if stand >= be:
            return be
        if stand > a:
            a = stand
    ms = gen(False) if incheck else gen(True)
    order_moves(ms, 0, ply)
    best = -INF
    legal = 0
    for m in ms:
        make(m)
        nm = turn ^ 1
        nks = wk if nm == 0 else bk
        if attacked(nks, nm == 1):
            unmake()
            continue
        legal += 1
        if key in path or key in hist:
            v = 0
        else:
            path.add(key)
            v = -qs(-be, -a, ply + 1)
            path.discard(key)
        unmake()
        if v > best:
            best = v
        if v > a:
            a = v
        if a >= be:
            break
    if incheck:
        if legal == 0:
            return -MATE + ply
        return best
    return a
def search(d, a, be, ply):
    global nodes, ROOTBEST
    nodes += 1
    if nodes >= BUDGET:
        raise AB
    if ply and half >= 100:
        return 0
    e = TT.get(key)
    tt = 0
    if e:
        tt = e[3]
        if e[0] >= d:
            v = e[2]
            if e[1] == 0:
                return v
            if e[1] == 1 and v >= be:
                return v
            if e[1] == 2 and v <= a:
                return v
    ms = gen(False)
    order_moves(ms, tt, ply)
    best = -INF
    bm = 0
    ao = a
    cut = False
    legal = 0
    me = turn
    ks = wk if me == 0 else bk
    incheck = attacked(ks, me == 1)
    for m in ms:
        make(m)
        nm = turn ^ 1
        nks = wk if nm == 0 else bk
        if attacked(nks, nm == 1):
            unmake()
            continue
        legal += 1
        if key in path or key in hist:
            v = 0
        else:
            path.add(key)
            if d <= 1:
                v = -qs(-be, -a, ply + 1)
            else:
                v = -search(d - 1, -be, -a, ply + 1)
            path.discard(key)
        unmake()
        if v > best:
            best = v
            bm = m
        if v > a:
            a = v
        if a >= be:
            if not is_cap(m):
                f = m & 127
                t = (m >> 7) & 127
                if KILL[ply][0] != m:
                    KILL[ply][1] = KILL[ply][0]
                    KILL[ply][0] = m
                HIST[zi(b[f])][t] += d * d
            cut = True
            break
    if legal == 0:
        return -MATE + ply if incheck else 0
    if cut:
        flag = 1
    elif best <= ao:
        flag = 2
    else:
        flag = 0
    TT[key] = (d, flag, best, bm)
    if ply == 0:
        ROOTBEST = bm
    return best
def legal_moves():
    out = []
    for m in gen(False):
        make(m)
        nm = turn ^ 1
        nks = wk if nm == 0 else bk
        if not attacked(nks, nm == 1):
            out.append(m)
        unmake()
    return out
def uci(m):
    f = m & 127
    t = (m >> 7) & 127
    pr = (m >> 14) & 7
    s = "abcdefgh"[f & 7] + str((f >> 4) + 1) + "abcdefgh"[t & 7] + str((t >> 4) + 1)
    if pr:
        s += "nbrq"[pr - 2]
    return s
def think(legal_uci):
    global nodes, ROOTBEST, path
    ms = legal_moves()
    if not ms:
        return legal_uci[0] if legal_uci else None
    if len(ms) == 1:
        return uci(ms[0])
    nodes = 0
    path = {key}
    ROOTBEST = ms[0]
    best = ms[0]
    for d in range(1, 32):
        try:
            v = search(d, -INF, INF, 0)
            best = ROOTBEST
            if v > MATE - 1000 or v < -MATE + 1000:
                break
        except AB:
            break
    return uci(best)
def post(path_, body):
    req = urllib.request.Request(
        ENV + path_,
        data=json.dumps(body).encode(),
        headers={"content-type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        sys.exit(f"{path_}: HTTP {e.code}")
if __name__ == "__main__":
    game_no = -1
    while True:
        g = post("/game", {})
        if g["status"] == "done":
            break
        if g["game"] != game_no:
            game_no = g["game"]
            hist = set()
        parse_fen(g["fen"])
        hist.add(key)
        while g["status"] == "your_move":
            mv = think(g["legal_moves"])
            if mv is None:
                mv = g["legal_moves"][0]
            if mv not in g["legal_moves"]:
                mv = g["legal_moves"][0]
            g = post("/move", {"game": g["game"], "move": mv})
            if g["status"] == "your_move":
                parse_fen(g["fen"])
                hist.add(key)
        print(f"game {g['game']}: {g['outcome']} by {g['reason']}", file=sys.stderr)
    print("done", file=sys.stderr)
