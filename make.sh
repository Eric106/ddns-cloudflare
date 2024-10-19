#!/bin/bash
cd "$(dirname "$0")"
pip install --upgrade -r requirements.txt
pyinstaller --onefile ddns-cloudflare.py -y

# Detectar la arquitectura del sistema
arch=$(uname -m)

# Verificar la arquitectura y ejecutar el comando correspondiente
if [[ $arch == "aarch64"* ]]; then
    echo "Binary for ARM64 complied"
    mv dist/ddns-cloudflare bin/ddns-cloudflare_aarch64

elif [[ $arch == "x86_64" || $arch == "amd64" ]]; then
    echo "Binary for x86_64 complied"
    mv dist/ddns-cloudflare bin/ddns-cloudflare_x86_64
else
    echo "Architecture $arch not valid"
fi

rm dist/ -rf ; rm build/ -rf ; rm ddns-cloudflare.spec
