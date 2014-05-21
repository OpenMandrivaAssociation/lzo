%define	api	2
%define	major	2
%define	libname	%mklibname lzo %{api} %{major}
%define	devname	%mklibname lzo -d

%bcond_without	uclibc

Summary:	Data compression library with very fast (de-)compression
Name:		liblzo
Version:	2.06
Release:	9.1
License:	GPLv2
Group:		System/Libraries
Url:		http://www.oberhumer.com/opensource/lzo/
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

%package -n	%{devname}
Summary:	Headers files of liblzo2 library
Group:		Development/C
Requires:	%{libname} = %{version}
%if %{with uclibc}
Requires:	uclibc-%{libname} = %{version}
%endif
Provides:	%{name}-devel = %{version}-%{release}
Provides:	lzo-devel = %{version}-%{release}
Obsoletes:	%mklibname lzo 2_2 -d

%description -n %{devname}
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
%configure2_5x \
	--enable-shared \
	--disable-static
%make
cd ..

%check
cd shared
make check
make test

%install
%if %{with uclibc}
%makeinstall_std -C uclibc

rm %{buildroot}%{uclibc_root}%{_libdir}/liblzo2.so
mkdir -p %{buildroot}%{uclibc_root}/%{_lib}
mv %{buildroot}%{uclibc_root}%{_libdir}/liblzo2.so.%{major}* %{buildroot}%{uclibc_root}/%{_lib}
ln -sr %{buildroot}%{uclibc_root}/%{_lib}/liblzo2.so.%{major}.* %{buildroot}%{uclibc_root}%{_libdir}/liblzo2.so
%endif

%makeinstall_std -C shared

rm %{buildroot}%{_libdir}/liblzo2.so
mkdir -p %{buildroot}/%{_lib}
mv %{buildroot}%{_libdir}/liblzo2.so.%{major}* %{buildroot}/%{_lib}
ln -sr %{buildroot}/%{_lib}/liblzo2.so.%{major}.* %{buildroot}%{_libdir}/liblzo2.so

install -m755 shared/lzotest/lzotest -D %{buildroot}%{_bindir}/lzotest
rm -rf %{buildroot}{%{uclibc_root},}%{_datadir}/doc/lzo

%files -n %{libname}
/%{_lib}/liblzo%{api}.so.%{major}*

%if %{with uclibc}
%files -n uclibc-%{libname}
%{uclibc_root}/%{_lib}/liblzo%{api}.so.%{major}*
%endif

%files -n %{devname}
%doc AUTHORS NEWS README THANKS doc/LZO.TXT doc/LZO.FAQ
%{_bindir}/lzotest
%{_libdir}/*.so
%if %{with uclibc}
%{uclibc_root}%{_libdir}/*.a
%{uclibc_root}%{_libdir}/*.so
%endif
%{_includedir}/* 
