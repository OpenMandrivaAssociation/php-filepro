%define modname filepro
%define dirname %{modname}
%define soname %{modname}.so
%define inifile 21_%{modname}.ini

Summary:	FilePro extension module for PHP
Name:		php-%{modname}
Version:	5.1.6
Release:	%mkrel 18
Group:		Development/PHP
License:	PHP License
URL:		http://www.php.net
Source0:	%{modname}.tar.bz2
BuildRequires:	php-devel >= 3:5.2.0
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
This is a dynamic shared object (DSO) for PHP that will add support for
read-only access to filePro databases.

These functions allow read-only access to data stored in filePro databases.
 
filePro is a registered trademark of fP Technologies, Inc. You can find more
information about filePro at http://www.fptech.com/.

%prep

%setup -q -n %{modname}

%build
%serverbuild

phpize
%configure2_5x --with-libdir=%{_lib} \
    --with-%{modname}=shared,%{_prefix}

%make
mv modules/*.so .

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot} 

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
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files 
%defattr(-,root,root)
%doc CREDITS package.xml
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/php.d/%{inifile}
%attr(0755,root,root) %{_libdir}/php/extensions/%{soname}
