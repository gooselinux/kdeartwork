Name: kdeartwork
Version: 4.3.4
Release: 6%{?dist}
Summary: Additional artwork for KDE
License: GPLv2 and MIT
Group: User Interface/Desktops
URL: http://www.kde.org/
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
# Source: ftp://ftp.kde.org/pub/kde/stable/%{version}/src/%{name}-%{version}.tar.bz2
# To create the pached archive do the following:
# tar jxf %{name}-%{version}.tar.bz2
# rm -rf %{name}-%{version}/WeatherWallpapers/Hail
# remove the line with Hail in CMakeLists.txt
# rm -rf %{name}-%{version}/kscreensaver/xsavers
# rm -rf %{name}-%{version}/kscreensaver/{ccmathteam.com,greggman.com,phpBB,plain,BoxedEmoticonSet}
# rm -rf %{name}-%{version}/kscreensaver/kdesavers/{polygon*,banner*,slideshow*,lines*,lorenz*,blob*,science*,fountain*,wave*,gravity*}
# tar jcf %{name}-%{version}-patched.tar.bz2 %{name}-%{version}-patched
Source: kdeartwork-4.3.4-patched.tar.bz2     

# add missing xscreensaver 
Patch0: kdeartwork-4.3.0-template.patch

BuildRequires: kdelibs4-devel >= %{version}
BuildRequires: kdebase-workspace-devel >= %{version}

Requires: kdebase-workspace >= %{version}

Obsoletes: kdeclassic-icon-theme < %{version}%{release}
Obsoletes: kdeartwork-icons < 4.2.2-3
Obsoletes: kdeartwork < 4.3.0-2

%description
%{summary}, including additional styles, themes.

%package -n nuvola-icon-theme
Summary: Nuvola icon theme
Group: User Interface/Desktops
BuildArch: noarch

%description -n nuvola-icon-theme
%{summary}.

%package -n kdeclassic-icon-theme
Summary: KDE classic icon theme
Group: User Interface/Desktops
Obsoletes: kdeartwork-icons < 4.2.2-3
Provides: kdeartwork-icons = %{version}-%{release}
BuildArch: noarch

%description -n kdeclassic-icon-theme
%{summary}.

%package -n kde-style-phase
Summary: Classic GUI style for KDE
Group: User Interface/Desktops

%description -n kde-style-phase
%{summary}.

%package screensavers
Summary: screensavers for KDE
Group: Amusements/Graphics
Obsoletes: kdeartwork-extras < 4.2.2-3
Provides: kdeartwork-extras = %{version}-%{release}

%description screensavers
%{summary}.

%package kxs
Summary: Support for xscreensaver-based screensavers
Group: Amusements/Graphics
Requires: kdebase-workspace >= %{version}
Requires: xscreensaver-base

%description kxs
%{summary}.

%package wallpapers
Summary: Additional wallpapers
Group: Amusements/Graphics
Requires: kde-filesystem
BuildArch: noarch

%description wallpapers
%{summary}.

%package sounds
Summary: Additional sounds
Group: Amusements/Graphics
Requires: kde-filesystem
BuildArch: noarch

%description sounds
%{summary}.


%prep
%setup -q -n %{name}-%{version}-patched

%patch0 -p1 -b .template

%build

mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kde4} ..
popd

make %{?_smp_mflags} -C %{_target_platform}


%install
rm -rf %{buildroot}

make install/fast DESTDIR=%{buildroot} -C %{_target_platform}

%if ! 0%{?include_crystalsvg}
rm -rf %{buildroot}%{_kde4_iconsdir}/crystalsvg/
%endif

%clean
rm -rf %{buildroot}


%if 0%{?kdeclassic_icons}
%post -n kdeclassic-icon-theme
touch --no-create %{_kde4_iconsdir}/kdeclassic &> /dev/null || :

%posttrans -n kdeclassic-icon-theme
gtk-update-icon-cache %{_kde4_iconsdir}/kdeclassic &> /dev/null || :

%postun -n kdeclassic-icon-theme
if [ $1 -eq 0 ] ; then
touch --no-create %{_kde4_iconsdir}/kdeclassic &> /dev/null || :
gtk-update-icon-cache %{_kde4_iconsdir}/kdeclassic &> /dev/null || :
fi
%endif

%post -n nuvola-icon-theme
touch --no-create %{_kde4_iconsdir}/nuvola &> /dev/null || :

%posttrans -n nuvola-icon-theme
gtk-update-icon-cache %{_kde4_iconsdir}/nuvola-icon-theme &> /dev/null || :

%postun -n nuvola-icon-theme
if [ $1 -eq 0 ] ; then
touch --no-create %{_kde4_iconsdir}/nuvola &> /dev/null || :
gtk-update-icon-cache %{_kde4_iconsdir}/nuvola &> /dev/null || :
fi


%files
%defattr(-,root,root,-)
%doc COPYING README
%{_kde4_appsdir}/color-schemes/*.colors
%{_kde4_appsdir}/desktoptheme/Aya
%{_kde4_appsdir}/desktoptheme/Clean-Blend/
%{_kde4_appsdir}/desktoptheme/Elegance/
%{_kde4_appsdir}/desktoptheme/heron/
%{_kde4_appsdir}/desktoptheme/Silicon/
%{_kde4_appsdir}/desktoptheme/slim-glow/
%{_kde4_datadir}/emoticons/*

# split for multilib'ing
%files -n kde-style-phase
%defattr(-,root,root,-)
%doc COPYING README
%{_kde4_appsdir}/kstyle/themes/phase.themerc
%{_kde4_libdir}/kde4/kstyle_phase_config.so
%{_kde4_libdir}/kde4/plugins/styles/phasestyle.so

%if 0%{?kdeclassic_icons}
%files -n kdeclassic-icon-theme
%defattr(-,root,root,-)
%doc COPYING README
%{_kde4_iconsdir}/kdeclassic/
%endif

%files -n nuvola-icon-theme
%defattr(-,root,root,-)
%doc COPYING README
%{_kde4_iconsdir}/nuvola/

%files screensavers
%defattr(-,root,root,-)
%doc COPYING README
%{_kde4_appsdir}/kfiresaver/
%{_kde4_appsdir}/kscreensaver/
%{_kde4_bindir}/*.kss
%{_kde4_datadir}/kde4/services/ScreenSavers/*

%files sounds
%defattr(-,root,root,-)
%doc COPYING README
%{_kde4_datadir}/sounds/*

%files wallpapers
%defattr(-,root,root,-)
%doc COPYING README
%{_kde4_datadir}/wallpapers/*


%changelog
* Thu Jul 08 2010 Than Ngo <than@redhat.com> - 4.3.4-6
- Resolves: bz#606886, legal issue

* Tue Jun 29 2010 Than Ngo <than@redhat.com> - 4.3.4-5
- Resolves: bz#606864, legal issue

* Tue Mar 30 2010 Than Ngo <than@redhat.com> - 4.3.4-4
- rebuilt against qt 4.6.2

* Wed Feb 17 2010 Than Ngo <than@redhat.com> - 4.3.4-3
- removed wallpapaer Hail from tarball because of licensing issues

* Sat Dec 12 2009 Than Ngo <than@redhat.com> - 4.3.4-2
- cleanup

* Tue Dec 01 2009 Than Ngo <than@redhat.com> - 4.3.4-1
- 4.3.4

* Fri Nov 13 2009 Than Ngo <than@redhat.com> - 4.3.3-2
- rhel cleanup, fix conditional for RHEL

* Sat Oct 31 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.3.3-1
- 4.3.3

* Mon Oct 26 2009 Than Ngo <than@redhat.com> - 4.3.2-3
- rhel cleanup

* Tue Oct 20 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.3.2-2
- rebuild (eigen2)

* Sun Oct 04 2009 Than Ngo <than@redhat.com> - 4.3.2-1
- 4.3.2

* Mon Sep 28 2009 Than Ngo <than@redhat.com> - 4.3.1-2
- rhel cleanup

* Fri Aug 28 2009 Than Ngo <than@redhat.com> - 4.3.1-1
- 4.3.1
- add missing screensavers bz#472886

* Thu Aug 20 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.3.0-2
- kde-style-phase subpkg (multilib'd)
- %%files: cleanup some dir ownership

* Thu Jul 30 2009 Than Ngo <than@redhat.com> - 4.3.0-1
- 4.3.0

* Tue Jul 21 2009 Than Ngo <than@redhat.com> - 4.2.98-1
- 4.3rc3

* Thu Jul 09 2009 Than Ngo <than@redhat.com> - 4.2.96-1
- 4.3.rc2

* Thu Jun 25 2009 Than Ngo <than@redhat.com> - 4.2.95-1
- 4.3rc1

* Thu Jun 04 2009 Lorenzo Villani <lvillani@binaryhelix.net> - 4.2.90-1
- KDE 4.3 Beta 2

* Wed May 13 2009 Lukáš Tinkl <ltinkl@redhat.com> - 4.2.85-1
- KDE 4.3 beta 1

* Wed Apr 01 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.2.2-3
- optimize scriptlets
- omit (unused) noarch hacks, use f10+ support
- -extras -> -screensavers rename
- -icons -> kdeclassic-icon-theme rename
- main pkg, Requires: -wallpapers, -sounds (upgrade path)
- -wallpapers, -sounds: drop Req: kdebase-workspace
- BR: eigen2-devel

* Tue Mar 31 2009 Jaroslav Reznik <jreznik@redhat.com> - 4.2.2-2
- split wallpapers and sounds
- noarch subpackages

* Mon Mar 30 2009 Lukáš Tinkl <ltinkl@redhat.com> - 4.2.2-1
- KDE 4.2.2

* Fri Feb 27 2009 Than Ngo <than@redhat.com> - 4.2.1-1
- 4.2.1

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Jan 22 2009 Than Ngo <than@redhat.com> - 4.2.0-1
- 4.2.0

* Sat Jan 10 2009 Than Ngo <than@redhat.com> - 4.1.96-2
- fix file list

* Wed Jan 07 2009 Than Ngo <than@redhat.com> - 4.1.96-1
- 4.2rc1

* Thu Dec 11 2008 Than Ngo <than@redhat.com> -  4.1.85-1
- 4.2beta2

* Wed Nov 26 2008 Than Ngo <than@redhat.com> 4.1.80-3
- enable webcollage since xscreensaver has sane default setting

* Thu Nov 20 2008 Than Ngo <than@redhat.com> 4.1.80-2
- drop duplicated BRs

* Wed Nov 19 2008 Lorenzo Villani <lvillani@binaryhelix.net> - 4.1.80-1
- 4.1.80
- BR cmake 2.6
- make install/fast

* Tue Nov 18 2008 Than Ngo <than@redhat.com> 4.1.3-2
- drop webcollage bz#461926

* Wed Nov 12 2008 Than Ngo <than@redhat.com> 4.1.3-1
- KDE 4.1.3

* Mon Sep 29 2008 Rex Dieter <rdieter@fedoraproject.org> 4.1.2-2
- make VERBOSE=1
- respin against new(er) kde-filesystem

* Fri Sep 26 2008 Rex Dieter <rdieter@fedoraproject.org> 4.1.2-1
- 4.1.2

* Fri Aug 29 2008 Than Ngo <than@redhat.com> 4.1.1-1
- 4.1.1

* Wed Jul 23 2008 Than Ngo <than@redhat.com> 4.1.0-1
- 4.1.0

* Fri Jul 18 2008 Rex Dieter <rdieter@fedoraproject.org> 4.0.99-1
- 4.0.99

* Fri Jul 11 2008 Rex Dieter <rdieter@fedoraproject.org> 4.0.98-1
- 4.0.98

* Sun Jul 06 2008 Rex Dieter <rdieter@fedoraproject.org> 4.0.85-1
- 4.0.85

* Fri Jun 27 2008 Rex Dieter <rdieter@fedoraproject.org> 4.0.84-1
- 4.0.84

* Thu Jun 19 2008 Than Ngo <than@redhat.com> 4.0.83-1
- 4.0.83 (beta2)

* Sun Jun 15 2008 Rex Dieter <rdieter@fedoraproject.org> 4.0.82-1
- 4.0.82

* Wed Jun 04 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.0.80-2
- omit crystalsvg icons for now

* Mon May 26 2008 Than Ngo <than@redhat.com> 4.0.80-1
- 4.1 beta1

* Wed May 07 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.0.72-1
- update to 4.0.72

* Fri Apr 18 2008 Rex Dieter <rdieter@fedoraproject.org> 4.0.3-6
- revert icons noarch hack (wasn't working anyway, rel-eng veto)

* Thu Apr 17 2008 Rex Dieter <rdieter@fedoraproject.org> 4.0.3-5
- -icons: build noarch

* Wed Apr 02 2008 Rex Dieter <rdieter@fedoraproject.org> 4.0.3-3
- -kxs: move here: Requires: kdebase-workspace

* Mon Mar 31 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.0.3-2
- rebuild for NDEBUG and _kde4_libexecdir

* Fri Mar 28 2008 Than Ngo <than@redhat.com> 4.0.3-1
- 4.0.3

* Mon Mar 24 2008 Rex Dieter <rdieter@fedoraproject.org> 4.0.2-3
- kdeartwork-icons-crystalsvg -> crystalsvg-icon-theme
- add scriptlet deps

* Thu Mar 20 2008 Rex Dieter <rdieter@fedoraproject.org> 4.0.2-2
- -icons: Provides: *-icon-theme (Locolor, ikons, kdeclassic, kids, slick)
- include noarch build hooks (not enabled)

* Thu Feb 28 2008 Than Ngo <than@redhat.com> 4.0.2-1
- 4.0.2

* Mon Feb 25 2008 Rex Dieter <rdieter@fedoraproject.org> 4.0.1-3
- %%files: don't own %%_kde4_libdir/kde4/plugins (thanks wolfy!)

* Fri Feb 15 2008 Than Ngo <than@redhat.com> 4.0.1-2
- rebuilt against GCC 4.3

* Sat Feb 09 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.0.1-1
- update to 4.0.1

* Tue Jan 08 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.0.0-1
- update to 4.0.0

* Mon Dec 10 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 3.97.0-1
- kde-3.97.0
- touchup for cvs import
- rework subpkg names a bit

* Fri Nov 30 2007 Sebastian Vahl <fedora@deadbabylon.de> 3.96.2-1
- kde-3.96.2

* Fri Nov 23 2007 Sebastian Vahl <fedora@deadbabylon.de> 3.96.1-1
- kde-3.96.1

* Mon Nov 19 2007 Sebastian Vahl <fedora@deadbabylon.de> 3.96.0-5
- put crystalsvg-icon-theme in it's own subpkg

* Mon Nov 19 2007 Sebastian Vahl <fedora@deadbabylon.de> 3.96.0-4
- BR: kde-filesystem >= 4

* Sun Nov 18 2007 Sebastian Vahl <fedora@deadbabylon.de> 3.96.0-3
- BR: libXtst-devel
- Require kdebase-workspace not kdebase-workspace-devel

* Sun Nov 18 2007 Sebastian Vahl <fedora@deadbabylon.de> 3.96.0-2
- kdeartwork-icons: Provide: crystalsvg-icon-theme

* Sun Nov 18 2007 Sebastian Vahl <fedora@deadbabylon.de> 3.96.0-1
- Initial version for Fedora

* Sat Oct 13 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 3.5.8-1
- kde-3.5.8

* Wed Aug 29 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 3.5.7-4
- License: GPLv2
- (Build)Requires: kdebase3(-devel)

* Wed Aug 29 2007 Fedora Release Engineering <rel-eng at fedoraproject dot org> - 3.5.7-3
- Rebuild for selinux ppc32 issue.

* Fri Jul 13 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 3.5.7-2
- webcollagerc: [directory] /usr/share/backgrounds/images/ (#227683)

* Mon Jun 11 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 3.5.7-1
- 3.5.7

* Thu May 17 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 3.5.6-5
- don't include %%_bindir/kxs* in main pkg
- --enable-final

* Fri May 04 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 3.5.6-4
- resurrect -kxs subpkg (see also #220704)

* Wed Mar 21 2007 Than Ngo <than@redhat.com> - 3.5.6-2.fc7
- cleanup specfile

* Wed Feb 07 2007 han Ngo <than@redhat.com> 3.5.6-1.fc7
- 3.5.6

* Thu Aug 10 2006 Than Ngo <than@redhat.com> 3.5.4-1
- rebuild

* Mon Jul 24 2006 Than Ngo <than@redhat.com> 3.5.4-0.pre1
- prerelease of 3.5.4 (from the first-cut tag)

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 3.5.3-1.1
- rebuild

* Thu Jun 01 2006 Than Ngo <than@redhat.com> 3.5.3-1
- update to 3.5.3

* Wed Apr 05 2006 Than Ngo <than@redhat.com> 3.5.2-1
- update to 3.5.2

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 3.5.1-1.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 3.5.1-1.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Feb 03 2006 Than Ngo <than@redhat.com> 3.5.1-1
- 3.5.1

* Sat Dec 17 2005 Than Ngo <than@redhat.com> 3.5.0-2
- requires on xscreensaver-extras

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Tue Nov 29 2005 Than Ngo <than@redhat.com> 3.5.0-1
- 3.5 final

* Tue Oct 25 2005 Than Ngo <than@redhat.com> 3.4.92-1
- update to 3.5 Beta 2

* Thu Oct 06 2005 Than Ngo <than@redhat.com> 3.4.91-1
- update to 3.5 Beta 1

* Tue Aug 09 2005 Than Ngo <than@redhat.com> 3.4.2-1
- update to 3.4.2

* Thu Jun 30 2005 Than Ngo <than@redhat.com> 3.4.1-2
- configure script does not look the right xscreensaver dirs
  apply patch to fix this problem, #161312, thanks to Rex Dieter

* Tue Jun 28 2005 Than Ngo <than@redhat.com> 3.4.1-1
- 3.4.1

* Fri Mar 18 2005 Than Ngo <than@redhat.com> 3.4.0-1
- 3.4.0

* Fri Mar 04 2005 Than Ngo <than@redhat.com> 3.4.0-0.rc1.2
- rebuilt against gcc-4.0.0-0.31

* Mon Feb 28 2005 Than Ngo <than@redhat.com> 3.4.0-0.rc1.1
- 3.4.0 rc1

* Wed Feb 16 2005 Than Ngo <than@redhat.com> 3.3.92-0.1
- KDE-3.4 Beta2

* Wed Dec 15 2004 Than Ngo <than@redhat.com> 3.3.2-0.3
- fix buildreq on xscreensaver-base

* Mon Dec 06 2004 Than Ngo <than@redhat.com> 3.3.2-0.2
- add correct paths for xscreensaver, xscreensaver-4.18-14 stores the
  config files and graphic hacks in %{_libdir}/xscreensaver/config/hacks
  and %{_libexecdir}/xscreensaver/hacks/

* Fri Dec 03 2004 Than Ngo <than@redhat.com> 3.3.2-0.1
- update to 3.3.2
- remove kdeartwork-3.3.1-kaleidescope.patch, it's included in 3.3.2

* Tue Nov 02 2004 Than Ngo <than@redhat.com> 3.3.1-3
- fix typo in configuration command.

* Mon Oct 18 2004 Than Ngo <than@redhat.com> 3.3.1-2
- rebuilt

* Wed Oct 13 2004 Than Ngo <than@redhat.com> 3.3.1-1
- update to 3.3.1

* Mon Aug 23 2004 Than Ngo <than@redhat.com> 3.3.0-1
- update to 3.3.0 release
- fix file conflict

* Tue Aug 10 2004 Than Ngo <than@redhat.com> 3.3.0-0.1.rc2
- update to 3.3.0 rc2

* Mon Jun 21 2004 Than Ngo <than@redhat.com> 3.2.3-1
- update to 3.2.3

* Mon May 24 2004 Than Ngo <than@redhat.com> 3.2.2-3
- fix file conflict with other kde packages

* Mon May 24 2004 Than Ngo <than@redhat.com> 3.2.2-2
- fix file conflict with other kde packages

* Tue Apr 13 2004 Than Ngo <than@redhat.com> 3.2.2-1
- 3.2.2 release

* Thu Apr 08 2004 Than Ngo <than@redhat.com> 3.2.1-3
- fix file conflict with kdeedu

* Thu Apr 08 2004 Than Ngo <than@redhat.com> 3.2.1-2
- fix icontheme name, bug #119015

* Sun Mar 07 2004 Than Ngo <than@redhat.com> 3.2.1-1
- 3.2.1 release

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Feb 05 2004 Than Ngo <than@redhat.com> 3.2.0-0.3
- 3.2.0 release
- build against qt 3.3.0

* Mon Jan 19 2004 Than Ngo <than@redhat.com> 3.1.95-0.1
- KDE 3.2 RC1

* Mon Dec 15 2003 Than Ngo <than@redhat.com> 3.1.94-0.2
- subpackage for icon

* Mon Dec 01 2003 Than Ngo <than@redhat.com> 3.1.94-0.1
- KDE 3.2 Beta 2

* Thu Nov 27 2003 Than Ngo <than@redhat.com> 3.1.93-0.2
- get rid of rpath

* Wed Nov 12 2003 Than Ngo <than@redhat.com> 3.1.93-0.1
- KDE 3.2 Beta1
- cleanup

* Tue Sep 30 2003 Than Ngo <than@redhat.com> 3.1.4-1
- 3.1.4

* Mon Sep 01 2003 Than Ngo <than@redhat.com> 3.1.3-3
- add requires xscreensaver

* Tue Aug 12 2003 Than Ngo <than@redhat.com> 3.1.3-2
- rebuilt

* Mon Aug 04 2003 Than Ngo <than@redhat.com> 3.1.3-1
- 3.1.3

* Thu Jun 26 2003 Than Ngo <than@redhat.com> 3.1.2-5
- rebuilt

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu May 22 2003 Than Ngo <than@redhat.com> 3.1.2-3
- get rid of buildrequires atomake15

* Mon May 19 2003 Than Ngo <than@redhat.com> 3.1.2-2
- 3.1.2

* Wed Mar 19 2003 Than Ngo <than@redhat.com> 3.1.1-1
- 3.1.1

* Mon Feb 24 2003 Elliot Lee <sopwith@redhat.com>
- debuginfo rebuild

* Fri Feb 21 2003 Than Ngo <than@redhat.com> 3.1-2
- get rid of gcc path from dependency_libs

* Tue Jan 28 2003 Than Ngo <than@redhat.com> 3.1-1
- 3.1 final

* Thu Jan 23 2003 Tim Powers <timp@redhat.com> 3.1-0.4
- rebuild

* Tue Jan 14 2003 Thomas Woerner <twoerner@redhat.com> 3.1-0.3
- removed size_t check
- excluded ia64

* Mon Jan 13 2003 Thomas Woerner <twoerner@redhat.com> 3.1-0.2
- rc6

* Wed Nov 27 2002 Than Ngo <than@redhat.com> 3.1-0.1
- update to 3.1 rc4
- get rid of sub packages

* Sun Nov 10 2002 Than Ngo <than@redhat.com> 3.0.5-1
- update to 3.0.5

* Thu Nov  7 2002 Than Ngo <than@redhat.com> 3.0.4-2
- fix some build problems

* Tue Oct 15 2002 Than Ngo <than@redhat.com> 3.0.4-1
- 3.0.4

* Fri Sep 13 2002 Than Ngo <than@redhat.com> 3.0.3-3.1
- Fixed to build on x86_64

* Mon Sep  2 2002 Than Ngo <than@redhat.com> 3.0.3-3
- Add BuildPrereq automake15

* Sun Aug 25 2002 Than Ngo <than@redhat.com> 3.0.3-2
- rebuild against new qt

* Mon Aug 12 2002 Than Ngo <than@redhat.com> 3.0.3-1
- 3.0.3

* Tue Jul 23 2002 Tim Powers <timp@redhat.com> 3.0.2-3
- build using gcc-3.2-0.1

* Fri Jul 19 2002 Than Ngo <than@redhat.com> 3.0.2-2
- Fixed screen saver issue

* Tue Jul 09 2002 Than Ngo <than@redhat.com> 3.0.2-1
- 3.0.2
- use desktop-file-install

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Tue May 14 2002 Bernhard Rosenkraenzer <bero@redhat.com> 3.0.1-1
- 3.0.1

* Tue Apr 16 2002 Bernhard Rosenkraenzer <bero@redhat.com> 3.0.0-4
- Rebuild

* Wed Mar 27 2002 Than Ngo <than@redhat.com> 3.0.0-3
- final

* Thu Jan 31 2002 Bernhard Rossenkraenzer <bero@redhat.com> 3.0.0-0.cvs20020129.2
- Remove KBlankscreen, it's in kdebase

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Tue Jan  8 2002 Bernhard Rosenkraenzer <bero@redhat.com> 3.0.0-0.cvs20020108.1
- Add missing files

* Mon Jan  7 2002 Bernhard Rosenkraenzer <bero@redhat.com> 3.0.0-0.cvs20020107.1
- Update

* Mon Jul 23 2001 Bernhard Rosenkraenzer <bero@redhat.com> 2.2-0.cvs20010723.1
- Update
