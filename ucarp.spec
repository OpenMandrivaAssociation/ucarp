Summary:	Common Address Redundancy Protocol (CARP) for Unix
Name:		ucarp
Version:	1.5.2
Release:	15
# See the COPYING file which details everything
License:	MIT and BSD
Group:		System/Servers
URL:		https://www.ucarp.org/
Source0:	http://download.pureftpd.org/pub/ucarp/ucarp-%{version}.tar.bz2
Source1:	ucarp@.service
Source2:	vip-001.conf.example
Source3:	vip-common.conf
Source4:	vip-up
Source5:	vip-down
Source7:	ucarp
Source8:	ucarp.8.sgml.bz2
Patch0:		ucarp-1.5.2-sighup.patch
Requires(post):		systemd-units
Requires(preun):	systemd-units
Requires(postun):	systemd-units
BuildRequires:	gettext
BuildRequires:	autoconf, automake, libtool
BuildRequires:	libpcap-devel
BuildRequires:	systemd
BuildRequires:	docbook-dtd41-sgml
BuildRequires:	docbook-utils

%description
UCARP allows a couple of hosts to share common virtual IP addresses in order
to provide automatic failover. It is a portable userland implementation of the
secure and patent-free Common Address Redundancy Protocol (CARP, OpenBSD's
alternative to the patents-bloated VRRP).
Strong points of the CARP protocol are: very low overhead, cryptographically
signed messages, interoperability between different operating systems and no
need for any dedicated extra network link between redundant hosts.


%prep
%setup -q
%patch0 -p0

bzcat %{SOURCE8} > ucarp.8.sgml


%build
autoreconf -fi
%configure2_5x
%make

docbook2man --backend man ucarp.8.sgml > ucarp.8
mv UCARP.8 ucarp.8

%install
%makeinstall_std
%find_lang %{name}

# Install the unit file
install -D -p -m 0755 %{SOURCE1} \
    %{buildroot}%{_unitdir}/ucarp@.service

mkdir -p %{buildroot}/etc/ucarp
mkdir -p %{buildroot}%{_libexecdir}/ucarp

# Install the example config files
install -D -p -m 0600 %{SOURCE2} %{SOURCE3} \
    %{buildroot}/etc/ucarp/

# Install helper scripts
install -D -p -m 0700 %{SOURCE4} %{SOURCE5} %{SOURCE7} \
    %{buildroot}%{_libexecdir}/ucarp/

mkdir -p %{buildroot}%{_mandir}/man8/
install -m0644 ucarp.8 %{buildroot}%{_mandir}/man8/

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service


%files -f %{name}.lang
%doc AUTHORS COPYING ChangeLog NEWS README
%{_unitdir}/ucarp@.service
%attr(0700,root,root) %dir /etc/ucarp/
%config(noreplace) /etc/ucarp/vip-common.conf
/etc/ucarp/vip-001.conf.example
%config(noreplace) %{_libexecdir}/ucarp/
%{_sbindir}/ucarp
%{_mandir}/man8/ucarp.8*
