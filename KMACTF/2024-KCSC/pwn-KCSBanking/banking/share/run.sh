#!/bin/sh

socat tcp-listen:10002,fork,reuseaddr exec:/app/banking 2>/dev/null