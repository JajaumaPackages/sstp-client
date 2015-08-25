%global _hardened_build 1
%global __provides_exclude ^sstp-pppd-plugin\\.so$
%global ppp_epoch %(rpm -q ppp > /dev/null && rpm -q ppp --qf '%{EPOCH}' || exit 1)
%global ppp_version %(rpm -q ppp > /dev/null && rpm -q ppp --qf '%{VERSION}' || exit 1)
%global ppp_release %(rpm -q ppp > /dev/null && rpm -q ppp --qf '%{RELEASE}' || exit 1)
%global commonname sstpc

Name:           sstp-client
Version:        1.0.10
Release:        1%{?dist}
Summary:        Secure Socket Tunneling Protocol(SSTP) Client
License:        GPLv2+
Url:            http://sstp-client.sourceforge.net
Source0:        http://downloads.sourceforge.net/project/%{name}/%{name}/%{version}/%{name}-%{version}.tar.gz
BuildRequires:  libevent-devel
BuildRequires:  openssl-devel
BuildRequires:  ppp
BuildRequires:  ppp-devel
Requires(pre):  shadow-utils
# PPP bumps location of the libraries with every new release, I can't promise
# the code is 100% compatible with new ppp always, so hardcode the version
# and manually rebuild after every new ppp package in Fedora.
Requires:       ppp = %{ppp_epoch}:%{ppp_version}-%{ppp_release}

%description
This is a client for the Secure Socket Tunneling Protocol(SSTP). It can be 
used to establish a SSTP connection to a Windows Server.

Features:
* Establish a SSTP connection to a remote Windows 2k8 server.
* Async PPP support.
* Similar command line handling as pptp-client for easy integration with 
pon/poff scripts.
* Basic HTTP Proxy support.
* Certficate handling and verification.
* IPv6 support.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       ppp-devel%{?_isa} = %{ppp_epoch}:%{ppp_version}-%{ppp_release}

%description    devel
This package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q

%build
%configure --disable-static                                          \
           --disable-silent-rules                                    \
           --with-libevent=2                                         \
           --with-pppd-plugin-dir="%{_libdir}/pppd/%{ppp_version}"   \
           --with-runtime-dir="%{_localstatedir}/run/%{commonname}"  \
           --enable-user=yes                                         \
           --enable-group=yes

%make_build

%install
%make_install

# Use %%doc to handle documentation.
rm -frv %{buildroot}%{_docdir}

find %{buildroot} -name '*.la' -delete -print

%check
make check

%pre
getent group %{commonname} >/dev/null || groupadd -r %{commonname}
getent passwd %{commonname} >/dev/null || \
    useradd -r -g %{commonname} \
    -d %{_localstatedir}/run/%{commonname} \
    -s /sbin/nologin \
    -c "Secure Socket Tunneling Protocol(SSTP) Client" %{commonname}
exit 0

%post -p /sbin/ldconfig

%postun
/sbin/ldconfig -p
rm -rf %{_localstatedir}/run/%{commonname}

%files
%doc AUTHORS README debian/changelog TODO USING *.example
%license COPYING
%{_sbindir}/sstpc
%{_libdir}/libsstp_api-0.so
%{_libdir}/pppd/%{ppp_version}/sstp-pppd-plugin.so
%{_mandir}/man8/sstpc.8*

%files devel
%{_includedir}/sstp-client/
%{_libdir}/libsstp_api.so
%{_libdir}/pkgconfig/sstp-client-1.0.pc

%changelog
* Sat Jun 20 2015 Christopher Meng <rpm@cicku.me> - 1.0.10-1
- Update to 1.0.10

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.9-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.9-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Jun 27 2014 Christopher Meng <rpm@cicku.me> - 1.0.9-6
- Rebuild against new ppp.

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.9-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Aug 01 2013 Christopher Meng <rpm@cicku.me> - 1.0.9-4
- Fix library issue.

* Fri Jul 26 2013 Christopher Meng <rpm@cicku.me> - 1.0.9-3
- Filter out the private library.

* Tue Jul 23 2013 Christopher Meng <rpm@cicku.me> - 1.0.9-2
- Remove Rpath.

* Sun Feb 03 2013 Christopher Meng <rpm@cicku.me> - 1.0.9-1
- Initial Package.
