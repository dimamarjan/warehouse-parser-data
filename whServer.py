from http.server import BaseHTTPRequestHandler, HTTPServer
from json import dumps, dump, load
from ast import literal_eval as convert_to_dict


PORT = 8000
URL_ADDR = "10.62.1.27"

""" The HTTP request handler """


class RequestHandler(BaseHTTPRequestHandler):

    def _send_cors_headers(self):
        """ Sets headers required for CORS """
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET,POST,OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "x-api-key,Content-Type")

    def send_dict_response(self, d):
        """ Sends a dictionary (JSON) back to the client """
        self.wfile.write(bytes(dumps(d), "utf8"))

    def do_OPTIONS(self):
        self.send_response(200)
        self._send_cors_headers()
        self.end_headers()

    def do_GET(self):
        self.send_response(200)
        self._send_cors_headers()
        self.end_headers()

        print()
        with open("data.json", "r", encoding="utf-8") as f:
            data = load(f)
        self.wfile.write(bytes(dumps(data), "utf8"))

    def do_POST(self):
        self.send_response(200)
        self._send_cors_headers()
        self.send_header("Content-Type", "application/json")
        self.end_headers()

        dataLength = int(self.headers["Content-Length"])
        data = self.rfile.read(dataLength)
        rcv_data = convert_to_dict(data.decode("utf-8"))

        with open("data.json", "r", encoding="utf-8") as f:
            temp = load(f)

        for i in temp:
            if i['num'] == rcv_data['num']:
                temp[temp.index(i)] = rcv_data

        with open("data.json", "w", encoding="utf-8") as f:
            dump([*temp], f, ensure_ascii=False)
            print("data saved!")


def start_server():
    print("Starting server")
    httpd = HTTPServer((URL_ADDR, PORT), RequestHandler)
    print(f"Hosting server start on {URL_ADDR} on port {PORT}")
    httpd.serve_forever()


