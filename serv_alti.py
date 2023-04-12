import http.server
import json
import math
import socketserver
import struct

from osgeo import gdal, osr
from tqdm import tqdm


class Correction:
    def __init__(self):
        self.vrt = 'Out.vrt'

    def get_alti(self, lat, long):
        src_ds = gdal.Open(self.vrt, gdal.GA_ReadOnly)
        gt_forward = src_ds.GetGeoTransform()
        gt_reverse = gdal.InvGeoTransform(gt_forward)
        rb = src_ds.GetRasterBand(1)

        w_fromcrs = osr.SpatialReference()
        w_fromcrs.SetWellKnownGeogCS("WGS84")

        mp_transfo = osr.CoordinateTransformation(w_fromcrs, src_ds.GetSpatialRef())

        mx, my, _ = mp_transfo.TransformPoint(lat, long)

        # Convert from map to pixel coordinates.
        px, py = gdal.ApplyGeoTransform(gt_reverse, mx, my)
        px = math.floor(px)
        py = math.floor(py)

        structval = rb.ReadRaster(px, py, 1, 1, buf_type=gdal.GDT_Float32)
        intval = round(struct.unpack('f', structval)[0], 2)
        return intval


correction = Correction()

config = json.load(open('./config.json', mode='r'))


class HttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        prefix_alti = '/alti/'
        if self.path.startswith(prefix_alti):
            xml = '<reponse>'
            list_coords = [tuple(map(float, elem.split(','))) for elem in
                           self.path[len(prefix_alti):].split('coords=')[1].split(config['Sep'])]

            for lat, lon in tqdm(list_coords):
                elevation = correction.get_alti(lat, lon)
                xml += f'<elevation>{elevation}</elevation>\n'
            
            xml += '</reponse>'
            self.send_response(200)
            self.send_header('Content-type', 'application/xml')
            self.end_headers()
            self.wfile.write(bytes(xml, "utf8"))


PORT = config['PORT']
HOST = ""

with socketserver.TCPServer((HOST, PORT), HttpRequestHandler) as server_map:
    print(f"Server running on port {PORT} ==> http://localhost:{PORT}")
    server_map.serve_forever()