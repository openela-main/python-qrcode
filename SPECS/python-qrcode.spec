%global pkgname qrcode

%if 0%{?rhel} > 7
# Disable python2 build by default
%bcond_with python2
%else
%bcond_without python2
%endif

Name:           python-%{pkgname}
Version:        5.1
Release:        12%{?dist}
Summary:        Python QR Code image generator

License:        BSD
URL:            https://github.com/lincolnloop/python-qrcode
Source0:        http://pypi.python.org/packages/source/q/qrcode/qrcode-%{version}.tar.gz

BuildArch:      noarch

%if %{with python2}
BuildRequires:  python2-devel
BuildRequires:  python2-setuptools
BuildRequires:  python2-imaging
BuildRequires:  python2-six
%endif # with python2

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-imaging
BuildRequires:  python3-six

%global _description\
This module uses the Python Imaging Library (PIL) to allow for the\
generation of QR Codes.\


%description %_description

%if %{with python2}
%package -n python2-%{pkgname}
Summary: %summary
Requires:       python2-imaging
Requires:       python2-%{pkgname}-core = %{version}-%{release}
%{?python_provide:%python_provide python2-%{pkgname}}

%description -n python2-%{pkgname} %_description

%package -n python2-%{pkgname}-core
Requires:       python-six
Conflicts:      python-qrcode < 5.0
Summary:        Python 2 QR Code image generator (core library)
%{?python_provide:%python_provide python2-%{pkgname}-core}

%description -n python2-%{pkgname}-core
Core Python 2 module for QR code generation. Does not contain image rendering.
%endif # with python2


%package -n python3-%{pkgname}
Summary:        Python QR Code image generator
Requires:       python3-imaging
# For entry point:
%if 0%{?rhel} && 0%{?rhel} >= 8
Requires:       platform-python-setuptools
%else
Requires:       python3-setuptools
%endif
Requires:       python3-%{pkgname}-core = %{version}-%{release}

%description -n python3-%{pkgname}
This module uses the Python Imaging Library (PIL) to allow for the
generation of QR Codes. Python 3 version.


%package -n python3-%{pkgname}-core
Requires:       python3-six
Summary:        Python 3 QR Code image generator (core library)

%description -n python3-%{pkgname}-core
Core Python 3 module for QR code generation. Does not contain image rendering.


%prep
%setup -qc

%if %{with python2}
cp -a %{pkgname}-%{version} python2

# The pure plugin requires pymaging which is not packaged in Fedora.
rm python2/qrcode/image/pure.py*

# Remove shebang
sed -i '1d' python2/qrcode/console_scripts.py
%endif # with python2

cp -a %{pkgname}-%{version} python3

# The pure plugin requires pymaging which is not packaged in Fedora.
rm python3/qrcode/image/pure.py*

# Remove shebang
sed -i '1d' python3/qrcode/console_scripts.py


%build
%if %{with python2}
pushd python2
%py2_build
popd
%endif # with python2

pushd python3
%py3_build
popd

%install
%if %{with python2}
pushd python2
%py2_install

# Be sure binscripts are Python 3
rm %{buildroot}%{_bindir}/*

# Do not install tests
rm -r %{buildroot}%{python2_sitelib}/%{pkgname}/tests
popd
%endif # with python2

pushd python3
%py3_install

# Do not install tests
rm -r %{buildroot}%{python3_sitelib}/%{pkgname}/tests
popd

#
# In previous iterations of the package, the qr script had been
# renamed to qrcode. This was an unnecessary change from upstream.
#
# We cary this symlink to maintain compat with old packages.
#
ln -s qr %{buildroot}%{_bindir}/qrcode

%check
# in lieue of a real test suite
modules=$(find qrcode -name '*.py' \
          | grep -v __init__ \
          | sort \
          | sed -e 's|/|.|g' \
          | sed -e 's|.py$||g');


%if %{with python2}
pushd python2
for m in $modules;
do
    %{__python2} -c "import $m"
done
popd
%endif # with python2

pushd python3
for m in $modules;
do
    %{__python3} -c "import $m"
done
popd


%if %{with python2}
%files -n python2-%{pkgname}
%{python2_sitelib}/%{pkgname}/image/svg.py*
%{python2_sitelib}/%{pkgname}/image/pil.py*


%files -n python2-%{pkgname}-core
%doc python2/README.rst python2/CHANGES.rst
%license python2/LICENSE
%dir %{python2_sitelib}/%{pkgname}/
%dir %{python2_sitelib}/%{pkgname}/image
%{python2_sitelib}/%{pkgname}*.egg-info
%{python2_sitelib}/%{pkgname}/*.py*
%{python2_sitelib}/%{pkgname}/image/__init__.py*
%{python2_sitelib}/%{pkgname}/image/base.py*
%endif # with python2


%files -n python3-%{pkgname}
%{_bindir}/qr
%{_bindir}/qrcode
%{_mandir}/man1/qr.1*
%{python3_sitelib}/%{pkgname}/image/svg.py*
%{python3_sitelib}/%{pkgname}/image/pil.py*
%{python3_sitelib}/%{pkgname}/image/__pycache__/svg.*
%{python3_sitelib}/%{pkgname}/image/__pycache__/pil.*


%files  -n python3-%{pkgname}-core
%doc python3/README.rst python3/CHANGES.rst
%license python3/LICENSE
%dir %{python3_sitelib}/%{pkgname}/
%dir %{python3_sitelib}/%{pkgname}/image
%dir %{python3_sitelib}/%{pkgname}/image/__pycache__
%{python3_sitelib}/%{pkgname}*.egg-info
%{python3_sitelib}/%{pkgname}/*.py*
%{python3_sitelib}/%{pkgname}/__pycache__
%{python3_sitelib}/%{pkgname}/image/__init__.py*
%{python3_sitelib}/%{pkgname}/image/base.py*
%{python3_sitelib}/%{pkgname}/image/__pycache__/__init__.*
%{python3_sitelib}/%{pkgname}/image/__pycache__/base.*


%changelog
* Wed Nov 28 2018 Tomas Orsava <torsava@redhat.com> - 5.1-12
- Require platform-python-setuptools instead of python3-setuptools
- Resolves: rhbz#1654457, rhbz#1654458

* Fri Jun 22 2018 Charalampos Stratakis <cstratak@redhat.com> - 5.1-11
- Conditionalize the python2 subpackage

* Tue Mar 20 2018 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 5.1-10
- Also rename python-qrcode-core to python2-qrcode-core

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 5.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Aug 19 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 5.1-8
- Python 2 binary package renamed to python2-qrcode
  See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 5.1-5
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.1-4
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 5.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Fri Jul 10 2015 Miro Hrončok <mhroncok@redhat.com> - 5.1-1
- Update to 5.1
- Introduce python3 subpackages (#1237118)
- Moved LICENSE from %%doc to %%license

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Sep 16 2014 Nathaniel McCallum <npmccallum@redhat.com> - 5.0.1-2
- Make python-qrcode-core conflicts with python-qrcode < 5.0

* Wed Sep 10 2014 Nathaniel McCallum <npmccallum@redhat.com> - 5.0.1-1
- Update to 5.0.1

* Tue Sep 09 2014 Nathaniel McCallum <npmccallum@redhat.com> - 2.4.1-7
- Create -core subpackage for minimal dependencies

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun  6 2012 Michel Salim <salimma@fedoraproject.org> - 2.4.1-2
- Clean up spec, removing unnecessary declarations
- Rename tool in %%{_bindir} to the less ambiguous qrcode

* Sat Jun  2 2012 Michel Salim <salimma@fedoraproject.org> - 2.4.1-1
- Initial package
