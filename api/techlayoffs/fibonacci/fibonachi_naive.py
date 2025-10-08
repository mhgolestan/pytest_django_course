
def fibonachi_naive(n: int) -> int:
    if n <= 1:
        return n
    else:
        return fibonachi_naive(n - 1) + fibonachi_naive(n - 2)