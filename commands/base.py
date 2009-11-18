import os, time
from core.honeypot import HoneyPotCommand
from core.fstypes import *

class command_whoami(HoneyPotCommand):
    def call(self, args):
        self.writeln(self.honeypot.user.username)

class command_cat(HoneyPotCommand):
    def call(self, args):
        path = self.fs.resolve_path(args, self.honeypot.cwd)

        if not path or not self.fs.exists(path):
            self.writeln('bash: cat: %s: No such file or directory' % args)
            return

        fakefile = './honeyfs/%s' % path
        if os.path.exists(fakefile) and \
                not os.path.islink(fakefile) and os.path.isfile(fakefile):
            f = file(fakefile, 'r')
            self.write(f.read())
            f.close()

class command_cd(HoneyPotCommand):
    def call(self, args):
        if not args:
            args = '/root'

        try:
            newpath = self.fs.resolve_path(args, self.honeypot.cwd)
            newdir = self.fs.get_path(newpath)
        except IndexError:
            newdir = None

        if newdir is None:
            self.writeln('bash: cd: %s: No such file or directory' % args)
            return
        self.honeypot.cwd = newpath

class command_rm(HoneyPotCommand):
    def call(self, args):
        for f in args.split(' '):
            path = self.fs.resolve_path(f, self.honeypot.cwd)
            try:
                dir = self.fs.get_path('/'.join(path.split('/')[:-1]))
            except IndexError:
                self.writeln(
                    'rm: cannot remove `%s\': No such file or directory' % f)
                continue
            basename = path.split('/')[-1]
            contents = [x for x in dir]
            for i in dir[:]:
                if i[A_NAME] == basename:
                    if i[A_TYPE] == T_DIR:
                        self.writeln(
                            'rm: cannot remove `%s\': Is a directory' % \
                            i[A_NAME])
                    else:
                        dir.remove(i)

class command_mkdir(HoneyPotCommand):
    def call(self, args):
        for f in args.split(' '):
            path = self.fs.resolve_path(f, self.honeypot.cwd)
            try:
                dir = self.fs.get_path('/'.join(path.split('/')[:-1]))
            except IndexError:
                self.writeln(
                    'mkdir: cannot create directory `%s\': ' % f + \
                    'No such file or directory')
                return
            if f in [x[A_NAME] for x in dir]:
                self.writeln(
                    'mkdir: cannot create directory `test\': File exists')
                return
            dir.append([f, T_DIR, 0, 0, 4096, 16877, time.time(), [], None])

class command_uptime(HoneyPotCommand):
    def call(self, args):
        self.writeln(
            ' %s up 14 days,  3:53,  0 users,  load average: 0.08, 0.02, 0.01' % \
            time.strftime('%T'))
        #self.writeln('USER     TTY      FROM              LOGIN@   IDLE   JCPU   PCPU WHAT')

class command_w(HoneyPotCommand):
    def call(self, args):
        self.writeln(
            ' %s up 14 days,  3:53,  0 users,  load average: 0.08, 0.02, 0.01' % \
            time.strftime('%T'))
        self.writeln('USER     TTY      FROM              LOGIN@   IDLE   JCPU   PCPU WHAT')

class command_echo(HoneyPotCommand):
    def call(self, args):
        self.writeln(args)

class command_exit(HoneyPotCommand):
    def call(self, args):
        self.honeypot.terminal.reset()
        self.writeln('Connection to server closed.')
        self.honeypot.hostname = 'localhost'

class command_clear(HoneyPotCommand):
    def call(self, args):
        self.honeypot.terminal.reset()

class command_vi(HoneyPotCommand):
    def call(self, args):
        self.writeln('E558: Terminal entry not found in terminfo')

class command_hostname(HoneyPotCommand):
    def call(self, args):
        self.writeln(self.honeypot.hostname)

class command_uname(HoneyPotCommand):
    def call(self, args):
        if args.strip() == '-a':
            self.writeln(
                'Linux %s 2.6.26-2-686 #1 SMP Wed Nov 4 20:45:37 UTC 2009 i686 GNU/Linux' % \
                self.honeypot.hostname)
        else:
            self.writeln('Linux')

class command_ps(HoneyPotCommand):
    def call(self, args):
        if args.strip().count('a'):
            output = (
                'USER       PID %%CPU %%MEM    VSZ   RSS TTY      STAT START   TIME COMMAND',
                'root         1  0.0  0.1   2100   688 ?        Ss   Nov06   0:07 init [2]  ',
                'root         2  0.0  0.0      0     0 ?        S<   Nov06   0:00 [kthreadd]',
                'root         3  0.0  0.0      0     0 ?        S<   Nov06   0:00 [migration/0]',
                'root         4  0.0  0.0      0     0 ?        S<   Nov06   0:00 [ksoftirqd/0]',
                'root         5  0.0  0.0      0     0 ?        S<   Nov06   0:00 [watchdog/0]',
                'root         6  0.0  0.0      0     0 ?        S<   Nov06   0:17 [events/0]',
                'root         7  0.0  0.0      0     0 ?        S<   Nov06   0:00 [khelper]',
                'root        39  0.0  0.0      0     0 ?        S<   Nov06   0:00 [kblockd/0]',
                'root        41  0.0  0.0      0     0 ?        S<   Nov06   0:00 [kacpid]',
                'root        42  0.0  0.0      0     0 ?        S<   Nov06   0:00 [kacpi_notify]',
                'root       170  0.0  0.0      0     0 ?        S<   Nov06   0:00 [kseriod]',
                'root       207  0.0  0.0      0     0 ?        S    Nov06   0:01 [pdflush]',
                'root       208  0.0  0.0      0     0 ?        S    Nov06   0:00 [pdflush]',
                'root       209  0.0  0.0      0     0 ?        S<   Nov06   0:00 [kswapd0]',
                'root       210  0.0  0.0      0     0 ?        S<   Nov06   0:00 [aio/0]',
                'root       748  0.0  0.0      0     0 ?        S<   Nov06   0:00 [ata/0]',
                'root       749  0.0  0.0      0     0 ?        S<   Nov06   0:00 [ata_aux]',
                'root       929  0.0  0.0      0     0 ?        S<   Nov06   0:00 [scsi_eh_0]',
                'root      1014  0.0  0.0      0     0 ?        D<   Nov06   0:03 [kjournald]',
                'root      1087  0.0  0.1   2288   772 ?        S<s  Nov06   0:00 udevd --daemon',
                'root      1553  0.0  0.0      0     0 ?        S<   Nov06   0:00 [kpsmoused]',
                'root      2054  0.0  0.2  28428  1508 ?        Sl   Nov06   0:01 /usr/sbin/rsyslogd -c3',
                'root      2103  0.0  0.2   2628  1196 tty1     Ss   Nov06   0:00 /bin/login --     ',
                'root      2105  0.0  0.0   1764   504 tty2     Ss+  Nov06   0:00 /sbin/getty 38400 tty2',
                'root      2107  0.0  0.0   1764   504 tty3     Ss+  Nov06   0:00 /sbin/getty 38400 tty3',
                'root      2109  0.0  0.0   1764   504 tty4     Ss+  Nov06   0:00 /sbin/getty 38400 tty4',
                'root      2110  0.0  0.0   1764   504 tty5     Ss+  Nov06   0:00 /sbin/getty 38400 tty5',
                'root      2112  0.0  0.0   1764   508 tty6     Ss+  Nov06   0:00 /sbin/getty 38400 tty6',
                'root      2133  0.0  0.1   2180   620 ?        S<s  Nov06   0:00 dhclient3 -pf /var/run/dhclient.eth0.pid -lf /var/lib/dhcp3/dhclien',
                'root      4969  0.0  0.1   5416  1024 ?        Ss   Nov08   0:00 /usr/sbin/sshd',
                'root      5673  0.0  0.2   2924  1540 pts/0    Ss   04:30   0:00 -bash',
                'root      5679  0.0  0.1   2432   928 pts/0    R+   04:32   0:00 ps %s' % args,
                )
        else:
            output = (
                '  PID TTY          TIME CMD',
                ' 5673 pts/0    00:00:00 bash',
                ' 5677 pts/0    00:00:00 ps %s' % args,
                )
        for l in output:
            self.writeln(l)

class command_id(HoneyPotCommand):
    def call(self, args):
        self.writeln('uid=0(root) gid=0(root) groups=0(root)')

class command_mount(HoneyPotCommand):
    def call(self, args):
        if len(args.strip()):
            return
        for i in [
                '/dev/sda1 on / type ext3 (rw,errors=remount-ro)',
                'tmpfs on /lib/init/rw type tmpfs (rw,nosuid,mode=0755)',
                'proc on /proc type proc (rw,noexec,nosuid,nodev)',
                'sysfs on /sys type sysfs (rw,noexec,nosuid,nodev)',
                'udev on /dev type tmpfs (rw,mode=0755)',
                'tmpfs on /dev/shm type tmpfs (rw,nosuid,nodev)',
                'devpts on /dev/pts type devpts (rw,noexec,nosuid,gid=5,mode=620)',
                ]:
            self.writeln(i)

class command_pwd(HoneyPotCommand):
    def call(self, args):
        self.writeln(self.honeypot.cwd)

class command_passwd(HoneyPotCommand):
    def start(self):
        self.write('Enter new UNIX password: ')
        self.honeypot.password_input = True
        self.callbacks = [self.ask_again, self.finish]

    def ask_again(self):
        self.write('Retype new UNIX password: ')

    def finish(self):
        self.honeypot.password_input = False
        self.writeln('Sorry, passwords do not match')
        self.writeln(
            'passwd: Authentication information cannot be recovered')
        self.writeln('passwd: password unchanged')
        self.exit()

    def lineReceived(self, line):
        print 'INPUT (passwd):', line
        self.callbacks.pop(0)()

class command_nop(HoneyPotCommand):
    def call(self, args):
        pass

# vim: set sw=4 et:
