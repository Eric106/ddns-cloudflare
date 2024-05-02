#!/bin/bash
cd "$(dirname "$0")"
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
fi

rm dist/ -rf ; rm build/ -rf ; rm ddns-cloudflare.spec
