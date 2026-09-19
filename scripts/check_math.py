#!/usr/bin/env python3
"""Finite arithmetic checks supplement, but do not replace, the written proof."""

from math import gcd, isqrt


def trace(a, b, k):
    original_gcd = gcd(a, b)
    result = [(a, b)]
    while a:
        c = k * a - b
        assert 0 <= c < a, (a, b, k, c)
        assert b * c + k == a * a
        assert c * c + a * a == k * (c * a + 1)
        assert c + a < a + b
        a, b = c, a
        result.append((a, b))
    assert b * b == k
    assert b == original_gcd
    return result


def main():
    assert trace(30, 112, 4) == [(30, 112), (8, 30), (2, 8), (0, 2)]
    assert trace(3, 27, 9) == [(3, 27), (0, 3)]
    assert trace(1, 1, 1) == [(1, 1), (0, 1)]
    checked = 0
    for a in range(1, 401):
        for b in range(a, 401):
            k, remainder = divmod(a * a + b * b, a * b + 1)
            if remainder:
                continue
            assert isqrt(k) ** 2 == k
            trace(a, b, k)
            checked += 1
    print(f"Verified examples and descent for {checked} admissible pairs with b <= 400.")


if __name__ == "__main__":
    main()
