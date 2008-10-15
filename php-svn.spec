%define modname svn
%define dirname %{modname}
%define soname %{modname}.so
%define inifile A47_%{modname}.ini

Summary:	PHP Bindings for the Subversion Revision control system
Name:		php-%{modname}
Version:	0.5.0
Release:	%mkrel 1
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

# instead of a patch
perl -pi -e "s|apr-0|apr-1|g" config.m4
perl -pi -e "s|apache2|apache|g" config.m4

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
