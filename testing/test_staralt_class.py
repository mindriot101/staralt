from staralt.staralt import StarAlt, InsufficientParameters
import pytest

def test_fail_with_invalid_parameters():
    s = StarAlt()

    with pytest.raises(InsufficientParameters) as err:
        s.save_image("image.gif")
