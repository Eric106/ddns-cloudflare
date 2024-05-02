#!/bin/bash
cd "$(dirname "$0")"
# Detectar la arquitectura del sistema
arch=$(uname -m)

# Verificar la arquitectura y ejecutar el comando correspondiente
if [[ $arch == "aarch64"* ]]; then
    bin/ddns-cloudflare_aarch64

elif [[ $arch == "x86_64" || $arch == "amd64" ]]; then
    bin/ddns-cloudflare_x86_64
else
    echo "Architecture $arch not valid"
fi