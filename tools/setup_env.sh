#!/bin/bash
# One-time per container: tools the pipeline needs that the base image lacks.
# Usage: tools/setup_env.sh [epubcheck_dir]   (default: /tmp/epubcheck)
set -e
if ! command -v tesseract >/dev/null ; then
  # cloud sessions pass only HTTPS through their proxy: plain-http apt mirrors hang (2026-11-19)
  for f in /etc/apt/sources.list /etc/apt/sources.list.d/*.sources /etc/apt/sources.list.d/*.list; do
    if [ -f "$f" ]; then sed -i 's|http://\(archive\|security\)\.ubuntu\.com|https://\1.ubuntu.com|g' "$f"; fi
  done
  timeout 600 apt-get update -q >/dev/null 2>&1
  apt-get install -y -q tesseract-ocr tesseract-ocr-eng >/dev/null 2>&1
fi
D=${1:-/tmp/epubcheck}
if [ ! -f "$D/epubcheck-5.1.0/epubcheck.jar" ]; then
  mkdir -p "$D"
  curl -L -sS "https://github.com/w3c/epubcheck/releases/download/v5.1.0/epubcheck-5.1.0.zip" -o "$D/e.zip"
  unzip -q -o "$D/e.zip" -d "$D"
fi
# python3 may be /usr/local (3.11) while apt's Pillow is for the system python: give it its own Pillow
python3 -c "import PIL.Image" 2>/dev/null || python3 -m pip install -q --target "$(python3 -c 'import sysconfig;print(sysconfig.get_paths()["purelib"])')" pillow
echo "ok: tesseract $(tesseract --version 2>&1 | head -1 | cut -d' ' -f2), epubcheck at $D/epubcheck-5.1.0/epubcheck.jar"
