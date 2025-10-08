import pytest

from api.techlayoffs.fibonacci.dynamic import fibonacci_dynamic_v2
from api.techlayoffs.fibonacci.conftest import track_performance


# @pytest.mark.performance
@track_performance
def test_performance():
    fibonacci_dynamic_v2(1000)
