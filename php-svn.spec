%define modname svn
%define dirname %{modname}
%define soname %{modname}.so
%define inifile A47_%{modname}.ini

Summary:	PHP Bindings for the Subversion Revision control system
Name:		php-%{modname}
Version:	1.0.2
Release:	3
Group:		Development/PHP
License:	PHP License
URL:		http://pecl.php.net/package/svn
Source0:	http://pecl.php.net/get/%{modname}-%{version}.tgz
BuildRequires:	php-devel >= 3:5.2.0
BuildRequires:	apache-devel >= 2.2.0
BuildRequires:	subversion-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
PHP Bindings for the Subversion Revision control system.

%prep

%setup -q -n %{modname}-%{version}
[ "../package*.xml" != "/" ] && mv ../package*.xml .

# fix attribs
find -type f | xargs chmod 644

# instead of a patch
perl -pi -e "s|apr-0|apr-1|g" config.m4
perl -pi -e "s|apache2|apache|g" config.m4

# fix version
perl -pi -e "s|^#define PHP_SVN_VERSION .*|#define PHP_SVN_VERSION \"%{version}\"|g" php_svn.h

%build
%serverbuild

export CPPFLAGS="`apr-1-config --cppflags`"

phpize
%configure2_5x --with-libdir=%{_lib} \
    --with-%{modname}=shared,%{_prefix}
%make
mv modules/*.so .

%install
rm -rf %{buildroot} 

install -d %{buildroot}%{_libdir}/php/extensions
install -d %{buildroot}%{_sysconfdir}/php.d

install -m755 %{soname} %{buildroot}%{_libdir}/php/extensions/

cat > %{buildroot}%{_sysconfdir}/php.d/%{inifile} << EOF
extension = %{soname}
EOF

%post
if [ -f /var/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart >/dev/null || :
fi

%postun
if [ "$1" = "0" ]; then
    if [ -f /var/lock/subsys/httpd ]; then
	%{_initrddir}/httpd restart >/dev/null || :
    fi
fi

%clean
rm -rf %{buildroot}

%files 
%defattr(-,root,root)
%doc examples CREDITS EXPERIMENTAL package*.xml 
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/php.d/%{inifile}
%attr(0755,root,root) %{_libdir}/php/extensions/%{soname}


%changelog
* Thu May 03 2012 Oden Eriksson <oeriksson@mandriva.com> 1.0.2-2mdv2012.0
+ Revision: 795510
- rebuild for php-5.4.x

* Thu Mar 29 2012 Oden Eriksson <oeriksson@mandriva.com> 1.0.2-1
+ Revision: 788164
- 1.0.2

* Mon Jan 16 2012 Oden Eriksson <oeriksson@mandriva.com> 1.0.1-7
+ Revision: 761684
- grab the latest code from upstream
- rebuild

* Wed Aug 24 2011 Oden Eriksson <oeriksson@mandriva.com> 1.0.1-6
+ Revision: 696475
- rebuilt for php-5.3.8

* Fri Aug 19 2011 Oden Eriksson <oeriksson@mandriva.com> 1.0.1-5
+ Revision: 695470
- rebuilt for php-5.3.7

* Sat Mar 19 2011 Oden Eriksson <oeriksson@mandriva.com> 1.0.1-4
+ Revision: 646690
- rebuilt for php-5.3.6

* Sat Jan 08 2011 Oden Eriksson <oeriksson@mandriva.com> 1.0.1-3mdv2011.0
+ Revision: 629882
- rebuilt for php-5.3.5

* Mon Jan 03 2011 Oden Eriksson <oeriksson@mandriva.com> 1.0.1-2mdv2011.0
+ Revision: 628196
- ensure it's built without automake1.7

* Thu Dec 09 2010 Oden Eriksson <oeriksson@mandriva.com> 1.0.1-1mdv2011.0
+ Revision: 618071
- 1.0.1

* Thu Dec 02 2010 Paulo Andrade <pcpa@mandriva.com.br> 1.0.0-4mdv2011.0
+ Revision: 605306
- Rebuild with apr with workaround to issue with gcc type based

* Wed Nov 24 2010 Oden Eriksson <oeriksson@mandriva.com> 1.0.0-3mdv2011.0
+ Revision: 600536
- rebuild

* Sun Oct 24 2010 Oden Eriksson <oeriksson@mandriva.com> 1.0.0-2mdv2011.0
+ Revision: 588873
- rebuild

* Tue May 18 2010 Oden Eriksson <oeriksson@mandriva.com> 1.0.0-1mdv2010.1
+ Revision: 545206
- 1.0.0

* Fri Mar 05 2010 Oden Eriksson <oeriksson@mandriva.com> 0.5.1-5mdv2010.1
+ Revision: 514663
- rebuilt for php-5.3.2

* Sat Jan 02 2010 Oden Eriksson <oeriksson@mandriva.com> 0.5.1-4mdv2010.1
+ Revision: 485488
- rebuilt for php-5.3.2RC1

* Sat Nov 21 2009 Oden Eriksson <oeriksson@mandriva.com> 0.5.1-3mdv2010.1
+ Revision: 468259
- rebuilt against php-5.3.1

* Wed Sep 30 2009 Oden Eriksson <oeriksson@mandriva.com> 0.5.1-2mdv2010.0
+ Revision: 451362
- rebuild

* Thu Sep 24 2009 Oden Eriksson <oeriksson@mandriva.com> 0.5.1-1mdv2010.0
+ Revision: 448202
- 0.5.1

* Mon Aug 03 2009 Oden Eriksson <oeriksson@mandriva.com> 0.5.0-7mdv2010.0
+ Revision: 408180
- fix build
- rebuilt for php-5.3.0RC2

  + Raphaël Gertz <rapsys@mandriva.org>
    - Rebuild

* Sun Mar 01 2009 Oden Eriksson <oeriksson@mandriva.com> 0.5.0-5mdv2009.1
+ Revision: 346640
- rebuilt for php-5.2.9

* Tue Feb 17 2009 Oden Eriksson <oeriksson@mandriva.com> 0.5.0-4mdv2009.1
+ Revision: 341813
- rebuilt against php-5.2.9RC2

* Sun Jan 04 2009 Oden Eriksson <oeriksson@mandriva.com> 0.5.0-3mdv2009.1
+ Revision: 324396
- fix build with -Werror=format-security

* Fri Dec 05 2008 Oden Eriksson <oeriksson@mandriva.com> 0.5.0-2mdv2009.1
+ Revision: 310312
- rebuilt against php-5.2.7

* Wed Oct 15 2008 Oden Eriksson <oeriksson@mandriva.com> 0.5.0-1mdv2009.1
+ Revision: 293864
- 0.5.0

* Fri Jul 18 2008 Oden Eriksson <oeriksson@mandriva.com> 0.4.1-3mdv2009.0
+ Revision: 238433
- rebuild

* Thu Jun 26 2008 Oden Eriksson <oeriksson@mandriva.com> 0.4.1-2mdv2009.0
+ Revision: 229357
- rebuild

* Tue Jun 24 2008 Oden Eriksson <oeriksson@mandriva.com> 0.4.1-1mdv2009.0
+ Revision: 228636
- 0.4.1

* Sun Jun 08 2008 Oden Eriksson <oeriksson@mandriva.com> 0.4-1mdv2009.0
+ Revision: 216819
- 0.4

* Fri May 02 2008 Oden Eriksson <oeriksson@mandriva.com> 0.3-2mdv2009.0
+ Revision: 200273
- rebuilt for php-5.2.6

* Mon Feb 11 2008 Oden Eriksson <oeriksson@mandriva.com> 0.3-1mdv2008.1
+ Revision: 165098
- 0.3

* Mon Feb 04 2008 Oden Eriksson <oeriksson@mandriva.com> 0.2-14mdv2008.1
+ Revision: 162248
- rebuild

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Sun Nov 11 2007 Oden Eriksson <oeriksson@mandriva.com> 0.2-13mdv2008.1
+ Revision: 107727
- restart apache if needed

* Sat Sep 01 2007 Oden Eriksson <oeriksson@mandriva.com> 0.2-12mdv2008.0
+ Revision: 77581
- rebuilt against php-5.2.4

* Thu Jun 14 2007 Oden Eriksson <oeriksson@mandriva.com> 0.2-11mdv2008.0
+ Revision: 39527
- use distro conditional -fstack-protector

* Fri Jun 01 2007 Oden Eriksson <oeriksson@mandriva.com> 0.2-10mdv2008.0
+ Revision: 33879
- rebuilt against new upstream version (5.2.3)

* Thu May 03 2007 Oden Eriksson <oeriksson@mandriva.com> 0.2-9mdv2008.0
+ Revision: 21360
- rebuilt against new upstream version (5.2.2)


* Thu Feb 08 2007 Oden Eriksson <oeriksson@mandriva.com> 0.2-8mdv2007.0
+ Revision: 117634
- rebuilt against new upstream version (5.2.1)

* Wed Nov 08 2006 Oden Eriksson <oeriksson@mandriva.com> 0.2-7mdv2007.0
+ Revision: 78109
- rebuilt for php-5.2.0
- Import php-svn

* Mon Aug 28 2006 Oden Eriksson <oeriksson@mandriva.com> 0.2-6
- rebuilt for php-5.1.6

* Thu Jul 27 2006 Oden Eriksson <oeriksson@mandriva.com> 0.2-5mdk
- rebuild

* Sat May 06 2006 Oden Eriksson <oeriksson@mandriva.com> 0.2-4mdk
- rebuilt for php-5.1.4

* Sat May 06 2006 Oden Eriksson <oeriksson@mandriva.com> 0.2-3mdk
- rebuilt for php-5.1.3

* Thu Mar 30 2006 Oden Eriksson <oeriksson@mandriva.com> 0.2-2mdk
- fix url (littletux)

* Mon Mar 20 2006 Oden Eriksson <oeriksson@mandriva.com> 0.2-1mdk
- initial mandriva package

