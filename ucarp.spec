Summary:	Portable implementation of the CARP protocol
Name:		ucarp
Version:	1.5.2
Release:	8
License:	BSD
Group:		Networking/Other
URL:		http://download.pureftpd.org/pub/ucarp/
Source0:	http://download.pureftpd.org/pub/ucarp/%{name}-%{version}.tar.gz
Source1:	ucarp.8.sgml.bz2
Source2:	ucarp.init
BuildRequires:	docbook-dtd41-sgml
BuildRequires:	docbook-utils
BuildRequires:	gettext
BuildRequires:	libpcap-devel
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

bzcat %{SOURCE1} > ucarp.8.sgml

%build
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


%changelog
* Fri May 06 2011 Oden Eriksson <oeriksson@mandriva.com> 1.5.2-2mdv2011.0
+ Revision: 670737
- mass rebuild

* Thu Feb 24 2011 Oden Eriksson <oeriksson@mandriva.com> 1.5.2-1
+ Revision: 639583
- 1.5.2

* Sat Dec 04 2010 Oden Eriksson <oeriksson@mandriva.com> 1.5.1-3mdv2011.0
+ Revision: 608092
- rebuild

* Sun Mar 14 2010 Oden Eriksson <oeriksson@mandriva.com> 1.5.1-2mdv2010.1
+ Revision: 519076
- rebuild

* Thu May 28 2009 Oden Eriksson <oeriksson@mandriva.com> 1.5.1-1mdv2010.0
+ Revision: 380369
- 1.5.1
- nuke redundant patch

* Mon Dec 22 2008 Oden Eriksson <oeriksson@mandriva.com> 1.5-3mdv2009.1
+ Revision: 317665
- rebuild

* Wed Oct 29 2008 Oden Eriksson <oeriksson@mandriva.com> 1.5-2mdv2009.1
+ Revision: 298445
- rebuilt against libpcap-1.0.0

* Tue Aug 05 2008 Oden Eriksson <oeriksson@mandriva.com> 1.5-1mdv2009.0
+ Revision: 263817
- 1.5
- rediffed P0

* Wed Jun 18 2008 Thierry Vignaud <tv@mandriva.org> 1.4-3mdv2009.0
+ Revision: 225894
- rebuild

* Mon Feb 18 2008 Thierry Vignaud <tv@mandriva.org> 1.4-2mdv2008.1
+ Revision: 171151
- rebuild
- fix "foobar is blabla" summary (=> "blabla") so that it looks nice in rpmdrake

* Tue Jan 22 2008 Oden Eriksson <oeriksson@mandriva.com> 1.4-1mdv2008.1
+ Revision: 156052
- 1.4
- drop the ucarp-1.2-ip_addr_len.patch patch, another fix seems to
  be implemented upstream
- use system libtool (P0)
- added missing entries in ucarp.init (S2)

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Wed Sep 19 2007 Guillaume Rousse <guillomovitch@mandriva.org> 1.2-9mdv2008.0
+ Revision: 90340
- rebuild

* Mon Jul 02 2007 Michael Scherer <misc@mandriva.org> 1.2-8mdv2008.0
+ Revision: 47096
- Import ucarp



* Sun Aug 27 2006 Olivier Blin <blino@mandriva.com> 1.2-8mdv2007.0
- make initscript start/stop correctly when no device is configured

* Wed Aug 23 2006 Olivier Blin <blino@mandriva.com> 1.2-7mdv2007.0
- Patch0: fix buffer overflow (#23817, patch from Michael Scherer)

* Wed Aug 23 2006 Olivier Blin <blino@mandriva.com> 1.2-6mdv2007.0
- add support for up/down scripts in initscript
- don't use ignored files in /etc/ucarp.d/

* Tue Aug 22 2006 Olivier Blin <blino@mandriva.com> 1.2-5mdv2007.0
- add service and /etc/ucarp.d configuration directory

* Fri Jul 07 2006 Oden Eriksson <oeriksson@mandriva.com> 1.2-4mdv2007.0
- fix deps

* Wed Jul 05 2006 Oden Eriksson <oeriksson@mandriva.com> 1.2-3mdv2007.0
- add a man page (debian)

* Wed Jul 05 2006 Oden Eriksson <oeriksson@mandriva.com> 1.2-2mdv2007.0
- fix deps

* Thu Jun 29 2006 Samir Bellabes <sbellabes@mandriva.com> 1.2-1mdv2007.0
- First release
