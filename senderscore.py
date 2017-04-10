import socket
from errbot import BotPlugin, botcmd


class SenderScore(BotPlugin):
    """Plugin to show the mail score of the given ip"""

    @botcmd
    def senderscore(self, msg, args):
        """retrieve mail reputation usage !senderscore [IP]"""
        return self.get_senderscores(args)

    def get_senderscores(self, ip):
        try:
            tmp = ip.split(".")
            ip_backwards = "%s.%s.%s.%s" % (tmp[3], tmp[2], tmp[1], tmp[0])
        except IndexError:
            return "the given value is not a valid ip format"

        try:
            host = '%s.%s' % (ip_backwards, "score.senderscore.com")
            ret = socket.gethostbyname(host)
        except socket.gaierror as e:
            return "Could'nt find a reputation for this ip"

        score = ret.split('.')[3]
        return ("The reputation of {} is: {}".format(ip, score))
