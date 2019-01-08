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
    -d|--debug)
      DEBUG="$2"
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


export DEBUG=${DEBUG}

if [[ "${MODE}" = "server" ]]; then

  export CARO_FOLDER=/opt/catcher_rover
  source "$CARO_FOLDER"/setup_env.sh

  SEDEST="$CARO_DARKNET_FOLDER"/banana.data
  sed -i 's@ .*names$@ = '"$CARO_DARKNET_FOLDER"'/banana.names@g' ${SEDEST}

  if [[ ! -d "$CARO_INBOX_FOLDER" ]]; then
    mkdir -p "$CARO_INBOX_FOLDER"
  fi

  python3 $CARO_FOLDER/main.py

else
  CLIENT=1
fi

if [[ "${CLIENT}" = 1 ]]; then

  export CARO_FOLDER=$(pwd)
  source "$CARO_FOLDER"/setup_env.sh

  if [[ ! -d "$CARO_CAPTURE_FOLDER" ]]; then
    mkdir -p "$CARO_CAPTURE_FOLDER"
  fi

  sudo -E python3 main_client.py

fi
