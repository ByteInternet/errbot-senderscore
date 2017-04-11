import socket
from errbot import BotPlugin, botcmd


class SenderScore(BotPlugin):
    """Plugin to show the mail score of the given address"""

    @botcmd
    def senderscore(self, msg, args):
        """retrieve mail reputation usage !senderscore [IP/Hostname]"""
        if self.is_ip(args):
            ipadresses = args
        else:
            hostname = args
            ips = self.get_host_ips(hostname)
        
        for ip in ipadresses:
            score = self.get_senderscores(ip)
            if score:
                yield ("The reputation of {} is: {}".format(ip, score))
            else:
                yield ("Could'nt find a reputation for: {}".format(ip))

    def get_senderscores(self, ip):
        try:
            tmp = ip.split(".")
            ip_backwards = "%s.%s.%s.%s" % (tmp[3], tmp[2], tmp[1], tmp[0])
        except IndexError:
            return None

        try:
            host = '%s.%s' % (ip_backwards, "score.senderscore.com")
            ret = socket.gethostbyname(host)
        except socket.gaierror as e:
            return None

        return ret.split('.')[3]

    def get_host_ips(self, hostname):
        try:
            ret = socket.gethostbyname_ex(hostname)
        except socket.gaierror as e:
            return None
        return ret[2]

    def is_ip(self, value):
        try:
            socket.inet_aton(value)
            return True
        except OSError:
            return False
