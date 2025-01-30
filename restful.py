
import argparse
import requests
import json
import csv
import sys


BASE_URL = "https://jsonplaceholder.typicode.com"

class RestClient:
    def __init__(self, method, endpoint, data=None, output=None):
        self.method = method.upper()
        self.url = f"{BASE_URL}{endpoint}"
        self.data = data
        self.output = output


    def send_request(self):
        try:
            if self.method == "GET":
                response = requests.get(self.url)
            elif self.method == "POST":
                headers = {'Content-Type': 'application/json'}
                response = requests.post(self.url, headers=headers, data=json.dumps(self.data))
            else:
                print("Unsupported method. Only GET and POST are allowed.")
                sys.exit(1)
            
            self.handle_response(response)
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            sys.exit(1)

    def handle_response(self, response):
        print(f"HTTP Status: {response.status_code}")
    
        if not response.ok:
            print("Error: ", response.text)
            sys.exit(1)
        
        data = response.json()
    
        if self.output:
            if self.output.endswith(".json"):
                self.save_json(data)
            elif self.output.endswith(".csv"):
                self.save_csv(data)
            else:
                print("Unsupported output format. Use .json or .csv")
                sys.exit(1)
        else:
            print(json.dumps(data, indent=4))
    

    def save_json(self, data):
        with open(self.output, "w") as f:
            json.dump(data, f, indent=4)
        print(f"Response saved to {self.output}")

    def save_csv(self, data):
        if isinstance(data, dict):
            data = [data]

        keys = data[0].keys()
        with open(self.output, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(data)
        print(f"Response saved to {self.output}")

def main():
    parser = argparse.ArgumentParser(description="Simple REST client for JSONPlaceholder API")
    parser.add_argument("method", choices=["get", "post"], help="Request method")
    parser.add_argument("endpoint", help="Request endpoint URI fragment")
    parser.add_argument("-d", "--data", type=json.loads, help="Data to send with POST request (JSON format)")
    parser.add_argument("-o", "--output", help="Output file (.json or .csv)")
    
    args = parser.parse_args()
    
    client = RestClient(args.method, args.endpoint, args.data, args.output)
    client.send_request()



if __name__ == "__main__":
    main()