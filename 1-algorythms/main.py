from typing import List


def get_lcs(arr: List[int]) -> int:
    longest = 0
    counter = 1
    prev = None
    for i in arr:
        if prev is None:
            prev = i
            longest = 1
        else:
            if prev <= i:
                counter += 1
            else:
                counter = 1
            if counter > longest:
                longest = counter
            prev = i

    return longest


def test_empty():
    assert get_lcs([]) == 0


def test_one():
    assert get_lcs([1]) == 1


def test_multi_asc():
    assert get_lcs([0, 1, 2]) == 3


def test_multi_desc():
    assert get_lcs([3, 2, 1]) == 1


def test_negative_asc():
    assert get_lcs([-10, 1]) == 2


def test_negative_desc():
    assert get_lcs([1, -10]) == 1


def test_equal():
    assert get_lcs([0, 0, 0, 0]) == 4


def test_zero_asc():
    assert get_lcs([-1, 0, 1]) == 3


def test_zero_desc():
    assert get_lcs([1, 0, -1]) == 1


def test_subseq_middle():
    assert get_lcs([5, 4, 5, 6, 4]) == 3


def test_subseq_end():
    assert get_lcs([5, 4, 5, 6]) == 3


def test_all():
    test_empty()
    test_one()
    test_multi_asc()
    test_multi_desc()
    test_negative_asc()
    test_negative_desc()
    test_equal()
    test_zero_asc()
    test_zero_desc()
    test_subseq_middle()
    test_subseq_end()
    print("Done!")


if __name__ == "__main__":
    test_all()
