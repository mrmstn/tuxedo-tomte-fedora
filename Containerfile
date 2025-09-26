# Multi-stage build for TUXEDO Tomte on Fedora 42

# Build stage
FROM registry.fedoraproject.org/fedora:42 AS builder

# Install build dependencies and required Perl modules
RUN dnf update -y && dnf install -y \
    perl-interpreter \
    perl-File-FcntlLock \
    dpkg-perl \
    perl-JSON \
    perl-Config-Tiny \
    perl-libintl-perl \
    perl-File-Slurp \
    perl-Readonly \
    perl-autovivification \
    perl-Parse-EDID \
    perl-Time-HiRes \
    perl-FindBin \
    perl-autodie \
    PackageKit-command-not-found \
    gettext \
    rpm-build \
    rpm-devel \
    rpmdevtools \
    systemd-rpm-macros \
    && dnf clean all

# Set up RPM build environment
RUN rpmdev-setuptree

# Copy source files
WORKDIR /build
COPY . .
RUN chmod -R 755 /build

# Compile translation files
RUN for po in po/*.po; do \
        lang=$(basename $po .po); \
        mkdir -p usr/share/locale/$lang/LC_MESSAGES; \
        msgfmt --output-file=usr/share/locale/$lang/LC_MESSAGES/tomte.mo $po; \
    done

# Skip Perl syntax check for now - will be validated at runtime

# Build RPM package
COPY tuxedo-tomte.spec /root/rpmbuild/SPECS/
RUN cd /tmp && \
    cp -r /build tuxedo-tomte-2.55.0 && \
    tar -czf /root/rpmbuild/SOURCES/tuxedo-tomte.tar.gz \
        --exclude='.git*' \
        --exclude='*.swp' \
        --exclude='Containerfile' \
        --exclude='output' \
        tuxedo-tomte-2.55.0 && \
    echo "Checking tarball contents:" && \
    tar -tzf /root/rpmbuild/SOURCES/tuxedo-tomte.tar.gz | head -10
RUN rpmbuild -ba /root/rpmbuild/SPECS/tuxedo-tomte.spec

# Output stage
FROM scratch AS output
COPY --from=builder /root/rpmbuild/RPMS/noarch/*.rpm /
COPY --from=builder /root/rpmbuild/SRPMS/*.rpm /