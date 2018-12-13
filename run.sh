#!/bin/bash

CLIENT=0

POSITIONAL=()
while [[ $# -gt 0 ]]
do

  key="$1"

  case $key in
    -m|--mode)
      MODE="$2"
      shift
      shift
      ;;
    *)
      POSITIONAL+=("$1")
      shift
      ;;
  esac
done

set -- "${POSITIONAL[@]}"

source setup_env.sh

if [[ "${MODE}" = "server" ]]; then
  if [[ ! -d "$CARO_INBOX_FOLDER" ]]; then
    mkdir -p "$CARO_INBOX_FOLDER"
  fi
  python3 main.py
else
  CLIENT=1
fi

if [[ "${CLIENT}" = 1 ]]; then
  if [[ ! -d "$CARO_CAPTURE_FOLDER" ]]; then
    mkdir -p "$CARO_CAPTURE_FOLDER"
  fi
  python3 main_client.py
fi
