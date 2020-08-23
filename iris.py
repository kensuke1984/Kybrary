# v0.0.1
class IrisStation:
    def __init__(self, network: str, name: str, lat: float, lon: float,
                 elevation: float, location: str, start, end):
        self.network = network
        self.name = name
        self.lat = lat
        self.lon = lon
        self.elevation = elevation
        self.location = location
        self.start = start
        self.end = end
        pass

    def __str__(self):
        return '{0} {1} {2} {3} {4} {5} {6} {7}'.format(self.network, self.name,
                                                        self.lat, self.lon,
                                                        self.elevation,
                                                        self.location,
                                                        self.start, self.end)


class IrisEvent:
    def __init__(self, time, mag: float, lat: float, lon: float, depth: float,
                 region: str, usgs_id: str, timestamp: int):
        self.time = time
        self.mag = mag
        self.lat = lat
        self.lon = lon
        self.depth = depth
        self.region = region
        self.usgs_id = usgs_id
        self.timestamp = timestamp

    def __str__(self):
        return '{0} {1} {2} {3} {4} {5} {6} {7}'.format(self.time, self.mag,
                                                        self.lat, self.lon,
                                                        self.depth, self.region,
                                                        self.usgs_id,
                                                        self.timestamp)
