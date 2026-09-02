

# def test_add():
#     result = 1 + 1
#     assert result == 3

def test_1():
    a = [{"name": "Java"}]
    b = a.copy()

    assert a is not b
# False

    assert a[0] is b[0]
# True
    