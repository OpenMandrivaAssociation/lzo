%define major 2
%define apiver 2
%define libname %mklibname lzo %{apiver} %{major}
%define develname %mklibname lzo -d

%bcond_without	uclibc

Summary:	Data compression library with very fast (de-)compression
Name:		liblzo
Version:	2.06
Release:	3
License:	GPLv2
Group:		System/Libraries
URL:		http://www.oberhumer.com/opensource/lzo/
Source0:	http://www.oberhumer.com/opensource/lzo/download/lzo-%version.tar.gz
%if %{with uclibc}
BuildRequires:	uClibc-devel
%endif

%description
LZO is a portable lossless data compression library written in ANSI C. 
It offers pretty fast compression and *very* fast decompression. 
Decompression requires no memory. In addition there are slower
compression levels achieving a quite competitive compression ratio while 
still decompressing at this very high speed.

%package -n	%{libname}
Summary:	Data compression library with very fast (de-)compression
Group:		System/Libraries

%description -n %{libname}
LZO is a portable lossless data compression library written in ANSI C.
It offers pretty fast compression and *very* fast decompression.
Decompression requires no memory. In addition there are slower
compression levels achieving a quite competitive compression ratio while
still decompressing at this very high speed.

%package -n	uclibc-%{libname}
Summary:	Data compression library with very fast (de-)compression (uClibc build)
Group:		System/Libraries

%description -n uclibc-%{libname}
LZO is a portable lossless data compression library written in ANSI C.
It offers pretty fast compression and *very* fast decompression.
Decompression requires no memory. In addition there are slower
compression levels achieving a quite competitive compression ratio while
still decompressing at this very high speed.

%package -n	%{develname}
Summary:	Headers files of liblzo library
Group:		Development/C
Requires:	%{libname} = %{version}
%if %{with uclibc}
Requires:	uclibc-%{libname} = %{version}
%endif
Provides:	%{name}2-devel = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Obsoletes:	%mklibname lzo 2_2 -d

%description -n %{develname}
LZO is a portable lossless data compression library written in ANSI C.
It offers pretty fast compression and *very* fast decompression.
Decompression requires no memory. In addition there are slower
compression levels achieving a quite competitive compression ratio while
still decompressing at this very high speed.

%prep
%setup -qn lzo-%{version}
autoreconf -fi

%build
export CONFIGURE_TOP=`pwd`
%if %{with uclibc}
mkdir -p uclibc
cd uclibc
%uclibc_configure \
		--enable-shared
%make
cd ..
%endif

mkdir -p shared
cd shared
%configure2_5x	--enable-shared
%make
cd ..

%check
cd shared
make check
make test

%install
%if %{with uclibc}
%makeinstall_std -C uclibc
%endif
%makeinstall_std -C shared
install -m755 shared/lzotest/lzotest -D %{buildroot}%{_bindir}/lzotest
rm -rf %{buildroot}{%{uclibc_root},}%{_datadir}/doc/lzo

%files -n %{libname}
%{_libdir}/*%{apiver}.so.%{major}*

%if %{with uclibc}
%files -n uclibc-%{libname}
%{uclibc_root}%{_libdir}/*%{apiver}.so.%{major}*
%endif

%files -n %{develname}
%doc AUTHORS NEWS README THANKS doc/LZO.TXT doc/LZO.FAQ
%{_bindir}/lzotest
%{_libdir}/*.a
%{_libdir}/*.so
%if %{with uclibc}
%{uclibc_root}%{_libdir}/*.a
%{uclibc_root}%{_libdir}/*.so
%endif
%{_includedir}/* 
