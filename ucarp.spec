Summary:	UCARP is a portable implementation of the CARP protocol
Name:		ucarp
Version:	1.4
Release:	%mkrel 1
License:	BSD
Group:		Networking/Other
URL:		http://download.pureftpd.org/pub/ucarp/
Source0:	http://download.pureftpd.org/pub/ucarp/%{name}-%{version}.tar.bz2
Source1:	ucarp.8.sgml.bz2
Source2:	ucarp.init
Patch0:		ucarp-no_bundled_libtool.diff
BuildRequires:	docbook-dtd41-sgml
BuildRequires:	docbook-utils
BuildRequires:	gettext
BuildRequires:	libpcap-devel
BuildRequires:	libtool
Requires(post):  rpm-helper
Requires(preun): rpm-helper
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
UCARP allows a couple of hosts to share common virtual IP addresses
in order to provide automatic failover. It is a portable userland
implementation of the secure and patent-free Common Address Redundancy
Protocol (CARP, OpenBSD\u2019s alternative to the patents-bloated VRRP).

Strong points of the CARP protocol are: very low overhead, cryptographically
signed messages, interoperability between different operating systems and
no need for any dedicated extra network link between redundant hosts.

%prep

%setup -q
%patch0 -p0 -b .no_bundled_libtool

bzcat %{SOURCE1} > ucarp.8.sgml

%build
rm -f configure
libtoolize --copy --force; aclocal -I m4; autoconf

%configure2_5x

%make

docbook2man --backend man ucarp.8.sgml > ucarp.8
mv UCARP.8 ucarp.8

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_mandir}/man8

%makeinstall_std PREFIX=/usr

install -m755 -D %{SOURCE2} %{buildroot}%{_initrddir}/%{name}
install -d %{buildroot}%{_sysconfdir}/%{name}.d/
install -m0644 ucarp.8 %{buildroot}%{_mandir}/man8/

%find_lang ucarp

%clean
rm -rf %{buildroot}

%post
%_post_service %{name}

%preun
%_preun_service %{name}

%files -f ucarp.lang
%defattr(-,root,root)
%doc README INSTALL COPYING AUTHORS NEWS examples/linux/*.sh
%defattr(-,root,root,0755)
%{_sbindir}/*
%{_initrddir}/%{name}
%{_sysconfdir}/%{name}.d/
%{_mandir}/man8/ucarp.8*
