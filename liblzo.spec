%define major 2
%define apiver 2
%define libname %mklibname lzo %{apiver} %{major}
%define develname %mklibname lzo -d

Summary:	Data compression library with very fast (de-)compression
Name:		liblzo
Version:	2.02
Release:	%mkrel 3
License:	GPL
URL:		http://www.oberhumer.com/opensource/lzo/
Source:		http://www.oberhumer.com/opensource/lzo/download/lzo-%version.tar.bz2
Group:		System/Libraries
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot

%description
LZO is a portable lossless data compression library written in ANSI C. 
It offers pretty fast compression and *very* fast decompression. 
Decompression requires no memory. In addition there are slower
compression levels achieving a quite competitive compression ratio while 
still decompressing at this very high speed.

%package -n %{libname}
Summary:	Data compression library with very fast (de-)compression
Group:		System/Libraries
Provides:	%{name}

%description -n %{libname}
LZO is a portable lossless data compression library written in ANSI C.
It offers pretty fast compression and *very* fast decompression.
Decompression requires no memory. In addition there are slower
compression levels achieving a quite competitive compression ratio while
still decompressing at this very high speed.

%package -n %{develname}
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

%build

%configure2_5x \
	--enable-shared

%make

%check
make check
make test

%install
rm -rf %{buildroot}
%makeinstall_std

%post -n %{libname} -p /sbin/ldconfig

%postun -n %{libname} -p /sbin/ldconfig

%clean
rm -rf %{buildroot}

%files -n %{libname}
%defattr (-,root,root)
%doc doc/*
%doc AUTHORS COPYING INSTALL NEWS README THANKS
%{_libdir}/*%{apiver}.so.%{major}*

%files -n %{develname}
%defattr (-,root,root)
%{_libdir}/*.a
%{_libdir}/*.so
%{_libdir}/*.la
%{_includedir}/* 
