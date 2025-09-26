#!/bin/bash

# Build script for TUXEDO Tomte in Fedora container

set -e

echo "Building TUXEDO Tomte RPM package in Fedora 42 container..."

# Create output directory
mkdir -p output

# Build the container with multi-stage output
echo "Building container and extracting RPM packages..."
podman build \
    --target output \
    --output type=local,dest=./output \
    -f Containerfile \
    .

echo "Build complete! RPM packages are in the ./output directory:"
ls -la output/

echo ""
echo "To install the package on Fedora, run:"
echo "  sudo dnf install output/tuxedo-tomte-*.noarch.rpm"
echo ""
echo "To test the package in a clean container:"
echo "  podman run --rm -v \$(pwd)/output:/rpms:ro registry.fedoraproject.org/fedora:42 \\"
echo "    sh -c 'dnf install -y /rpms/tuxedo-tomte-*.noarch.rpm && tuxedo-tomte --help'"