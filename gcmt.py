# v0.0.1
from datetime import datetime

import environment
from geometry import Location

catalog_path = environment.kibrary_home.joinpath('share', 'globalcmt.catalog')


def of(gcmtid: str):
    for ndk in ndks:
        if ndk.id == gcmtid:
            return ndk
    raise RuntimeError('No information for ' + gcmtid)


class NDK:

    def __init__(self, lines):
        from util import m0_to_mw
        """
        Creates an NDK from the lines
        :param lines: 5 lines for a NDK
        """
        if lines is None or not len(lines) == 5:
            raise ValueError("Input for NDK must be in the certain style (5 lines)")

        # line 0
        parts = lines[0].split()
        if lines[0].startswith(' '):
            parts = [' ' * 4] + parts
        self.hypocenter_reference_catalog = parts[0]  # [0-3]
        self.reference_date_time = datetime.strptime(' '.join(parts[1:3]), "%Y/%m/%d %H:%M:%S.%f")
        self.hypocenter_location = Location(float(parts[3]), float(parts[4]), 6371 - float(parts[5]))
        self.mb = float(parts[6])
        self.ms = float(parts[7])
        self.geographical_location = lines[0][56:].strip()

        # line 1
        parts = lines[1].split()
        self.id = parts[0][1:]  # TODO
        bsm_parts = lines[1][17:61].replace("B:", "").replace("S:", "").replace("M:", "").split()
        self.b = []
        self.b.append(int(bsm_parts[0]))
        self.b.append(int(bsm_parts[1]))
        self.b.append(int(bsm_parts[2]))
        self.s = []
        self.s.append(int(bsm_parts[3]))
        self.s.append(int(bsm_parts[4]))
        self.s.append(int(bsm_parts[5]))
        self.m = []
        self.m.append(int(bsm_parts[6]))
        self.m.append(int(bsm_parts[7]))
        self.m.append(int(bsm_parts[8]))
        cmt_parts = lines[1][61:].split()
        self.cmt_type = int(cmt_parts[1])
        self.moment_rate_function = cmt_parts[2][0:5]
        self.half_duration_moment_rate_function = float(cmt_parts[3])

        # line 2
        parts = lines[2].split()
        self.time_difference = float(parts[1])
        self.centroid_location = Location(float(parts[3]), float(parts[5]), 6371 - float(parts[7]))
        self.depth_type = parts[9]
        self.time_stamp = parts[10]

        # line 3
        parts = lines[3].split()
        self.moment_exponent = int(parts[0])
        self.mrr = float(parts[1])
        self.mtt = float(parts[3])
        self.mpp = float(parts[5])
        self.mrt = float(parts[7])
        self.mrp = float(parts[9])
        self.mtp = float(parts[11])

        # line 4
        parts = lines[4].split()
        self.version_code = parts[0]
        self.scalar_moment = float(parts[10]) * 10 ** self.moment_exponent
        # 10**5 dyne = N, 100 cm = 1m
        self.m0 = self.scalar_moment / 100000 / 100
        self.mw = round(m0_to_mw(self.m0), 1)
        self.eigenValue0 = float(parts[1])
        self.eigenValue1 = float(parts[4])
        self.eigenValue2 = float(parts[7])
        self.plunge0 = float(parts[2])
        self.plunge1 = float(parts[5])
        self.plunge2 = float(parts[8])
        self.azimuth0 = float(parts[3])
        self.azimuth1 = float(parts[6])
        self.azimuth2 = float(parts[9])
        self.strike0 = int(parts[11])
        self.dip0 = int(parts[12])
        self.rake0 = int(parts[13])
        self.strike1 = int(parts[14])
        self.dip1 = int(parts[15])
        self.rake1 = int(parts[16])


ndks = []


def _read_catalog():
    with open(_get_catalog()) as f:
        all_lines = f.readlines()
        n = len(all_lines)
        if not n % 5 == 0:
            raise RuntimeError('The catalog file is broken. ' + f.name)
        for i in range(int(n / 5)):
            ndks.append(NDK(all_lines[5 * i:5 * i + 5]))
    pass


def _get_catalog():
    from pathlib import Path
    if not catalog_path.exists():
        file = _download_catalog()
        catalog_path.parent.mkdir(parents=True, exist_ok=True)
        Path(file).replace(catalog_path)
    return catalog_path


def _download_catalog():
    import urllib.request
    import tempfile
    catalog_url = 'https://bit.ly/3bdGQji'
    temp_file = tempfile.mkstemp(suffix='.cat')
    urllib.request.urlretrieve(catalog_url, temp_file[1])
    return temp_file[1]


_read_catalog()
