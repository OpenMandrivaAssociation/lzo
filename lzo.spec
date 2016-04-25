%define api 2
%define major 2
%define libname %mklibname %{name} %{api} %{major}
%define devname %mklibname %{name} -d

Summary:	Data compression library with very fast (de-)compression
Name:		lzo
Version:	2.09
Release:	1
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
%setup -qn lzo-%{version}
%apply_patches
autoreconf -fi

%build
export CFLAGS="%{optflags} -Ofast"
export CXXLAGS="%{optflags} -Ofast"

%configure \
	--enable-shared \
	--disable-static

%make

%check
make check
make test

%install
%makeinstall_std

rm %{buildroot}%{_libdir}/liblzo2.so
mkdir -p %{buildroot}/%{_lib}
mv %{buildroot}%{_libdir}/liblzo2.so.%{major}* %{buildroot}/%{_lib}
ln -sr %{buildroot}/%{_lib}/liblzo2.so.%{major}.* %{buildroot}%{_libdir}/liblzo2.so

install -m755 shared/lzotest/lzotest -D %{buildroot}%{_bindir}/lzotest
rm -rf %{buildroot}{%{uclibc_root},}%{_datadir}/doc/lzo

%files -n %{libname}
/%{_lib}/liblzo%{api}.so.%{major}*

%files -n %{devname}
%doc AUTHORS NEWS README THANKS doc/LZO.TXT doc/LZO.FAQ
%{_bindir}/lzotest
%{_libdir}/*.so
%{_includedir}/*
