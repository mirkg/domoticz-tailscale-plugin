#!/bin/bash

JQ=/usr/bin/jq

CDIR=/opt/servers/certs

/usr/bin/sudo mkdir -p "$CDIR"
cd "$CDIR"

OUT=$(/usr/bin/sudo /usr/bin/tailscale cert --cert-file server.pem --key-file server.key $@ 2>&1)
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

/usr/bin/sudo chown -R pi:pi "$CDIR"
