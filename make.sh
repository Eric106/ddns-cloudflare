pyinstaller --onefile ddns-cloudflare.py -y
mv dist/ddns-cloudflare ./
rm dist/ -rf