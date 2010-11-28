%define major 2
%define apiver 2
%define libname %mklibname lzo %{apiver} %{major}
%define develname %mklibname lzo -d

%bcond_without	uclibc

Summary:	Data compression library with very fast (de-)compression
Name:		liblzo
Version:	2.03
Release:	%mkrel 4
License:	GPLv2
Group:		System/Libraries
URL:		http://www.oberhumer.com/opensource/lzo/
Source0:	http://www.oberhumer.com/opensource/lzo/download/lzo-%version.tar.gz
Patch0:		lzo-2.03-format_not_a_string_literal_and_no_format_arguments.diff
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot
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
Provides:	%{name}

%description -n %{libname}
LZO is a portable lossless data compression library written in ANSI C.
It offers pretty fast compression and *very* fast decompression.
Decompression requires no memory. In addition there are slower
compression levels achieving a quite competitive compression ratio while
still decompressing at this very high speed.

%package -n	%{develname}
Summary:	Headers files of liblzo library
Group:		Development/C
Requires:	%{libname} = %{version}
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
%patch0 -p0 -b .format_not_a_string_literal_and_no_format_arguments

%build
export CONFIGURE_TOP=`pwd`
%if %{with uclibc}
mkdir -p uclibc
cd uclibc
%configure2_5x	CC="%{uclibc_cc}" \
		CFLAGS="%{uclibc_cflags}" \
		--disable-shared
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
rm -rf %{buildroot}
%if %{with uclibc}
install -m644 uclibc/src/.libs/liblzo2.a -D %{buildroot}%{uclibc_root}%{_libdir}/liblzo.a
%endif
%makeinstall_std -C shared
install -m755 shared/lzotest/lzotest -D %{buildroot}%{_bindir}/lzotest

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%clean
rm -rf %{buildroot}

%files -n %{libname}
%defattr (-,root,root)
%doc AUTHORS NEWS README THANKS doc/LZO.TXT doc/LZO.FAQ
%{_libdir}/*%{apiver}.so.%{major}*

%files -n %{develname}
%defattr (-,root,root)
%doc doc/LZOAPI.TXT doc/LZOTEST.TXT
%{_bindir}/lzotest
%{_libdir}/*.a
%if %{with uclibc}
%{uclibc_root}%{_libdir}/*.a
%endif
%{_libdir}/*.so
%{_libdir}/*.la
%{_includedir}/* 
