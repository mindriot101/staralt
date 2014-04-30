from staralt.coordinate import Coordinate, CannotParseCoordinate
import pytest

@pytest.fixture
def coordinate():
    c = Coordinate(name='kepler_field', ra='19 30 24', dec='46 50 12')
    return c

def test_set_name(coordinate):
    assert coordinate.name == 'kepler_field'

def test_set_ra(coordinate):
    assert coordinate.ra == '19 30 24'

def test_set_dec(coordinate):
    assert coordinate.dec == '46 50 12'

def test_ra_to_coordinate(coordinate):
    expected = (19. + (30. / 60.) + (24. / 3600.)) * 15.
    assert Coordinate.sanitise_ra(coordinate.ra) == expected

def test_dec_to_coordinate(coordinate):
    expected = (46. + (50. / 60.) + (12. / 3600.))
    assert Coordinate.sanitise_dec(coordinate.dec) == expected

def test_bad_ra_coordinate(coordinate):
    coordinate.ra = "thisisatest"
    with pytest.raises(CannotParseCoordinate) as err:
        Coordinate.sanitise_ra(coordinate.ra)

def test_bad_dec_coordinate(coordinate):
    coordinate.dec = "thisisatest"
    with pytest.raises(CannotParseCoordinate) as err:
        Coordinate.sanitise_dec(coordinate.dec)

def test_all_ra_coordinates():
    expected = (19. + (30. / 60.) + (24. / 3600.)) * 15.

    for coord_value in [
            '19 30 24',
            '19:30:24',
            (19. + (30. / 60.) + (24. / 3600.)) * 15.,
            ]:
        assert Coordinate.sanitise_ra(coord_value) == expected

def test_all_dec_coordinates():
    expected = (46. + (50. / 60.) + (12. / 3600.))

    for coord_value in [
            '46 50 12',
            '46:50:12',
            '+46 50 12',
            (46. + (50. / 60.) + (12. / 3600.)),
            ]:
        assert Coordinate.sanitise_dec(coord_value) == expected

def test_negative_dec_coordinate():
    expected = -(46. + (50. / 60.) + (12. / 3600.))
    assert Coordinate.sanitise_dec('-46 50 12') == expected

def test_upload_format(coordinate):
    expected_ra = (19. + (30. / 60.) + (24. / 3600.)) * 15.
    expected_dec = (46. + (50. / 60.) + (12. / 3600.))
    assert coordinate.upload_string() == 'kepler_field {} {}'.format(expected_ra, expected_dec)



