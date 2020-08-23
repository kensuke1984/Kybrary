# v0.0.2
import math

EARTH_RADIUS = 6371
EQUATORIAL_RADIUS = 6378.137
POLAR_RADIUS = 6356.752314140356
E = 0.08181919104281514
FLATTENING = 1 / 298.257223563
N = 0.0016792443125758178


def epicentral_distance(pos1, pos2):
    theta1 = pos1.get_theta()
    theta2 = pos2.get_theta()
    phi1 = pos1.get_phi()
    phi2 = pos2.get_phi()
    # // cos a = a*b/|a|/|b|
    cos_a = math.sin(theta1) * math.sin(theta2) * math.cos(
        phi1 - phi2) + math.cos(theta1) * math.cos(theta2)
    return math.acos(cos_a)


def to_geocentric(geographic: float) -> float:
    """

    :param geographic: [rad]
    :return:
    """
    if 0.5 * math.pi < math.fabs(geographic):
        raise ValueError(
            "geographical latitude: " + str(
                geographic) + " must be [-pi/2, pi/2].")
    ratio = POLAR_RADIUS / EQUATORIAL_RADIUS
    return math.atan(ratio * ratio * math.tan(geographic))


class HorizontalPosition:
    def __init__(self, latitude: float, longitude: float):
        """

        :param latitude: geographic latitude [deg]
        :param longitude: [deg]
        """
        self.latitude = Latitude(latitude)
        self.longitude = Longitude(longitude)

    def get_theta(self):
        return self.latitude.theta

    def get_phi(self):
        return self.longitude.phi

    def epicentral_distance(self, pos):
        return epicentral_distance(self, pos)

    def __str__(self):
        return str(self.latitude.geographic) + ' ' + str(self.longitude.longitude)


class Location(HorizontalPosition):
    def __init__(self, latitude: float, longitude: float, radius: float):
        super().__init__(latitude, longitude)
        self.radius = radius

    def __str__(self):
        return super().__str__() + ' ' + str(self.radius)


class Latitude:
    def __init__(self, geographic):
        if not -90 <= geographic <= 90:
            raise ValueError(
                "The input latitude: {0} is invalid (must be [-90, 90]).".format(
                    geographic))
        self.geographic = geographic
        self.geocentric = to_geocentric(math.radians(geographic))
        self.theta = 0.5 * math.pi - self.geocentric


class Longitude:
    def __init__(self, longitude: float):
        """

        :param longitude: [deg]
        """
        if not -180 <= longitude < 360:
            raise ValueError(
                "The input longitude: " + str(
                    longitude) + " is invalid (must be [-180, 360).")
        if 180 < longitude:
            self.phi = math.radians(longitude - 360)
            self.longitude = -360 + longitude
        else:
            self.phi = math.radians(longitude)
            self.longitude = longitude

# def compute_epicentral_distance(lat1: float, lon1: float, lat2: float,
#                                 lon2: float):
#     theta1 = loc1.getTheta();
#     theta2 = loc2.getTheta();
#     phi1 = loc1.getPhi();
#     phi2 = loc2.getPhi();
#     // cos
#     a = a * b / | a | / | b |
#     double
#     cosAlpha = FastMath.sin(theta1) * FastMath.sin(theta2) * FastMath.cos(
#         phi1 - phi2) +
#     FastMath.cos(theta1) * FastMath.cos(theta2);
#
#     return FastMath.acos(cosAlpha)
