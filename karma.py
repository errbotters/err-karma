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

    def update_karma(self, msg, match, increment):
        name = match.group(1)
        update = match.group(2)
        nick = msg.frm.nick
        karmas = self['karma']

        if name == nick:
            return 'Not in this universe, maggot!'
        else:
            if name not in karmas:
                karmas[name] = 0

            if increment:
                karmas[name] += len(update)//2
            else:
                karmas[name] -= len(update)//2

        self['karma'] = karmas

    @re_botcmd(pattern=KARMA_INC_REGEX, prefixed=False)
    def karma_inc(self, msg, match):
        """Increment user's karma (e.g. user++)"""
        self.update_karma(msg, match, True)

    @re_botcmd(pattern=KARMA_DEC_REGEX, prefixed=False)
    def karma_dec(self, msg, match):
        """Decrement user's karma (e.g. user--)"""
        self.update_karma(msg, match, False)

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

    def number_suffix(self, num):
        suffixes = {1: 'st', 2: 'nd', 3: 'rd'}
        i = num if (num < 20) else (num % 10)
        return suffixes.get(i, 'th')

    @botcmd
    def top_karma(self, msg, args):
        """Get n people with most karma points. If argument not
        specified, get 5 people with most karma points."""
        karmas = self['karma']
        output = ''
        karmees = sorted([(value, key) for (key, value) in karmas.items()],
                         reverse=True)

        n = 5
        if len(args) > 0:
            # Takes top 'n' or less if len(karmees) < n
            try:
                n = int(args)
            except ValueError:
                return "Argument must be a number!"
        karmees = karmees[:n]

        for pos, (k, v) in enumerate(karmees, start=1):
            output += '{0}{1} {2} with {3}\n'.format(pos,
                                                     self.number_suffix(pos),
                                                     v, k)

        return output
