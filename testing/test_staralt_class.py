from staralt.staralt import *
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
@mock.patch.object(StarAlt, 'invalid_mode', return_value=False)
def test_success_with_valid_parameters(mock_mode, mock_staralt, mock_get):
    s = StarAlt()
    s.save_image("image.gif")

@mock.patch.object(StarAlt, 'invalid_mode', return_value=False)
def test_insufficient_parameters(mock_mode):
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

def test_min_elevation():
    s = StarAlt()
    s.min_elevation = 30
    assert s._parse_min_elevation() == {
            'form[minangle]': '30'}

@mock.patch('requests.get')
@mock.patch.object(StarAlt, 'insufficient_parameters', return_value=False)
def test_invalid_mode(mock_params, mock_get):
    s = StarAlt()
    s.mode = 'not_valid_mode'
    with pytest.raises(InvalidMode) as err:
        s.save_image("output.gif")

@mock.patch('requests.get')
@mock.patch.object(StarAlt, 'insufficient_parameters', return_value=False)
def test_valid_mode(mock_parameters, mock_requests):
    s = StarAlt()
    s.mode = "starobs"
    s.save_image("output.gif")

@mock.patch('requests.get')
def test_valid_site_coordinates(mock_get):
    s = StarAlt()
    s.site_location = {'latitude': 6., 'longitude': 46.,
            'altitude': 400, 'utc-offset': 1}

    result = s._parse_site()
    assert result == {
            'form[sitecoord]': '{} {} {} {}'.format(6., 46., 400, 1)}

def test_alternate_constructors():
    fn_names = ['starobs', 'startrack', 'starmult', 'staralt']
    for name in fn_names:
        fn = getattr(StarAlt, name)
        s = fn()
        assert s.mode == name
