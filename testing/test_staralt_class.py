from staralt.staralt import StarAlt, InsufficientParameters
import pytest
import mock
from datetime import date

@mock.patch.object(StarAlt, 'insufficient_parameters', return_value=True)
def test_fail_with_invalid_parameters(mock_staralt):
    s = StarAlt()

    with pytest.raises(InsufficientParameters) as err:
        s.save_image("image.gif")

@mock.patch('requests.get')
@mock.patch.object(StarAlt, 'insufficient_parameters', return_value=False)
def test_success_with_valid_parameters(mock_staralt, mock_get):
    s = StarAlt()
    s.save_image("image.gif")

def test_insufficient_parameters():
    s = StarAlt()
    assert s.insufficient_parameters() == False

@mock.patch('staralt.coordinate.Coordinate')
def test_sufficient_parameters(mock_coordinate):
    s = StarAlt()
    s.mode = 'starobs'
    s.date = date.today()
    s.coordinates = [mock_coordinate, ]

    assert s.moon_distance == True
    assert s.min_elevation == 30

    assert s.insufficient_parameters() == True

def test_parse_date():
    s = StarAlt()
    s.date = date(2014, 5, 1)
    result = s._parse_date()
    assert result == {
            'form[day]': '1',
            'form[month]': '5',
            'form[year]': '2014',
            }

@mock.patch('staralt.coordinate.Coordinate')
def test_parse_coordinates(mock_coordinate):
    mock_coordinate.upload_string.return_value = 'kepler_field 30.0 49.0'
    s = StarAlt()
    s.coordinates = [mock_coordinate, mock_coordinate]

    assert s._parse_coordinates() == {'form[coordlist]': 
    'kepler_field 30.0 49.0\nkepler_field 30.0 49.0'}

def test_parse_moon_distance():
    s = StarAlt()
    s.moon_distance = True

    assert s._parse_moon_distance() == {
            'form[paramdist]': '2',
            }

