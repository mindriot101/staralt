class CannotParseCoordinate(RuntimeError): pass

class Coordinate(object):
    def __init__(self, **kwargs):
        for kwarg in kwargs:
            setattr(self, kwarg, kwargs[kwarg])

    @classmethod
    def sanitise_ra(cls, ra):
        out = cls._sanitise_coordinate(ra) * 15.
        return out if out <= 360 else out / 15.

    @classmethod
    def sanitise_dec(cls, dec):
        return cls._sanitise_coordinate(dec)

    @staticmethod
    def _sanitise_coordinate(coordinate):
        try:
            return float(coordinate)
        except ValueError:
            if ':' in coordinate:
                parts = coordinate.split(':')
            elif ' ' in coordinate:
                parts = coordinate.split()
            else:
                raise CannotParseCoordinate("cannot parse {}".format(coordinate))

            parts = map(float, parts)
            if parts[0] < 0:
                return -(-parts[0] + (parts[1] / 60.) + (parts[2] / 3600.))
            else:
                return (parts[0] + (parts[1] / 60.) + (parts[2] / 3600.))

    def upload_string(self):
        upload_ra = self.sanitise_ra(self.ra)
        upload_dec = self.sanitise_dec(self.dec)
        return "{name} {upload_ra} {upload_dec}".format(
                name=self.name,
                upload_ra=upload_ra,
                upload_dec=upload_dec)
