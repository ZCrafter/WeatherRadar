def mean_absolute_error(preds, obs):
    vals = [abs(p - o) for p, o in zip(preds, obs) if p is not None and o is not None]
    return round(sum(vals) / len(vals), 2) if vals else None

def mean_bias(preds, obs):
    vals = [p - o for p, o in zip(preds, obs) if p is not None and o is not None]
    return round(sum(vals) / len(vals), 2) if vals else None

def precipitation_brier_score(preds_mm, obs_mm, threshold=0.1):
    preds = [1 if (p or 0) >= threshold else 0 for p in preds_mm if p is not None]
    obs = [1 if (o or 0) >= threshold else 0 for o in obs_mm if o is not None]
    vals = [(p - o) ** 2 for p, o in zip(preds, obs)]
    return round(sum(vals) / len(vals), 4) if vals else None

def precipitation_hit_rate(preds_mm, obs_mm, threshold=0.1):
    preds = [1 if (p or 0) >= threshold else 0 for p in preds_mm if p is not None]
    obs = [1 if (o or 0) >= threshold else 0 for o in obs_mm if o is not None]
    tp = sum(1 for p, o in zip(preds, obs) if p == 1 and o == 1)
    fp = sum(1 for p, o in zip(preds, obs) if p == 1 and o == 0)
    fn = sum(1 for p, o in zip(preds, obs) if p == 0 and o == 1)
    denom = tp + fp + fn
    return round(tp / denom, 3) if denom else None
