import time


def predict_pred_score(model, text, strength):
    proba = model.predict_proba([text])[0]
    lim = 1 - strength / 10
    pred = 1 if proba[1] > lim else 0
    score = round(proba[pred], 3)
    return {
        "is_spam": bool(pred),
        "confidence": score,
        "strength": strength,
        "input_text": text,
        "time": time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()),
    }
