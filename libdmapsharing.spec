#
# Conditional build:
%bcond_without	apidocs		# do not build and package API docs

Summary:	A DMAP client and server library
Name:		libdmapsharing
Version:	2.9.15
Release:	1
License:	LGPL v2+
Group:		Development/Libraries
Source0:	http://www.flyn.org/projects/libdmapsharing/%{name}-%{version}.tar.gz
# Source0-md5:	52c9e4d3de931d9013eeaccf7371bb2d
URL:		http://www.flyn.org/projects/libdmapsharing/index.html
BuildRequires:	avahi-glib-devel >= 0.5
BuildRequires:	gdk-pixbuf2-devel
BuildRequires:	glib2-devel
BuildRequires:	gstreamer-plugins-base-devel >= 0.10.23.2
BuildRequires:	libsoup-devel >= 2.32.2
BuildRequires:	pkgconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
libdmapsharing is a library you may use to access and share DMAP (DAAP
& DPAP) content. The library is written in C using GObject and
libsoup.

The DMAP family of protocols are used by products such as iTunes(tm),
iPhoto(tm) and the Roku SoundBridge(tm) family to share content such
as music and photos.

%package devel
Summary:	Files needed to develop applications using libdmapsharing
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	avahi-glib-devel
Requires:	gdk-pixbuf2-devel
Requires:	glib2-devel
Requires:	gstreamer-plugins-base-devel >= 0.10.23.2
Requires:	libsoup-devel >= 2.32.2

%description devel
libdmapsharing implements the DMAP protocols. This includes support
for DAAP and DPAP. This package provides the libraries, include files,
and other resources needed for developing applications using
libdmapsharing.

%package apidocs
Summary:	libdmapsharing API documentation
Summary(pl.UTF-8):	Dokumentacja API biblioteki libdmapsharing
Group:		Documentation

%description apidocs
API documentation for libdmapsharing library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki libdmapsharing.

%prep
%setup -q

%build
%configure \
	--disable-static \
	--with-mdns=avahi \
	--with-html-dir=%{_gtkdocdir}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	INSTALL="install -p" \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/libdmapsharing-3.0.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%attr(755,root,root) %{_libdir}/libdmapsharing-3.0.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libdmapsharing-3.0.so.2

%files devel
%defattr(644,root,root,755)
%{_pkgconfigdir}/libdmapsharing-3.0.pc
%{_includedir}/libdmapsharing-3.0
%{_libdir}/libdmapsharing-3.0.so

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/libdmapsharing-3.0
%endif
