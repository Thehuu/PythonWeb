import mmh3
import requests
import base64

# URL của logo
url = 'https://www.saputoranch.com/logo.png'

# Tải nội dung từ URL
response = requests.get(url)

if response.status_code == 200:
    # Mã hóa logo sang base64
    favicon = base64.encodebytes(response.content)
    # Tính toán hash bằng mmh3
    hash_value = mmh3.hash(favicon)
    print(f"Hash của logo: {hash_value}")
else:
    print(f"Không thể tải logo. HTTP Status: {response.status_code}")
