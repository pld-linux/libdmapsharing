#
# Conditional build:
%bcond_without	apidocs		# do not build and package API docs
%bcond_with	check		# check/testing support (note: library links with libcheck!)
%bcond_without	static_libs	# static library build

Summary:	A DMAP client and server library
Summary(pl.UTF-8):	Biblioteka klienta i serwera DMAP
Name:		libdmapsharing
Version:	3.9.13
Release:	1
License:	LGPL v2.1+
Group:		Libraries
Source0:	https://www.flyn.org/projects/libdmapsharing/%{name}-%{version}.tar.gz
# Source0-md5:	b6687c3bede93421ca9bfdd9f596f122
Patch0:		floorf.patch
URL:		https://www.flyn.org/projects/libdmapsharing/
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
BuildRequires:	avahi-glib-devel >= 0.6
%{?with_check:BuildRequires:	check-devel >= 0.12}
BuildRequires:	gdk-pixbuf2-devel >= 2.0
BuildRequires:	glib2-devel >= 1:2.66
BuildRequires:	gobject-introspection-devel >= 1.30.0
BuildRequires:	gstreamer-plugins-base-devel >= 1.0
BuildRequires:	gtk-doc >= 1.0
# noinst programs only
#BuildRequires:	gtk+3-devel >= 3.0
#BuildRequires:	libgee-devel >= 0.8
BuildRequires:	libsoup3-devel >= 3.0
BuildRequires:	libtool >= 2:2
BuildRequires:	pkgconfig
# not needed for releases, noinst only
#BuildRequires:	vala >= 1:0.11.4
BuildRequires:	zlib-devel
Requires:	avahi-glib >= 0.6
Requires:	glib2 >= 1:2.66
Requires:	libsoup3 >= 3.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
libdmapsharing is a library you may use to access and share DMAP (DAAP
& DPAP) content. The library is written in C using GObject and
libsoup.

The DMAP family of protocols are used by products such as iTunes(TM),
iPhoto(TM) and the Roku SoundBridge(TM) family to share content such
as music and photos.

%description -l pl.UTF-8
libdmapsharing to biblioteka służąca do dostępu i współdzielenia
treści DMAP (DAAP i DPAP). Biblioteka jest napisana w C z użyciem
bibliotek GObject i libsoup.

Rodzina protokołów DMAP jest wykorzystywana przez produkty takie jak
iTunes(TM), iPhoto(TM) oraz Roku SoundBridge do współdzielenia treści
takich jak muzyka czy zdjęcia.

%package devel
Summary:	Files needed to develop applications using libdmapsharing
Summary(pl.UTF-8):	Pliki niezbędne do tworzenia aplikacji wykorzystujących libdmapsharing
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	avahi-glib-devel >= 0.6
Requires:	gdk-pixbuf2-devel >= 2.0
Requires:	glib2-devel >= 1:2.66
Requires:	gstreamer-plugins-base-devel >= 1.0
Requires:	libsoup3-devel >= 3.0

%description devel
libdmapsharing implements the DMAP protocols. This includes support
for DAAP and DPAP. This package provides the include files and other
resources needed for developing applications using libdmapsharing.

%description devel -l pl.UTF-8
libdmapsharing implementuje protokoły DMAP. Obejmuje obsługę DAAP i
DPAP. Ten pakiet zawiera pliki nagłówkowe i inne niezbędne do
tworzenia aplikacji wykorzystujących libdmapsharing.

%package static
Summary:	Static libdmapsharing library
Summary(pl.UTF-8):	Statyczna biblioteka libdmapsharing
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static libdmapsharing library.

%description static -l pl.UTF-8
Statyczna biblioteka libdmapsharing.

%package apidocs
Summary:	libdmapsharing API documentation
Summary(pl.UTF-8):	Dokumentacja API biblioteki libdmapsharing
Group:		Documentation
BuildArch:	noarch

%description apidocs
API documentation for libdmapsharing library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki libdmapsharing.

%package -n vala-libdmapsharing
Summary:	Vala API for libdmapsharing library
Summary(pl.UTF-8):	API języka Vala do biblioteki libdmapsharing
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Requires:	vala >= 1:0.11.4
BuildArch:	noarch

%description -n vala-libdmapsharing
Vala API for libdmapsharing library.

%description -n vala-libdmapsharing -l pl.UTF-8
API języka Vala do biblioteki libdmapsharing.

%prep
%setup -q
%patch0 -p1

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{!?with_check:--disable-check} \
	--disable-silent-rules \
	%{?with_static_libs:--enable-static} \
	%{!?with_check:--disable-tests} \
	--with-html-dir=%{_gtkdocdir} \
	--with-mdns=avahi

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	INSTALL="install -p" \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/libdmapsharing-4.0.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README README-Memory TODO
%attr(755,root,root) %{_libdir}/libdmapsharing-4.0.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libdmapsharing-4.0.so.3
%{_libdir}/girepository-1.0/Dmap-4.0.typelib

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libdmapsharing-4.0.so
%{_includedir}/libdmapsharing-4.0
%{_datadir}/gir-1.0/Dmap-4.0.gir
%{_pkgconfigdir}/libdmapsharing-4.0.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libdmapsharing-4.0.a
%endif

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/libdmapsharing-4.0
%endif

%files -n vala-libdmapsharing
%defattr(644,root,root,755)
%{_datadir}/vala/vapi/libdmapsharing-4.0.vapi
