import http.server
import socketserver
import requests

PORT = 8000

class MyHandler(http.server.SimpleHTTPRequestHandler):

    def do_POST(self):
        print("POST received")
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)

        hostname = '127.0.0.1:5000'
        print(self.path)
        url = 'http://{}{}'.format(hostname, self.path)
        req_header = self.headers

        # Call the target service
        resp = requests.post(url, headers=req_header, verify=False, data=post_data)

        self.send_response(resp.status_code)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(resp.content)

    def do_PUT(self):
        content_length = int(self.headers['Content-Length'])
        put_data = self.rfile.read(content_length)

        print("Put received\n")
        # Parse request
        hostname = '127.0.0.1:5000'
        url = 'http://{}{}'.format(hostname, self.path)
        print(url)
        req_header = self.headers

        # Call the target service
        resp = requests.put(url, headers=req_header, data=put_data)

        self.send_response(resp.status_code)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(resp.content)


    def do_DELETE(self):


        print("delete received\n")
        # Parse request
        hostname = '127.0.0.1:5000'
        url = 'http://{}{}'.format(hostname, self.path)
        req_header = self.headers

        # Call the target service
        resp = requests.delete(url, headers=req_header)

        self.send_response(resp.status_code)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(resp.content)

    def do_GET(self, body=True):
        if 'local-land-charges' in self.path:
            print("GET recieved")
            # Parse request
            hostname = '127.0.0.1:5000'
            url = 'http://{}{}'.format(hostname, self.path)
            print(url)
            req_header = self.headers
    
            # Call the target service
            resp = requests.get(url, headers=req_header, verify=False)
    
            # Respond with the requested data
            self.send_response(resp.status_code)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(resp.content)
        else:
            f = self.send_head()
            if f:
                try:
                    self.copyfile(f, self.wfile)
                finally:
                    f.close()

Handler = MyHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("serving at port", PORT)
    httpd.serve_forever()
