# Created by pyp2rpm-1.1.1
%global pypi_name unittest2

%bcond_with python2
%bcond_without python3
%bcond_with tests

%{!?python3_pkgversion:%global python3_pkgversion 3}

%if ( "0%{?dist}" == "0.amzn2" )
%global with_amzn2 1
%global bootstrap_traceback2 1
%else
%global bootstrap_traceback2 0
%endif

Name:           python-%{pypi_name}
Version:        1.1.0
Release:        17%{?dist}
Summary:        The new features in unittest backported to Python 2.4+

License:        BSD
URL:            http://pypi.python.org/pypi/unittest2
Source0:        https://pypi.python.org/packages/source/u/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
# we don't need this in Fedora, since we have Python 2.7, which has argparse
Patch0:         unittest2-1.1.0-remove-argparse-from-requires.patch
# we only apply this if bootstrap_traceback2 == 1
Patch1:         unittest2-1.1.0-remove-traceback2-from-requires.patch
# this patch backports tests from Python 3.5, that weren't yet merged, thus the tests are failing
#  (the test is modified to also pass on Python < 3.5)
#  TODO: submit upstream
Patch2:         unittest2-1.1.0-backport-tests-from-py3.5.patch
BuildArch:      noarch


%description
unittest2 is a backport of the new features added to the unittest testing
framework in Python 2.7 and onwards. It is tested to run on Python 2.6, 2.7,
3.2, 3.3, 3.4 and pypy.


%if %{with python2}
%package -n     python2-%{pypi_name}
Summary:        The new features in unittest backported to Python 2.4+
%{?python_provide:%python_provide python2-%{pypi_name}}
%if 0%{?with_amzn2}
BuildRequires:  python2-rpm-macros
BuildRequires:  python-devel
%else
BuildRequires:  python2-devel
%endif
BuildRequires:  python2-setuptools
BuildRequires:  python2-six
%if ! 0%{?bootstrap_traceback2}
BuildRequires:  python2-traceback2
Requires:       python2-traceback2
%endif
Requires:       python2-setuptools
Requires:       python2-six

%description -n python2-%{pypi_name}
unittest2 is a backport of the new features added to the unittest testing
framework in Python 2.7 and onwards. It is tested to run on Python 2.6, 2.7,
3.2, 3.3, 3.4 and pypy.
%endif


%if %{with python3}
%package -n     python%{python3_pkgversion}-%{pypi_name}
Summary:        The new features in unittest backported to Python 2.4+
%{?python_provide:%python_provide python-%{python3_pkgversion}%{pypi_name}}
%if 0%{?with_amzn2}
BuildRequires:  python3-rpm-macros
%endif
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-setuptools
BuildRequires:  python%{python3_pkgversion}-six
%if ! 0%{?bootstrap_traceback2}
BuildRequires:  python%{python3_pkgversion}-traceback2
%endif # bootstrap_traceback2
Requires:       python%{python3_pkgversion}-setuptools
Requires:       python%{python3_pkgversion}-six
%if ! 0%{?bootstrap_traceback2}
Requires:       python%{python3_pkgversion}-traceback2
%endif

%description -n python%{python3_pkgversion}-%{pypi_name}
unittest2 is a backport of the new features added to the unittest testing
framework in Python 2.7 and onwards. It is tested to run on Python 2.6, 2.7,
3.2, 3.3, 3.4 and pypy.
%endif # with_python3


%prep
%setup -q -n %{pypi_name}-%{version}
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

%patch0 -p0
%patch2 -p0
%if 0%{?bootstrap_traceback2}
%patch1 -p0
%endif


%build
%if %{with python2}
%py2_build
%endif
%if %{with python3}
## %%py3_build
## amzn2 has issue with %{py_setup} expansion
CFLAGS="%{optflags}" %{__python3} setup.py %{?py_setup_args} build --executable="%{__python3} %{py3_shbang_opts}" %{?*}
sleep 1
%endif


%install
# Must do the subpackages' install first because the scripts in /usr/bin are
# overwritten with every setup.py install (and we want the python2 version
# to be the default for now).
%if %{with python3}
## %%py3_install
## amzn2 has issue with %{py_setup} expansion
CFLAGS="%{optflags}" %{__python3} setup.py %{?py_setup_args} install -O1 --skip-build --root %{buildroot} %{?*}
pushd %{buildroot}%{_bindir}
mv unit2 unit2-%{python3_version}
ln -s unit2-%{python3_version} unit2-3
# compatibility symlink
ln -s unit2-%{python3_version} python%{python3_pkgversion}-unit2
popd
%endif

%if %{with python2}
%py2_install
pushd %{buildroot}%{_bindir}
mv unit2 unit2-%{python2_version}
ln -s unit2-%{python2_version} unit2-2
ln -s unit2-2 unit2
popd
%endif


%if %{with tests}
%check
%if ! 0%{?bootstrap_traceback2}
%if %{with python2}
%{__python2} -m unittest2
%endif

%if %{with python3}
%{__python3} -m unittest2
%endif # with_python3
%endif # bootstrap_traceback2
%endif


%if %{with python2}
%files -n python2-%{pypi_name}
%doc README.txt
%{_bindir}/unit2
%{_bindir}/unit2-2
%{_bindir}/unit2-%{python2_version}
%{python2_sitelib}/%{pypi_name}
%{python2_sitelib}/%{pypi_name}-%{version}-py?.?.egg-info
%endif


%if %{with python3}
%files -n python%{python3_pkgversion}-%{pypi_name}
%doc README.txt
%{_bindir}/unit2-3
%{_bindir}/unit2-%{python3_version}
%{_bindir}/python%{python3_pkgversion}-unit2
%{python3_sitelib}/%{pypi_name}
%{python3_sitelib}/%{pypi_name}-%{version}-py?.?.egg-info
%endif # with_python3


%changelog
* Mon Jun 17 2019 SaltStack Packaging Team <packaging@saltstack.com> - 1.1.0-17
- Made support for Python 2 optional

* Thu Oct 04 2018 SaltStack Packaging Team <packaging@#saltstack.com> - 1.1.0-16
- Support for Python 3 on Amazon Linux 2

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jun 13 2018 Miro Hrončok <mhroncok@redhat.com> - 1.1.0-14
- Rebuilt for Python 3.7

* Wed Jun 13 2018 Miro Hrončok <mhroncok@redhat.com> - 1.1.0-13
- Bootstrap for Python 3.7

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jan 31 2018 Iryna Shcherbina <ishcherb@redhat.com> - 1.1.0-11
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 12 2016 Charalampos Stratakis <cstratak@redhat.com> - 1.1.0-8
- Disable bootstrap method

* Fri Dec 09 2016 Charalampos Stratakis <cstratak@redhat.com> - 1.1.0-7
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-6
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu May 19 2016 Carl George <carl.george@rackspace.com> - 1.1.0-5
- Implement new Python packaging guidelines (python2 subpackage)

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sun Nov 15 2015 Slavek Kabrda <bkabrda@redhat.com> - 1.1.0-3
- Fix tests on Python 3.5

* Sat Nov 14 2015 Toshio Kuratomi <toshio@fedoraproject.org> - - 1.1.0-2
- traceback2 has been bootstrapped.  Remove the bootstrapping conditional

* Thu Nov 12 2015 bkabrda <bkabrda@redhat.com> - 1.1.0-1
- Update to 1.1.0
- Bootstrap dependency on traceback2

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.0-4
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Nov 14 2014 Slavek Kabrda <bkabrda@redhat.com> - 0.8.0-2
- Bump to avoid collision with previously blocked 0.8.0-1

* Mon Nov 10 2014 Slavek Kabrda <bkabrda@redhat.com> - 0.8.0-1
- Unretire the package, create a fresh specfile
