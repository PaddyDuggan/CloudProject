import requests

def test_validate_ips():
    url = "http://localhost:5000/validate_ips"

    # Test with valid IPv4 addresses
    params = {'items': '192.168.1.1,10.0.0.1'}
    response = requests.get(url, params=params)
    assert response.status_code == 200
    data = response.json()
    print(data)
    assert data['total_valid_ips'] == 2
    assert "192.168.1.1 -> valid" in data['results']
    assert "10.0.0.1 -> valid" in data['results']

    # Test with valid IPv6 addresses
    params = {'items': '2001:0db8:85a3:0000:0000:8a2e:0370:7334,::1'}
    response = requests.get(url, params=params)
    assert response.status_code == 200
    data = response.json()
    print(data)
    assert data['total_valid_ips'] == 2
    assert "2001:0db8:85a3:0000:0000:8a2e:0370:7334 -> valid" in data['results']
    assert "::1 -> valid" in data['results']

    # Test with invalid IP addresses
    params = {'items': '999.999...999.999,abcd:1234:a:b:c:d:1:2:3'}
    response = requests.get(url, params=params)
    assert response.status_code == 200
    data = response.json()
    print(data)
    assert data['total_valid_ips'] == 0
    assert "999.999...999.999 -> invalid" in data['results']
    assert "abcd:1234:a:b:c:d:1:2:3 -> invalid" in data['results']

    # Test with mixed valid and invalid IPs
    params = {'items': '192.168.1.1,10.0.0.1,999.999.999.999.999,abcd'}
    response = requests.get(url, params=params)
    assert response.status_code == 200
    data = response.json()
    print(data)
    assert data['total_valid_ips'] == 2
    assert "192.168.1.1 -> valid" in data['results']
    assert "10.0.0.1 -> valid" in data['results']
    assert "999.999.999.999.999 -> invalid" in data['results']
    assert "abcd -> invalid" in data['results']

if __name__ == "__main__":
    test_validate_ips()
    print("All tests passed!")
