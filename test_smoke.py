import pytest

@pytest.mark.smoke
def test_smoke_1():
    assert 1 + 1 == 2

@pytest.mark.smoke
def test_smoke_2():
    assert "hello".upper() == "HELLO"