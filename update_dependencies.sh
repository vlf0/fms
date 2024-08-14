#!/bin/bash

PREVIOUS_DEPS=${DEPS_AMOUNT:-0}

CURRENT_DEPS=$(wc -l < requirements.txt)

export DEPS_AMOUNT=$CURRENT_DEPS

if [ "$CURRENT_DEPS" -gt "$PREVIOUS_DEPS" ]; then

  DIFFERENCE=$((CURRENT_DEPS - PREVIOUS_DEPS))

  NEW_DEPENDENCIES=$(tail -n "$DIFFERENCE" requirements.txt)

  source venv/bin/activate

  pip3 install $NEW_DEPENDENCIES

  deactivate
fi