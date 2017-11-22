from disco.bot import Plugin
import code


class RoleManagePlugin(Plugin):

    def load(self, ctx):
        self.game_groups = []

    @Plugin.command('add', '<group:role>')
    def on_add_command(self, event, group):
        if group in self.game_groups:
            event.member.add_role(group)
            event.msg.reply('You have been successfully added to '
                            + group.name)

    @Plugin.command('groupauth', '<group:role>')
    def on_groupauth_command(self, event, group):
        if any((event.guild.roles[r].name == 'Admin')
               for r in event.member.roles):
            self.game_groups.append(group)
            event.msg.reply("auth'd " + group.name)
