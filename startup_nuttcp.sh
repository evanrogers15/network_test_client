#!/bin/bash

echo "Waiting for 2 seconds before starting NutTCP Server..."
sleep 2

nuttcp -S

echo "NutTCP Server started in the background"

# Keep the container running in the foreground and allow console interaction
/bin/bash
