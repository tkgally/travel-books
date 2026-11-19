#!/bin/bash
# One-time per container: tools the pipeline needs that the base image lacks.
# Usage: tools/setup_env.sh [epubcheck_dir]   (default: /tmp/epubcheck)
#        tools/setup_env.sh --apt-https-only [apt_dir]   (only the mirror rewrite; used by the tests)
set -e
# cloud sessions pass only HTTPS through their proxy: plain-http apt mirrors hang (2026-11-19).
# (Not `s|…\(a\|b\)…|`: with | as the delimiter, \| is a literal bar and nothing matched, so apt hung.)
apt_https() {
  local d=${1:-/etc/apt}
  for f in "$d"/sources.list "$d"/sources.list.d/*.sources "$d"/sources.list.d/*.list; do
    if [ -f "$f" ]; then sed -E -i 's#http://(archive|security)\.ubuntu\.com#https://\1.ubuntu.com#g' "$f"; fi
  done
}
if [ "$1" = "--apt-https-only" ]; then apt_https "$2"; exit 0; fi
if ! command -v tesseract >/dev/null ; then
  apt_https
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
