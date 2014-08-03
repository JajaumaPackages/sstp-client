%global _hardened_build 1

%global __provides_exclude ^sstp-pppd-plugin\\.so$

%global ppp_version %(rpm -q ppp --queryformat '%{VERSION}')

Name:           sstp-client
Version:        1.0.9
Release:        6%{?dist}
Summary:        Secure Socket Tunneling Protocol (SSTP) Client
License:        GPLv2+
Url:            http://sstp-client.sourceforge.net
Source0:        http://downloads.sourceforge.net/project/%{name}/%{name}/%{version}/%{name}-%{version}.tar.gz
BuildRequires:  libevent-devel
BuildRequires:  libtool
BuildRequires:  openssl-devel
BuildRequires:  pkgconfig
BuildRequires:  ppp-devel
Requires(pre):  shadow-utils

%description
This is a client for the Secure Socket Tunneling Protocol, SSTP. It can be 
used to establish a SSTP connection to a Windows Server.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
This package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q

%build
%configure --disable-static                                        \
           --disable-silent-rules                                  \
           --with-pppd-plugin-dir="%{_libdir}/pppd/%{ppp_version}" \
           --with-runtime-dir="%{_localstatedir}/run/sstpc"

# Get rid of RPATH
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

# Get rid of redundant linking
sed -i -e 's! -shared ! -Wl,--as-needed\0!g' libtool

%make_build

%install
%make_install

# Use %%doc to handle documentation.
rm -frv %{buildroot}%{_docdir}

find %{buildroot} -name '*.la' -delete -print

%pre
getent group sstpc >/dev/null || groupadd -r sstpc
getent passwd sstpc >/dev/null || \
    useradd -r -g sstpc \
    -d %{_localstatedir}/run/sstpc \
    -s /sbin/nologin \
    -c "Secure Socket Tunneling Protocol (SSTP) Client" sstpc
exit 0

%post -p /sbin/ldconfig

%postun
/sbin/ldconfig -p
rm -rf %{_localstatedir}/run/sstpc

%files
%doc AUTHORS ChangeLog COPYING README TODO USING *.example
%{_sbindir}/sstpc
%{_libdir}/libsstp_api-0.so
%{_libdir}/pppd/%{ppp_version}/sstp-pppd-plugin.so
%{_mandir}/man8/sstpc.8*

%files devel
%{_includedir}/sstp-client/
%{_libdir}/libsstp_api.so
%{_libdir}/pkgconfig/sstp-client-1.0.pc

%changelog
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
