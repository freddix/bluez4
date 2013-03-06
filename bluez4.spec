Summary:	Bluetooth protocol stack for Linux
Name:		bluez4
Version:	4.101
Release:	1
License:	GPL v2+
Group:		Applications/System
Source0:	http://www.kernel.org/pub/linux/bluetooth/bluez-%{version}.tar.gz
# Source0-md5:	fb42cb7038c380eb0e2fa208987c96ad
URL:		http://www.bluez.org/
BuildRequires:	alsa-lib-devel
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	bison
BuildRequires:	dbus-glib-devel
%if %{with gstreamer}
BuildRequires:	gstreamer010-plugins-base-devel
%endif
BuildRequires:	libnl-devel
BuildRequires:	libsndfile-devel
BuildRequires:	libtool
BuildRequires:	libusbx-devel
BuildRequires:	pkg-config
Requires(post,preun,postun):	systemd-units
Requires:	%{name}-libs = %{epoch}:%{version}-%{release}
Requires:	udev
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# hardcoded /usr/lib
%define		cupsdir		/usr/lib/cups/backend

%description
Bluetooth protocol stack for Linux.

%package -n cups-backend-bluez
Summary:	Bluetooth backend for CUPS
Group:		Applications/Printing
Requires:	bluez-libs >= %{epoch}:%{version}-%{release}
Requires:	cups

%description -n cups-backend-bluez
Bluetooth backend for CUPS.

%package libs
Summary:	Bluetooth libraries
Group:		Development/Libraries

%description libs
Libraries for use in Bluetooth applications.

%package devel
Summary:	Header files for Bluetooth applications
Group:		Development/Libraries
Requires:	%{name}-libs = %{epoch}:%{version}-%{release}

%description devel
bluez-libs-devel contains header files for use in Bluetooth
applications.

%prep
%setup -qn bluez-%{version}

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-silent-rules	\
	--disable-test		\
	--enable-audio		\
	--enable-bccmd		\
	--enable-configfiles	\
	--enable-cups		\
	--enable-dfutool	\
	--enable-dund		\
	--enable-hidd		\
	--enable-input		\
	--enable-network	\
	--enable-pand		\
	--enable-serial		\
	--enable-shared		\
	--enable-tools		\
	--enable-usb		\
	--with-systemdunitdir=%{systemdunitdir}
%{__make} \
	cupsdir=%{cupsdir}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_libdir}/bluetooth/plugins,%{_sysconfdir}/bluetooth}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	cupsdir=%{cupsdir}

install audio/audio.conf $RPM_BUILD_ROOT/etc/bluetooth
install input/input.conf $RPM_BUILD_ROOT/etc/bluetooth
install network/network.conf $RPM_BUILD_ROOT/etc/bluetooth

%clean
rm -rf $RPM_BUILD_ROOT

%post
%systemd_post bluetooth.service

%preun
%systemd_preun bluetooth.service

%postun
%systemd_postun

%post	libs -p /usr/sbin/ldconfig
%postun	libs -p /usr/sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_sbindir}/*

%dir %{_libdir}/bluetooth
%dir %{_libdir}/bluetooth/plugins
%dir %{_sysconfdir}/bluetooth

%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/bluetooth/audio.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/bluetooth/input.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/bluetooth/main.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/bluetooth/network.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/bluetooth/rfcomm.conf
%config(noreplace) %verify(not md5 mtime size) /etc/dbus-1/system.d/bluetooth.conf

%{systemdunitdir}/bluetooth.service
%{_datadir}/dbus-1/system-services/org.bluez.service

%{_mandir}/man[18]/*

%files -n cups-backend-bluez
%defattr(644,root,root,755)
%attr(755,root,root) %{_prefix}/lib/cups/backend/bluetooth

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %ghost %{_libdir}/libbluetooth.so.?
%attr(755,root,root) %{_libdir}/libbluetooth.so.*.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libbluetooth.so
%{_libdir}/libbluetooth.la
%{_includedir}/bluetooth
%{_pkgconfigdir}/bluez.pc

