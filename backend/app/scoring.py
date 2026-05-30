def mae(preds, obs):
    vals = [abs(p - o) for p, o in zip(preds, obs) if p is not None and o is not None]
    return sum(vals) / len(vals) if vals else None

def bias(preds, obs):
    vals = [p - o for p, o in zip(preds, obs) if p is not None and o is not None]
    return sum(vals) / len(vals) if vals else None
