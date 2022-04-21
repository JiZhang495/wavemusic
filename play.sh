#!/usr/bin/env bash

python3 examples/simplest.py

case "$OSTYPE" in
  linux*)   aplay music.wav ;;
  darwin*)  afplay music.wav ;;
  *)        echo "unsupported OS: $OSTYPE" ;;
esac

