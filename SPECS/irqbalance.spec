Name:           irqbalance
Version:        1.9.0
Release:        3%{?dist}
Epoch:          2
Summary:        IRQ balancing daemon

License:        GPLv2
Url:            https://github.com/Irqbalance/irqbalance
Source0:        https://github.com/Irqbalance/irqbalance/archive/irqbalance-%{version}.tar.gz
Source1:        irqbalance.sysconfig

BuildRequires:  autoconf automake libtool libcap-ng
BuildRequires:  glib2-devel pkgconf libcap-ng-devel
BuildRequires:  systemd ncurses-devel
BuildRequires:  make
Requires: ncurses-libs
%ifnarch %{arm}
BuildRequires:  numactl-devel
Requires: numactl-libs
%endif

%define _hardened_build 1

ExcludeArch: s390 s390x

Patch1: irqbalance-1.8.0-env-file-path.patch
Patch2: 0001-get-irq-module-relationship-from-sys-bus-pci-driver.patch
Patch3: 0002-check-whether-savedptr-is-NULL-before-invoking-strle.patch
Patch4: 0003-add-meson.patch
Patch5: 0004-Prepare-to-handle-thermal-event.patch
Patch6: 0005-Implement-Netlink-helper-functions-to-subscribe-ther.patch
Patch7: 0006-Handle-thermal-events-to-mask-CPUs.patch
Patch8: 0007-add-keep_going-check-to-prevent-irqbalance-from-fail.patch
Patch9: 0008-parse_proc_interrupts-fix-parsing-interrupt-counts.patch
Patch10: 0009-irqbalance-ui-move-ASSIGNED-TO-CPUS-to-the-last-colu.patch
Patch11: 0010-irqbalance-ui-can-t-change-window-when-in-editing-st.patch
Patch12: 0011-fix-memory-leak-in-ui-ui.c.patch
Patch13: 0012-irqbalance-ui-support-scroll-under-tui-mode-of-irqba.patch
Patch14: 0013-irqbalance-ui-print-cpulist-in-SETUP-IRQS.patch
Patch15: 0014-Improve-documentation-and-logging-for-banned-cpus.patch
Patch16: 0001-irqbalance-ui-skip-in-parse_setup-to-avoid-coredump.patch

%description
irqbalance is a daemon that evenly distributes IRQ load across
multiple CPUs for enhanced performance.

%prep
%setup -q
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1
%patch15 -p1
%patch16 -p1

%build
./autogen.sh
%configure
CFLAGS="%{optflags}" make %{?_smp_mflags}

%install
install -D -p -m 0755 %{name} %{buildroot}%{_sbindir}/%{name}
install -D -p -m 0755 %{name}-ui %{buildroot}%{_sbindir}/%{name}-ui
install -D -p -m 0644 ./misc/irqbalance.service %{buildroot}/%{_unitdir}/irqbalance.service
install -D -p -m 0644 %{SOURCE1} %{buildroot}%{_sysconfdir}/sysconfig/%{name}

install -d %{buildroot}%{_mandir}/man1/
install -p -m 0644 ./irqbalance.1 %{buildroot}%{_mandir}/man1/

%check
make check

%files
%doc COPYING AUTHORS
%{_sbindir}/irqbalance
%{_sbindir}/irqbalance-ui
%{_unitdir}/irqbalance.service
%{_mandir}/man1/*
%config(noreplace) %{_sysconfdir}/sysconfig/irqbalance

%post
%systemd_post irqbalance.service

%preun
%systemd_preun irqbalance.service

%postun
%systemd_postun_with_restart irqbalance.service

%triggerun -- irqbalance < 2:0.56-3
if /sbin/chkconfig --level 3 irqbalance ; then
    /bin/systemctl enable irqbalance.service >/dev/null 2>&1 || :
fi
/sbin/chkconfig --del irqbalance >/dev/null 2>&1 || :

%changelog
* Tue Jul 19 2022 Tao Liu <ltao@redhat.com> - 2:1.9.0-3
- Rebase to latest upstream commit (c8d1fff0f1)

* Thu Jul 14 2022 Tao Liu <ltao@redhat.com> - 2:1.9.0-2
- Rebase to latest upstream commit (167580790c)

* Mon Jun 20 2022 Tao Liu <ltao@redhat.com> - 2:1.9.0-1
- Rebase to latest upstream release v1.9.0. Resolves:rhbz2097871

* Fri Apr 8 2022 Tao Liu <ltao@redhat.com> - 2:1.8.0-5
- Document migrateval. Resolves: rhbz2071959
- Confine irqbalance to systems where it is useful. Resolves: rhbz2063930
- Wrong EnvironmentFile in irqbalance.service. Resolves: rhbz2058509

* Mon Sep 27 2021 Kairui Song <kasong@redhat.com> - 2:1.8.0-4
- Drop CapabilityBoundingSet from irqbalance service. Resolves: rhbz1963152

* Mon Aug 09 2021 Mohan Boddu <mboddu@redhat.com> - 2:1.8.0-3
- Rebuilt for IMA sigs, glibc 2.34, aarch64 flags
  Related: rhbz#1991688

* Fri Aug 06 2021 Kairui Song <kasong@redhat.com> - 2:1.8.0-2
- Disable the communication socket when UI is disabled. Resolves: rhbz1951292
- drop NoNewPrivs from irqbalance service. Resolves: rhbz1963152

* Fri Jul 30 2021 Kairui Song <kasong@redhat.com> - 2:1.8.0-1
- Rebase to latest upstream release

* Fri Apr 16 2021 Mohan Boddu <mboddu@redhat.com> - 2:1.7.0-6
- Rebuilt for RHEL 9 BETA on Apr 15th 2021. Related: rhbz#1947937

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2:1.7.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Aug 05 2020 Peter Robinson <pbrobinson@fedoraproject.org> - 2:1.7.0-4
- Epoch never can go backwards

* Tue Aug 04 2020 Neil Horman <nhorman@redhat.com> - 2:1.7.0-1
- Update to latest upstream (bz 1866002)

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2:1.6.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jun 04 2020 Adam Williamson <awilliam@redhat.com> - 2:1.6.0-2
- Restore environment file patch and fix service start (thanks Ondřej Lysoněk)

* Wed Jun 03 2020 Neil Horman <nhorman@redhat.com> - 2:1.6.0-1
- Update to latest upstream (bz1712908)

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2:1.4.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2:1.4.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2:1.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2:1.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon May 14 2018 Neil Horman <nhorman@redhat.com> 2:1.4.0-1
- Update to latest upstream release
- Add CI harness

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2:1.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Nov 14 2017 Neil Horman <nhorman@redhat.com> - 2:1.3.0-1
- Update to latest upstream
* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2:1.2.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2:1.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2:1.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Jan 13 2017 Petr Holasek <holasekp@gmail.com> - 2:1.2.0-1
- Rebased to v1.2.0 (bz1411554)

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2:1.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Dec 15 2015 Marcin Juszkiewicz <mjuszkiewicz@redhat.com> - 2:1.1.0-2
- Fixed AArch64 support.

* Mon Dec 07 2015 Petr Holasek <pholasek@redhat.com> - 2:1.1.0-1
- Rebased to v1.1.0 (bz1288674)

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:1.0.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Mar 18 2015 Petr Holasek <pholasek@redhat.com> - 2:1.0.9-1
- Rebased to v1.0.9

* Mon Jan 05 2015 Petr Holasek <pholasek@redhat.com> - 2:1.0.8-1
- Rebased to v1.0.8 (bz1176898)

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:1.0.7-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:1.0.7-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun May 11 2014 Peter Robinson <pbrobinson@fedoraproject.org> 2:1.0.7-6
- Switch ExclusiveArch to ExcludeArch as all but s390 is supported (also build for aarch64)

* Thu May 08 2014 Petr Holasek <pholasek@redhat.com> - 2:1.0.7-5
- Fixed memory leak (bz1095915)

* Mon Feb 10 2014 Petr Holasek <pholasek@redhat.com> - 2:1.0.7-4
- Missing autogen.sh call fixed

* Mon Feb 10 2014 Petr Holasek <pholasek@redhat.com> - 2:1.0.7-3
- Irqbalance website address was fixed

* Fri Jan 10 2014 Petr Holasek <pholasek@redhat.com> - 2:1.0.7-2
- ppc64le architecture support was enabled

* Fri Oct 11 2013 Petr Holasek <pholasek@redhat.com> - 2:1.0.7-1
- Rebased to version 1.0.7

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:1.0.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jul 22 2013 Peter Robinson <pbrobinson@fedoraproject.org> 2:1.0.6-3
- Fix FTBFS on ARM, minor spec cleanups

* Thu Jul 18 2013 Petr Holasek <pholasek@redhat.com> - 2:1.0.6-2
- Hardened build

* Mon Jun 10 2013 Petr Holasek <pholasek@redhat.com> - 2:1.0.6-1
- Rebased to version 1.0.6

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:1.0.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Jan 21 2013 Petr Holasek <pholasek@redhat.com> - 2:1.0.5-1
- Rebased to version 1.0.5

* Wed Aug 29 2012 Petr Holasek <pholasek@redhat.com> - 2:1.0.4-2
- Env file path edited

* Mon Aug 27 2012 Petr Holasek <pholasek@redhat.com> - 2:1.0.4-1
- Rebased to version 1.0.4

* Wed Aug 22 2012 Petr Holasek <pholasek@redhat.com> - 2:1.0.3-5
- Make irqbalance scan for new irqs when it detects new irqs (bz832815)
- Fixes SIGFPE crash for some banning configuration (bz849792)
- Fixes affinity_hint values processing (bz832815)
- Adds banirq and bansript options (bz837049)
- imake isn't needed for building any more (bz844359)
- Fixes clogging of syslog (bz837646)
- Added IRQBALANCE_ARGS variable for passing arguments via systemd(bz837048)
- Fixes --hint-policy=subset behavior (bz844381)

* Sun Apr 15 2012 Petr Holasek <pholasek@redhat.com> - 2:1.0.3-4
- Updated libnuma dependencies

* Sun Feb  5 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 2:1.0.3-3
- Build on ARM

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:1.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Dec 02 2011 Neil Horman <nhorman@redhat.com> - 2:1.0.3-1
- Updated to latest upstream release

* Fri Nov 04 2011 Neil Horman <nhorman@redhat.com> - 2:1.0.2-1
- Updated to latest upstream release

* Wed Oct 26 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:1.0-4
- Rebuilt for glibc bug#747377

* Fri Oct 21 2011 Neil Horman <nhorman@redhat.com> - 2:1.0-3
- Fix another crash on non-numa systems (bz 748070)

* Mon Oct 17 2011 Neil Horman <nhorman@redhat.com> - 2:1.0-2
- Fix crash for systems with no numa node support

* Wed Oct 12 2011 Neil Horman <nhorman@redhat.com> - 2:1.0-1
- Update irqbalance to latest upstream version

* Fri May  6 2011 Bill Nottingham <notting@redhat.com> - 2:0.56-4
- fix upgrade trigger

* Fri Apr  8 2011 Peter Robinson <pbrobinson@gmail.com> - 2:0.56-3
- Fix build in rawhide
- Add license file to rpm
- Cleanup spec file

* Fri Mar 25 2011 Anton Arapov <anton@redhat.com> - 2:0.56-3
- rework init in order to respect systemd. (bz 659622)

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:0.56-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jun 10 2010 Neil Horman <nhorman@redhat.com> - 2:0.56-1
- Updated to latest upstream version

* Wed Sep 09 2009 Neil Horman <nhorman@redhat.com> - 2:0.55-25
- Fixing BuildRequires

* Fri Sep 04 2009 Neil Horman <nhorman@redhat.com> - 2:0.55-24
- Fixing irqbalance initscript (bz 521246)

* Wed Sep 02 2009 Neil Horman <nhorman@redhat.com> - 2:0.55-23
- Fixing BuildRequires for new config script

* Tue Sep 01 2009 Neil Horman <nhorman@redhat.com> - 2:0.55-22
- Fixing BuildRequires for new config script

* Tue Sep 01 2009 Neil Horman <nhorman@redhat.com> - 2:0.55-21
- Fixing BuildRequires for new config script

* Tue Sep 01 2009 Neil Horman <nhorman@redhat.com> - 2:0.55-20
- Fixing BuildRequires for new config script

* Tue Sep 01 2009 Neil Horman <nhorman@redhat.com> - 2:0.55-19
- Incorporate capng (bz 520699)

* Fri Jul 31 2009 Peter Lemenkov <lemenkov@gmail.com> - 2:0.55-18
- Added back accidentaly forgotten imake

* Fri Jul 31 2009 Peter Lemenkov <lemenkov@gmail.com> - 2:0.55-17
- Cosmetic fixes in spec-file
- Fixed rpmlint error in the init-script

* Tue Jul 28 2009 Peter Lemenkov <lemenkov@gmail.com> - 2:0.55-16
- Many imrovements in spec-file

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:0.55-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Mar 6 2009 Neil Horman <nhorman@redhat.com>
- Update spec file to build for i586 as per new build guidelines (bz 488849)

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:0.55-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Dec 12 2008 Neil Norman <nhorman@redhat.com> - 2:0.55-12
- Remove odd Netorking dependence from irqbalance (bz 476179)

* Fri Aug 01 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2:0.55-11
- fix license tag

* Wed Jun 04 2008 Neil Horman <nhorman@redhat.com> - 2:0.55-10
- Update man page to explain why irqbalance exits on single cache (bz 449949)

* Tue Mar 18 2008 Neil Horman <nhorman@redhat.com> - 2:0.55-9
- Rediff pid-file patch to not remove initial parse_cpu_tree (bz 433270)

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 2:0.55-8
- Autorebuild for GCC 4.3

* Thu Nov 01 2007 Neil Horman <nhorman@redhat.com> - 2:0.55-7
- Update to properly hadndle pid files (bz 355231)

* Thu Oct 04 2007 Neil Horman <nhorman@redhat.com> - 2:0.55-6
- Fix irqbalance init script (bz 317219)

* Fri Sep 28 2007 Neil Horman <nhorman@redhat.com> - 2:0.55-5
- Install pie patch
- Grab Ulis cpuparse cleanup (bz 310821)

* Wed Aug 29 2007 Fedora Release Engineering <rel-eng at fedoraproject dot org> - 2:0.55-4
- Rebuild for selinux ppc32 issue.

* Thu Jul 05 2007 Neil Horman <nhorman@redhat.com> - 0.55.3
- Fixing LSB requirements (bz 246959)

* Tue Dec 12 2006 Neil Horman <nhorman@redhat.com> - 0.55-2
- Fixing typos in spec file (bz 219301)

* Tue Dec 12 2006 Neil Horman <nhorman@redhat.com> - 0.55-1
- Updating to version 0.55

* Mon Dec 11 2006 Neil Horman <nhorman@redhat.com> - 0.54-1
- Update irqbalance to new version released at www.irqbalance.org

* Wed Nov 15 2006 Neil Horman <nhorman@redhat.com> - 1.13-8
- Add ability to set default affinity mask (bz 211148)

* Wed Nov 08 2006 Neil Horman <nhorman@redhat.com> - 1.13-7
- fix up irqbalance to detect multicore (not ht) (bz 211183)

* Thu Nov 02 2006 Neil Horman <nhorman@redhat.com> - 1.13-6
- bumping up MAX_INTERRUPTS to support xen kernels
- rediffing patch1 and patch3 to remove fuzz

* Tue Oct 17 2006 Neil Horman <nhorman@redhat.com> - 1.13-5
- Making oneshot mean oneshot always (bz 211178)

* Wed Sep 13 2006 Peter Jones <pjones@redhat.com> - 1.13-4
- Fix subsystem locking

* Fri Aug 18 2006 Jesse Keating <jkeating@redhat.com> - 1.13-2
- rebuilt with latest binutils to pick up 64K -z commonpagesize on ppc*
  (#203001)
- Remove hack to use cvs checkin ID as release as it doesn't follow
  packaging guidelines

* Tue Aug 01 2006 Neil Horman <nhorman@redhat.com>
- Change license to GPL in version 0.13

* Sat Jul 29 2006 Dave Jones <davej@redhat.com>
- identify a bunch more classes.

* Fri Jul 14 2006 Jesse Keating <jkeating@redhat.com>
- rebuild

* Tue Jul 11 2006 Dave Jones <davej@redhat.com>
- Further lazy rebalancing tweaks.

* Sun Feb 26 2006 Dave Jones <davej@redhat.com>
- Don't rebalance IRQs where no interrupts have occured.

* Sun Feb 12 2006 Dave Jones <davej@redhat.com>
- Build for ppc[64] too.

* Thu Feb 09 2006 Dave Jones <davej@redhat.com>
- rebuild.

* Fri Dec 16 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt for new gcj

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Tue Mar  1 2005 Dave Jones <davej@redhat.com>
- Rebuild with gcc4

* Tue Feb  8 2005 Dave Jones <davej@redhat.com>
- Build as pie, also -D_FORTIFY_SOURCE=2

* Tue Jan 11 2005 Dave Jones <davej@redhat.com>
- Add missing Obsoletes: kernel-utils.

* Mon Jan 10 2005 Dave Jones <davej@redhat.com>
- Start irqbalance in runlevel 2 too. (#102064)

* Sat Dec 18 2004 Dave Jones <davej@redhat.com>
- Initial packaging, based on kernel-utils.

