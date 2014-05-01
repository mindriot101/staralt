class InsufficientParameters(RuntimeError):
    def __init__(self):
        super(InsufficientParameters, self).__init__("Insufficient parameters "
        "set on StarAlt class")

class InvalidMode(RuntimeError):
    def __init__(self, mode_parameter):
        super(InvalidMode, self).__init__("Invalid mode parameter: {0}".format(mode_parameter))

class StarAlt(object):
    DEFAULT_MOON_DISTANCE = True
    DEFAULT_MIN_ELEVATION = 30

    REQUIRED_PARAMS = ['mode', 'date', 'coordinates',
            'moon_distance', 'min_elevation']

    ALLOWED_MODES = ['starobs', 'startrack', 'starmult', 'staralt']

    def __init__(self):
        self.moon_distance = self.DEFAULT_MOON_DISTANCE
        self.min_elevation = self.DEFAULT_MIN_ELEVATION
        self.mode = None
        self.date = None
        self.coordinates = []

    @classmethod
    def starobs(cls):
        s = cls()
        s.mode = 'starobs'
        return s

    @classmethod
    def startrack(cls):
        s = cls()
        s.mode = 'startrack'
        return s

    @classmethod
    def starmult(cls):
        s = cls()
        s.mode = 'starmult'
        return s

    @classmethod
    def staralt(cls):
        s = cls()
        s.mode = 'staralt'
        return s

    def save_image(self, filename):
        if self.insufficient_parameters():
            raise InsufficientParameters

        if self.invalid_mode():
            raise InvalidMode(self.mode)

    def insufficient_parameters(self):
        return all(getattr(self, param) is not None
                for param in self.REQUIRED_PARAMS)

    def invalid_mode(self):
        if self.mode not in self.ALLOWED_MODES:
            raise InvalidMode(self.mode)

    def _parse_date(self):
        return {
                'form[day]': str(self.date.day),
                'form[month]': str(self.date.month),
                'form[year]': str(self.date.year),
                }

    def _parse_coordinates(self):
        return {
                'form[coordlist]':
                '\n'.join([c.upload_string() for c in self.coordinates])}

    def _parse_moon_distance(self):
        if self.moon_distance:
            return {'form[paramdist]': '2'}

    def _parse_min_elevation(self):
        return {'form[minangle]': str(self.min_elevation)}

    def _parse_site(self):
        latitude, longitude = self.site_location['latitude'], self.site_location['longitude']
        altitude, utc_offset = self.site_location.get('altitude', ''), self.site_location.get('utc-offset', '')
        return {
                'form[sitecoord]':
                "{latitude} {longitude} {altitude} {utc_offset}".format(
                    latitude=latitude,
                    longitude=longitude,
                    altitude=altitude,
                    utc_offset=utc_offset).strip()
                }
