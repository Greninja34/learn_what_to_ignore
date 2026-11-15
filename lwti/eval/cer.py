"""Character error rate.

CER = total edit distance / total reference characters (corpus-level, the
usual HTR convention), computed with jiwer. `self_check()` compares against
a plain Levenshtein implementation on hand-made pairs.
"""
import jiwer


def cer(refs, hyps):
    refs = list(refs)
    hyps = [h if h else "" for h in hyps]
    # jiwer rejects empty references; they contribute no characters anyway
    pairs = [(r, h) for r, h in zip(refs, hyps) if r]
    if not pairs:
        return 0.0
    r, h = zip(*pairs)
    return jiwer.cer(list(r), list(h))


def levenshtein(a, b):
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]


def self_check():
    pairs = [("hello world", "helo world"), ("abc", ""), ("q̃ y paresçio", "q y paresçio"),
             ("the cat", "the cat"), ("short", "a much longer guess")]
    refs, hyps = zip(*pairs)
    ours = sum(levenshtein(r, h) for r, h in pairs) / sum(len(r) for r in refs)
    theirs = cer(refs, hyps)
    assert abs(ours - theirs) < 1e-9, (ours, theirs)
    print(f"CER self-check ok: {theirs:.4f}")


if __name__ == "__main__":
    self_check()
