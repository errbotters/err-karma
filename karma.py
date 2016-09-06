from errbot import BotPlugin, botcmd, re_botcmd


KARMA_INC_REGEX = '^([a-zA-Z0-9_]+)((:?\+)+)$'
KARMA_DEC_REGEX = '^([a-zA-Z0-9_]+)((:?\-)+)$'


class Karma(BotPlugin):
    def activate(self):
        super(Karma, self).activate()
        try:
            if type(self['karma']) is not dict:
                self['karma'] = {}
        except KeyError:
            self['karma'] = {}

    @re_botcmd(pattern=KARMA_INC_REGEX, prefixed=False)
    def karma_inc(self, msg, match):
        """Increment user's karma (e.g. user++)"""
        name = match.group(1)
        pluses = match.group(2)
        nick = msg.frm.nick
        karmas = self['karma']

        if name == nick:
            return 'Not in this universe, maggot!'
        else:
            if name not in karmas:
                karmas[name] = 0
            karmas[name] += len(pluses)//2

        self['karma'] = karmas 

    @re_botcmd(pattern=KARMA_DEC_REGEX, prefixed=False)
    def karma_dec(self, msg, match):
        """Decrement user's karma (e.g. user--)"""
        name = match.group(1)
        minuses = match.group(2)
        nick = msg.frm.nick
        karmas = self['karma']

        if name == nick:
            return 'Not in this universe, maggot!'
        else:
            if name not in karmas:
                karmas[name] = 0
            karmas[name] -= len(minuses)//2

        self['karma'] = karmas 

    @botcmd
    def karma(self, msg, args):
        """Get karma either of specific user or command caller"""
        karmas = self['karma']
        if not len(args):
            user = msg.frm.nick
        else:
            user = args

        if user not in karmas:
            karmas[user] = 0

        self['karma'] = karmas
        return "{0}'s karma level is: {1}".format(user, karmas[user])

    @botcmd
    def top_karma(self, msg, args):
        """Get 5 people with most karma points."""
        karmas = self['karma']
        output = ""
        karmees = sorted([(value, key) for (key, value) in karmas.items()],
                        reverse=True)
        # Takes top 5 or less if len(karmees) < 5
        karmees = karmees[:5]

        suffixes = ['', 'st', 'nd', 'rd', 'th', 'th']

        for pos, (k, v) in enumerate(karmees, start=1):
            output += "{0}{1} {2} with {3}\n".format(pos, suffixes[pos], v, k)

        return output
