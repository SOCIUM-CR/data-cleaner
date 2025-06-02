#!/usr/bin/env python3
# Test file with sensitive data

import requests

def main():
    # Contact information
    email = "john.doe@company.com"
    phone = "+1-555-1234"
    
    # API endpoint
    api_url = "https://api.example.com/v1/users"
    
    # IP address for server
    server_ip = "192.168.1.100"
    
    print(f"Sending request to {api_url}")
    print(f"Contact: {email}, {phone}")
    print(f"Server: {server_ip}")

if __name__ == "__main__":
    main()
