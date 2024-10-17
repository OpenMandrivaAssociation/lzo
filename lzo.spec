# liblzo is used by cairo, cairo is used by wine
%ifarch %{x86_64}
%bcond_without compat32
%else
%bcond_with compat32
%endif

%define api 2
%define major 2
%define libname %mklibname %{name} %{api}
%define oldlibname %mklibname %{name} %{api} %{major}
%define devname %mklibname %{name} -d
%define lib32name %mklib32name %{name} %{api}
%define oldlib32name %mklib32name %{name} %{api} %{major}
%define dev32name %mklib32name %{name} -d

%global optflags %{optflags} -O3

Summary:	Data compression library with very fast (de-)compression
Name:		lzo
Version:	2.10
Release:	8
License:	GPLv2
Group:		System/Libraries
Url:		https://www.oberhumer.com/opensource/lzo/
Source0:	http://www.oberhumer.com/opensource/lzo/download/%{name}-%version.tar.gz
Source1:	%{name}.rpmlintrc
Patch0:		lzo-2.07-buildfix.patch
%if %{with compat32}
BuildRequires:	libc6
%endif

%description
LZO is a portable lossless data compression library written in ANSI C. 
It offers pretty fast compression and *very* fast decompression. 
Decompression requires no memory. In addition there are slower
compression levels achieving a quite competitive compression ratio while 
still decompressing at this very high speed.

%package -n %{libname}
Summary:	Data compression library with very fast (de-)compression
Group:		System/Libraries
%rename %{oldlibname}

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

%if %{with compat32}
%package -n %{lib32name}
Summary:	Data compression library with very fast (de-)compression (32-bit)
Group:		System/Libraries
%rename %{oldlib32name}

%description -n %{lib32name}
LZO is a portable lossless data compression library written in ANSI C.
It offers pretty fast compression and *very* fast decompression.
Decompression requires no memory. In addition there are slower
compression levels achieving a quite competitive compression ratio while
still decompressing at this very high speed.

%package -n %{dev32name}
Summary:	Headers files of liblzo2 library (32-bit)
Group:		Development/C
Requires:	%{devname} = %{version}
Requires:	%{lib32name} = %{version}

%description -n %{dev32name}
LZO is a portable lossless data compression library written in ANSI C.
It offers pretty fast compression and *very* fast decompression.
Decompression requires no memory. In addition there are slower
compression levels achieving a quite competitive compression ratio while
still decompressing at this very high speed.
%endif

%prep
%autosetup -n lzo-%{version} -p1
autoreconf -fi
export CONFIGURE_TOP="$(pwd)"

%if %{with compat32}
mkdir build32
cd build32
%configure32 --enable-shared
cd ..
%endif

mkdir build
cd build
%configure --enable-shared

%build
%if %{with compat32}
%make_build -C build32
%endif
%make_build -C build

%if ! %{cross_compiling}
%check
%if %{with compat32}
make -C build32 check test
%endif
make -C build check test
%endif

%install
%if %{with compat32}
%make_install -C build32
%endif
%make_install -C build

install -m755 build/lzotest/lzotest -D %{buildroot}%{_bindir}/lzotest
rm -rf %{buildroot}%{_datadir}/doc/lzo

%files -n %{libname}
%{_libdir}/liblzo%{api}.so.%{major}*

%files -n %{devname}
%doc AUTHORS NEWS README THANKS doc/LZO.TXT doc/LZO.FAQ
%{_bindir}/lzotest
%{_libdir}/*.so
%{_includedir}/*
%{_libdir}/pkgconfig/*.pc

%if %{with compat32}
%files -n %{lib32name}
%{_prefix}/lib/liblzo%{api}.so.%{major}*

%files -n %{dev32name}
%{_prefix}/lib/*.so
%{_prefix}/lib/pkgconfig/*.pc
%endif
