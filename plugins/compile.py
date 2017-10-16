from disco.bot import Plugin
from hackerrank.HackerRankAPI import HackerRankAPI
import humanfriendly


KEY = 'hackerrank|2064922-1979|6cef8989650eee47a3b67fb1e4a691c30a7afa29'

MSG_FMT = '''
{mention}

```
{output}
```

Computed in {time} seconds, using {memory} memory.

Additional message: ` {message}`
'''

class CompilePlugin(Plugin):

    def load(self, ctx):
        self.compiler = HackerRankAPI(api_key=KEY)

    @Plugin.command('run', '<src:str...>')
    def on_run_command(self, event, src):
        split_src = src.split('```')

        result = self.compiler.run({
            'source': split_src[1],
            'lang': split_src[0].strip()})

        print(type(result.output))

        event.msg.reply(MSG_FMT.format(
            mention=event.msg.member.user.mention,
            output=(result.output[0][:1750] + '(truncated)') if len(result.output[0]) > 1750 else result.output[0],
            time=result.time[0],
            memory=humanfriendly.format_size(result.memory[0], binary=True),
            message=result.message))

    @Plugin.command('languages')
    def on_lang_command(self, event):
        event.msg.reply('• ' + '\n• '.join(
            self.compiler.supportedlanguages()))

    @Plugin.command('tts', '<input:str...>')
    def on_test_command(self, event, input):
        event.msg.reply(input, tts=True)

    # @Plugin.command('test')
    # def on_test_command(self, event):
