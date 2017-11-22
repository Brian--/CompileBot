from disco.bot import Plugin
from hackerrank.HackerRankAPI import HackerRankAPI
from jinja2 import Environment, FileSystemLoader
import code

KEY = 'hackerrank|2064922-1979|6cef8989650eee47a3b67fb1e4a691c30a7afa29'


class CompilePlugin(Plugin):

    def load(self, ctx):
        self.compiler = HackerRankAPI(api_key=KEY)
        env = Environment(loader=FileSystemLoader('templates'))
        self.res_out = env.get_template('result.txt')
        self.lang_out = env.get_template('languages.txt')
        self.err_out = env.get_template('error.txt')
        self.help_out = env.get_template('help.txt')

    @Plugin.command('run', '<src:str...>')
    def on_run_command(self, event, src):
        tokens = list((x.strip() for x in src.split('```') if x.strip()))
        lang = tokens[0]
        args = tokens[1:-1] or ['']
        source = tokens[-1]

        if lang not in self.compiler.supportedlanguages():
            event.msg.reply(self.err_out.render(
                mention=event.msg.member.user.mention,
                error=lang + ' is not a valid language',
                helpcmd='languages'), tts=True)
            return

        if len(tokens) < 2:
            event.msg.reply(self.err_out.render(
                mention=event.msg.member.user.mention,
                error='You must include source to compile.',
                helpcmd='help'), tts=True)
            return

        result = self.compiler.run({
            'source': source,
            'lang': lang,
            'testcases': args})

        if not result:
            event.msg.reply(self.err_out.render(
                mention=event.msg.member.user.mention,
                error='Something weird happened, result object is falsy',
                helpcmd='.`<@195428466450104329>`.'))

        event.msg.reply(self.res_out.render(
            mention=event.msg.member.user.mention,
            result=result or '\n'))

        print(self.res_out.render(
            mention=event.msg.member.user.mention,
            result=result))

    @Plugin.command('languages')
    def on_lang_command(self, event):
        event.msg.reply('• ' + '\n• '.join(
            self.compiler.supportedlanguages())).pin()

    @Plugin.command('help')
    def on_help_command(self, event):
        event.msg.reply(self.help_out.render(
            mention=event.msg.member.user.mention))

    @Plugin.command('repl')
    def on_repl_command(self, event):
        event.msg.reply(event.msg.member.user.mention + " shell running")
        code.interact(local=dict(globals(), **locals()))
        event.msg.reply(event.msg.member.user.mention + " shell stopped")

    @Plugin.command('pin')
    def on_pin_command(self, event):
        event.msg.pin()
        # import inspect
        # for m in inspect.getmembers(event.msg):
        #     print(m)
