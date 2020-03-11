%define api 2
%define major 2
%define libname %mklibname %{name} %{api} %{major}
%define devname %mklibname %{name} -d

%global optflags %{optflags} -O3

Summary:	Data compression library with very fast (de-)compression
Name:		lzo
Version:	2.10
Release:	5
License:	GPLv2
Group:		System/Libraries
Url:		http://www.oberhumer.com/opensource/lzo/
Source0:	http://www.oberhumer.com/opensource/lzo/download/%{name}-%version.tar.gz
Source1:	%{name}.rpmlintrc
Patch0:		lzo-2.07-buildfix.patch

%description
LZO is a portable lossless data compression library written in ANSI C. 
It offers pretty fast compression and *very* fast decompression. 
Decompression requires no memory. In addition there are slower
compression levels achieving a quite competitive compression ratio while 
still decompressing at this very high speed.

%package -n %{libname}
Summary:	Data compression library with very fast (de-)compression
Group:		System/Libraries

%description -n %{libname}
LZO is a portable lossless data compression library written in ANSI C.
It offers pretty fast compression and *very* fast decompression.
Decompression requires no memory. In addition there are slower
compression levels achieving a quite competitive compression ratio while
still decompressing at this very high speed.

%package -n %{devname}
Summary:	Headers files of liblzo2 library
Group:		Development/C
Requires:	%{libname} = %{version}
Provides:	lzo-devel = %{version}-%{release}
Obsoletes:	%mklibname lzo 2_2 -d

%description -n %{devname}
LZO is a portable lossless data compression library written in ANSI C.
It offers pretty fast compression and *very* fast decompression.
Decompression requires no memory. In addition there are slower
compression levels achieving a quite competitive compression ratio while
still decompressing at this very high speed.

%prep
%autosetup -n lzo-%{version} -p1
autoreconf -fi

%build
%configure \
	--enable-shared \
	--disable-static

%make_build

%check
make check
make test

%install
%make_install

install -m755 lzotest/lzotest -D %{buildroot}%{_bindir}/lzotest
rm -rf %{buildroot}%{_datadir}/doc/lzo

%files -n %{libname}
%{_libdir}/liblzo%{api}.so.%{major}*

%files -n %{devname}
%doc AUTHORS NEWS README THANKS doc/LZO.TXT doc/LZO.FAQ
%{_bindir}/lzotest
%{_libdir}/*.so
%{_includedir}/*
%{_libdir}/pkgconfig/*.pc
