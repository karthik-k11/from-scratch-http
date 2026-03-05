class HttpRequest:
    def __init__(self, raw_request: str):
        self.raw_request = raw_request
        self.method = None
        self.path = None
        self.version = None
        self.headers = {}
        self.body = None
        self.query_params = {}

        self.parse()

    def parse(self):
        lines = self.raw_request.split("\r\n")

        ##Request Line
        request_line = lines[0]
        self.method, full_path, self.version = request_line.split()

        #Query paeameters
        if "?" in full_path:
            path, query_string = full_path.split("?", 1)
            self.path = path

            pairs = query_string.split("&")

            for pair in pairs:
                if "=" in pair:
                    key, value = pair.split("=", 1)
                    self.query_params[key] = value
        else:
            self.path = full_path

        ##Headers
        i = 1
        while lines[i] != "":
            key, value = lines[i].split(":", 1)
            self.headers[key.strip()] = value.strip()
            i += 1

        ##Body
        body_index = i + 1
        if body_index < len(lines):
            self.body = "\n".join(lines[body_index:])