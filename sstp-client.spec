%global _hardened_build 1
%global __provides_exclude ^sstp-pppd-plugin\\.so$
%global clientname sstpc

Name:           sstp-client
Version:        1.0.9
Release:        4%{?dist}
Summary:        Secure Socket Tunneling Protocol (SSTP) Client
License:        GPLv2+
Url:            http://sstp-client.sourceforge.net
Source0:        http://downloads.sourceforge.net/project/%{name}/%{name}/%{version}/%{name}-%{version}.tar.gz
BuildRequires:  libevent-devel
BuildRequires:  libtool
BuildRequires:  openssl-devel
BuildRequires:  pkgconfig
BuildRequires:  ppp-devel
Requires:       openssl
Requires:       ppp
Requires(pre):  shadow-utils

%description
This is a client for the Secure Socket Tunneling Protocol, SSTP. It can be 
used to establish a SSTP connection to a Windows Server.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q

%build
%configure --disable-static \
           --with-runtime-dir="%{_localstatedir}/run/%{clientname}"
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
sed -i -e 's! -shared ! -Wl,--as-needed\0!g' libtool
make CFLAGS="%{optflags}" %{?_smp_mflags} V=1

%install
make install DESTDIR=%{buildroot}
rm -rf %{buildroot}%{_datadir}/doc
find %{buildroot} -name '*.la' -exec rm -f {} ';'

%pre
getent group %{clientname} >/dev/null || groupadd -r %{clientname}
getent passwd %{clientname} >/dev/null || \
    useradd -r -g %{clientname} \
    -d %{_localstatedir}/run/%{clientname} \
    -s /sbin/nologin \
    -c "Secure Socket Tunneling Protocol (SSTP) Client" %{clientname}
exit 0

%post -p /sbin/ldconfig

%postun
/sbin/ldconfig -p
rm -rf %{_localstatedir}/run/%{clientname}

%files
%doc AUTHORS ChangeLog COPYING README TODO USING *.example
%{_sbindir}/%{clientname}
%{_libdir}/libsstp_api-0.so
%{_libdir}/pppd/2.4.5/sstp-pppd-plugin.so
%{_mandir}/man8/%{clientname}.8*

%files devel
%{_includedir}/sstp-client/
%{_libdir}/libsstp_api.so
%{_libdir}/pkgconfig/sstp-client-1.0.pc

%changelog
* Thu Aug 01 2013 Christopher Meng <rpm@cicku.me> - 1.0.9-4
- Fix library issue.

* Fri Jul 26 2013 Christopher Meng <rpm@cicku.me> - 1.0.9-3
- Filter out the private library.

* Tue Jul 23 2013 Christopher Meng <rpm@cicku.me> - 1.0.9-2
- Remove Rpath.

* Sun Feb 03 2013 Christopher Meng <rpm@cicku.me> - 1.0.9-1
- Initial Package.
