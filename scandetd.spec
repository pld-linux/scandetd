Summary:	Scandetd - daemon recognizing TCP and UDP port scans and OS fingerprinting probes
Summary(pl):	Scandetd - demon rozpoznaj�cy skanowanie port�w TCP i UDP oraz sprawdzanie OS
Name:		scandetd
Version:	1.2.0
Release:	1
License:	GPL
Vendor:		Michal Suszycki <mike@wizard.ae.krakow.pl>
Group:		Networking/Daemons
Source0:	http://wizard.ae.krakow.pl/~mike/download/%{name}-%{version}.tar.gz
# Source0-md5:	187335bb6a3cf59cca38019f2559e1cb
Source1:	%{name}.init
Source2:	%{name}.conf
URL:		http://wizard.ae.krakow.pl/~mike/
Requires:	/usr/sbin/sendmail
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Scandetd is a daemon which tries to recognize TCP and UDP port scans
and OS fingerprinting probes. Program also could be used as a TCP/UDP
connection logger. If it encounters port scan or OS probe it is able
to send an e-mail with following informations:
 - scanning host
 - number of connections made
 - port of the first connection and it's time
 - port of the last one and it's time
 - guessed type of scan (SYN, FIN, NULL) - if it was a TCP scan
 - TCP flags set in packets (if OS probe).

%description -l pl
Scandetd to demon pr�buj�cy rozpozna� skanowanie port�w TCP i UDP oraz
pr�by rozpoznania systemu operacyjnego. Program mo�e by� u�ywany tak�e
do logowania po��cze� TCP/UDP. W przypadku zauwa�enia skanowania
port�w lub pr�b rozpoznania systemu mo�e wys�a� e-mail z nast�puj�cymi
informacjami:
 - skanuj�cy host
 - liczba nawi�zanych po��cze�
 - port i czas przy pierwszym po��czeniu
 - port i czas przy ostatnim po��czeniu
 - prawdopodobny typ skanowania (SYN, FIN, NULL) w przypadk�w skan�w
   TCP
 - flagi TCP ustawione w pakietach (w przypadku pr�b rozpoznania
   systemu operacyjnego).

%prep
%setup -q

%build
CFLAGS="%{rpmcflags}" \
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},/etc/{rc.d/init.d,sysconfig}}
  
install scandetd $RPM_BUILD_ROOT%{_sbindir}
install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add scandetd
        echo "Run \"/etc/rc.d/init.d/scandetd start\" to start scandetd daemons."

%preun
if [ "$1" = "0" ]; then
        if [ -f /var/lock/subsys/scandetd ]; then
        /etc/rc.d/init.d/scandetd stop >&2
        fi
        /sbin/chkconfig --del scandetd
fi

%files
%defattr(644,root,root,755)
%doc README TODO
%attr(755,root,root) %{_sbindir}/%{name}
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%attr(640,root,root) %config(noreplace) %verify(not md5 size mtime) /etc/sysconfig/%{name}
