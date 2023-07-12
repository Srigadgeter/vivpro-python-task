import json
from urllib.parse import urlparse, parse_qs, unquote
from http.server import BaseHTTPRequestHandler, HTTPServer

# Define the path to the playlist.json file
json_file = 'playlist.json'

normalized_data = []

# Parse and normalize the JSON data
with open(json_file) as file:
    data = json.load(file)

    properties = list(data.keys())

    for i in range(len(data['id'])):
        item = {prop: data[prop][str(i)] for prop in properties}
        item["index"] = i
        normalized_data.append(item)
    
    # print('normalized_data >>', normalized_data)


# RequestHandler Class
class RequestHandler(BaseHTTPRequestHandler):
    def set_response(self, status_code=200, content_type='application/json'):
        self.send_response(status_code)
        self.send_header('Content-type', content_type)
        self.send_header('Access-Control-Allow-Origin', '*')  # Allow requests from any origin
        self.send_header('Access-Control-Allow-Methods', 'GET')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_OPTIONS(self):
        self.set_response()

    def do_GET(self):
        if self.path.startswith('/playlist'):
            parsed_url = urlparse(self.path)
            query_params = parse_qs(parsed_url.query)
            filters = {}
            for param, values in query_params.items():
                decoded_param = unquote(param)
                decoded_values = [unquote(value).lower() for value in values]
                filters[decoded_param] = decoded_values

            filtered_data = normalized_data
            for prop, values in filters.items():
                filtered_data = [
                    item for item in filtered_data if item.get(prop).lower() in values
                ]

            self.set_response()
            self.wfile.write(json.dumps(filtered_data).encode('utf-8'))
        else:
            self.set_response(404)
            self.wfile.write("Not found".encode('utf-8'))


def run(server_class=HTTPServer, handler_class=RequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Server running on port {port}")
    httpd.serve_forever()


if __name__ == '__main__':
    run()
