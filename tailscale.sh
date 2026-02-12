#!/bin/bash

JQ=/usr/bin/jq

OUT=$(/usr/bin/sudo /usr/bin/tailscale $@ 2>&1)
RC=$?
if [ "$RC" == "0" ]; then
    OOUT=$(echo "$OUT" | $JQ -c 2>&1)
    RC=$?
    if [ "$RC" == "0" ]; then
        if [ "$OOUT" == "" ]; then
            echo "{}"
        else
            echo "$OOUT"
        fi
    else
        echo "$OUT" | $JQ -s -R 'split("\n") | .[:-1] | join("\n")' | $JQ '{error: .}' | $JQ -c    
    fi
else
    echo "$OUT" | $JQ -s -R 'split("\n") | .[:-1] | join("\n")' | $JQ '{error: .}' | $JQ -c
fi
