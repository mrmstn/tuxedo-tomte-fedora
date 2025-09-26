Name:           tuxedo-tomte
Version:        2.55.0
Release:        1%{?dist}
Summary:        Little helper that provides services, updates and fixes for TUXEDO devices

License:        GPL-3.0-or-later
URL:            https://www.tuxedocomputers.com
Source0:        %{name}.tar.gz

BuildArch:      noarch
BuildRequires:  gettext
BuildRequires:  systemd-rpm-macros

Requires:       perl-interpreter
Requires:       perl-File-FcntlLock
Requires:       perl-JSON
Requires:       perl-Config-Tiny
Requires:       perl-libintl-perl
Requires:       perl-File-Slurp
Requires:       perl-Readonly
Requires:       perl-autovivification
Requires:       perl-Parse-EDID
Requires:       perl-Time-HiRes
Requires:       perl-FindBin
Requires:       perl-autodie
Requires:       perl-File-Copy
Requires:       PackageKit-command-not-found

%description
TUXEDO Tomte is a little helper that provides services, updates and fixes for
TUXEDO devices in the background. It does not send any information, telemetry
data or similar stuff out!

TUXEDO Tomte ist ein kleiner Helfer, der Dienste, Updates und Fixes für
TUXEDO-Geräte im Hintergrund bereitstellt. Es sendet keine Informationen,
Telemetriedaten oder ähnliches zurück!

%prep
%setup -q

%build
# Compile translation files
for po in po/*.po; do
    lang=$(basename $po .po)
    mkdir -p usr/share/locale/$lang/LC_MESSAGES
    msgfmt --output-file=usr/share/locale/$lang/LC_MESSAGES/tomte.mo $po
done

%install
# Create directories
install -d %{buildroot}%{_bindir}
install -d %{buildroot}%{_datadir}/%{name}
install -d %{buildroot}%{_datadir}/bash-completion/completions
install -d %{buildroot}%{_mandir}/man1
install -d %{buildroot}%{_mandir}/de/man1
install -d %{buildroot}%{_sysconfdir}/logrotate.d
install -d %{buildroot}%{_datadir}/perl5
install -d %{buildroot}%{_unitdir}

# Install files according to debian/install
install -m 755 src/tuxedo-tomte %{buildroot}%{_bindir}/
install -m 644 misc/nh5xax-1.aml %{buildroot}%{_datadir}/%{name}/
install -m 755 misc/tuxedo-corefix-clevo-nh5xax %{buildroot}%{_datadir}/%{name}/
install -m 644 misc/tuxedo-tomte %{buildroot}%{_datadir}/bash-completion/completions/
install -m 644 misc/tomte %{buildroot}%{_datadir}/bash-completion/completions/
install -m 644 man/tuxedo-tomte.1 %{buildroot}%{_mandir}/man1/
install -m 644 man/de/tuxedo-tomte.1 %{buildroot}%{_mandir}/de/man1/
install -m 644 logrotate/tuxedo-tomte %{buildroot}%{_sysconfdir}/logrotate.d/
cp -r Tomte %{buildroot}%{_datadir}/perl5/

# Install systemd service and timer
install -m 644 debian/tuxedo-tomte.service %{buildroot}%{_unitdir}/
install -m 644 debian/tuxedo-tomte.timer %{buildroot}%{_unitdir}/

# Install translation files
cp -r usr/share/locale %{buildroot}%{_datadir}/

%post
%systemd_post %{name}.service %{name}.timer

%preun
%systemd_preun %{name}.service %{name}.timer

%postun
%systemd_postun_with_restart %{name}.service %{name}.timer

%files
%license copyright
%doc README.md
%{_bindir}/tuxedo-tomte
%{_datadir}/%{name}/
%{_datadir}/bash-completion/completions/tuxedo-tomte
%{_datadir}/bash-completion/completions/tomte
%{_mandir}/man1/tuxedo-tomte.1*
%{_mandir}/de/man1/tuxedo-tomte.1*
%config(noreplace) %{_sysconfdir}/logrotate.d/tuxedo-tomte
%{_datadir}/perl5/Tomte/
%{_unitdir}/tuxedo-tomte.service
%{_unitdir}/tuxedo-tomte.timer
%{_datadir}/locale/*/LC_MESSAGES/tomte.mo

%changelog
* Thu Jul 17 2025 E. Mohr <e.mohr@tuxedocomputers.com> - 2.55.0-1
- added Linux Mint 22.2

* Wed Jul 10 2025 E. Mohr <e.mohr@tuxedocomputers.com> - 2.54.1-1
- added module krackanpointusb4suspendfix
- added module krackanpointusb4suspendfix to TUXEDO Nano Pro Gen14 AMD

* Tue Jul 02 2025 E. Mohr <e.mohr@tuxedocomputers.com> - 2.54.0-1
- Initial RPM package for Fedora