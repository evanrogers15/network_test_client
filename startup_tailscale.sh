#!/bin/bash

echo "Waiting for 2 seconds before starting Tailscale daemon..."
sleep 2

tailscaled &

echo "Tailscale daemon started in the background"

# Keep the container running in the foreground and allow console interaction
/bin/bash
