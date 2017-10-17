from disco.bot import Plugin
from hackerrank.HackerRankAPI import HackerRankAPI
from jinja2 import Environment, FileSystemLoader

KEY = 'hackerrank|2064922-1979|6cef8989650eee47a3b67fb1e4a691c30a7afa29'

MSG_FMT = '''
{mention}

```
{output}
```

Computed in {time} seconds, using {memory} memory.

Additional message: ` {message}`
'''

MSG_ERR = '''
{mention}

`{lang}` is not a valid language
Try my `languages` command
'''

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
        split_src = src.split('```')
        lang = split_src[0].strip()

        if lang not in self.compiler.supportedlanguages():
            event.msg.reply(MSG_ERR.format(
                mention=event.msg.member.user.mention,
                lang=lang))
            return

        source = split_src[1]
        result = self.compiler.run({
            'source': source,
            'lang': lang})

        event.msg.reply()
        # event.msg.reply(MSG_FMT.format(
        #     mention=event.msg.member.user.mention,
        #     output=result.output[0],
        #     time=result.time[0],
        #     memory=humanfriendly.format_size(result.memory[0], binary=True),
        #     message=result.message))

    @Plugin.command('languages')
    def on_lang_command(self, event):
        event.msg.reply('• ' + '\n• '.join(
            self.compiler.supportedlanguages()))

    @Plugin.command('tts', '<input:str...>')
    def on_test_command(self, event, input):
        event.msg.reply(input, tts=True)

    # @Plugin.command('test')
    # def on_test_command(self, event):
