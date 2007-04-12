%define name liblzo
%define version 2.01
%define release %mkrel 2

%define major 2_2
%define libname %mklibname lzo %{major}
#fixed2
%{?!mkrel:%define mkrel(c:) %{-c: 0.%{-c*}.}%{!?_with_unstable:%(perl -e '$_="%{1}";m/(.\*\\D\+)?(\\d+)$/;$rel=${2}-1;re;print "$1$rel";').%{?subrel:%subrel}%{!?subrel:1}.%{?distversion:%distversion}%{?!distversion:%(echo $[%{mdkversion}/10])}}%{?_with_unstable:%{1}}%{?distsuffix:%distsuffix}%{?!distsuffix:mdk}}

Name: %name
Summary: Data compression library with very fast (de-)compression
Version: %version
Release: %release
Source: http://www.oberhumer.com/opensource/lzo/download/lzo-%version.tar.bz2
Group: System/Libraries
BuildRoot: %{_tmppath}/%{name}-buildroot
License: GPL
URL: http://www.oberhumer.com/opensource/lzo/

%description
LZO is a portable lossless data compression library written in ANSI C. 
It offers pretty fast compression and *very* fast decompression. 
Decompression requires no memory. In addition there are slower
compression levels achieving a quite competitive compression ratio while 
still decompressing at this very high speed.

%package -n %{libname}
Summary: Data compression library with very fast (de-)compression
Group: System/Libraries
Provides: %name

%description -n %{libname}
LZO is a portable lossless data compression library written in ANSI C.
It offers pretty fast compression and *very* fast decompression.
Decompression requires no memory. In addition there are slower
compression levels achieving a quite competitive compression ratio while
still decompressing at this very high speed.

%package -n %{libname}-devel
Summary: Headers files of liblzo library
Group: Development/C
Requires: %{libname} = %version
Provides: liblzo2-devel = %version-%release
Provides: liblzo-devel = %version-%release

%description -n %{libname}-devel
LZO is a portable lossless data compression library written in ANSI C.
It offers pretty fast compression and *very* fast decompression.
Decompression requires no memory. In addition there are slower
compression levels achieving a quite competitive compression ratio while
still decompressing at this very high speed.                    

%prep
rm -rf $RPM_BUILD_ROOT

%setup -q -n lzo-%version

%build

%configure2_5x --enable-shared

%make

%check
make check
make test


%install
%makeinstall 

%post -n %{libname} -p /sbin/ldconfig

%postun -n %{libname} -p /sbin/ldconfig

%clean
rm -rf $RPM_BUILD_ROOT 

%files -n %{libname}
%defattr (-,root,root)
%doc doc/*
%doc AUTHORS COPYING INSTALL NEWS README THANKS
%_libdir/*.so.*

%files -n %{libname}-devel
%defattr (-,root,root)
%_libdir/*a
%_libdir/*so
%_includedir/* 


