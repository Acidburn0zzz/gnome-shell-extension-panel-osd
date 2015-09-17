%global git 0205d68
%global uuid panel-osd@berend.de.schouwer.gmail.com
%global github jenslody-gnome-shell-extension-panel-osd
%global checkout git%{git}
%global checkout_date 20150918

Name:           gnome-shell-extension-panel-osd
Version:        1
Release:        0.1.%{checkout_date}%{checkout}%{?dist}
Summary:        Configure the place where notifications are shown

Group:          User Interface/Desktops

# The entire source code is GPLv3+ except convenience.js, which is BSD
License:        GPLv3+ and BSD
URL:            https://github.com/jenslody/gnome-shell-extension-panel-osd
Source0:        https://github.com/jenslody/gnome-shell-extension-panel-osd/tarball/master/%{github}-%{git}.tar.gz
BuildArch:      noarch

BuildRequires:  autoconf, automake, glib2-devel, gnome-common >= 3.10.0, intltool
# In Fedora  >= 24 %%{_datadir}/gnome-shell/extensions/ is owned by gnome-shell,
# before it was owned by gnome-shell-extension-common
%if 0%{?fedora} >= 24
Requires:       gnome-shell >= 3.12.0
%else
Requires:       gnome-shell-extension-common >= 3.12.0
%endif


%description
gnome-shell-extension-panel-osd is an extension to show the notification
messages at any (configurable) place on the (primary) monitor.

%prep
%setup -q -n %{github}-%{git}

%build
NOCONFIGURE=1 ./autogen.sh
%configure --prefix=%{_prefix} GIT_VERSION=${checkout}
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}
%find_lang %{name}

# Fedora uses file-triggers for some stuff (e.g. compile schemas) since fc24.
# Compiling schemas is the only thing done in %%postun and %%posttrans, so
# I decided to make both completely conditional.
%if 0%{?fedora} < 24
%postun
if [ $1 -eq 0 ] ; then
        %{_bindir}/glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
fi

%posttrans
%{_bindir}/glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
%endif

%files -f %{name}.lang
%license COPYING
%doc AUTHORS README.md
%{_datadir}/glib-2.0/schemas/org.gnome.shell.extensions.panel-osd.gschema.xml
%{_datadir}/gnome-shell/extensions/%{uuid}

%changelog
* Thu Sep 17 2015 Jens Lody <fedora@jenslody.de> - 1-0.1.20150918git0205d68
- Use checkout-date instead of build-date in package-version.

* Thu Aug 20 2015 Jens Lody <fedora@jenslody.de> - 1-0.1.20150821gitcb1f6f6
- Remove dot before git in Release-tag.
- Use (conditional) file-triggers for schema compiling, introduced in fc24.

* Sun Jan 26 2014 Jens Lody <jens@jenslody.de>
- Initial package for Fedora of the panel-osd-extension fork

