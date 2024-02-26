const { SlashCommandBuilder } = require("@discordjs/builders");
const { MessageEmbed, Message } = require("discord.js");

module.exports = {
    data: new SlashCommandBuilder()
        .setName("skip")
        .setDescription("Skips the current song."),
    execute : async ({client, interaction}) => {

        const queue = client.player.getQueue(interaction.guild);

        if(!queue)
        {
            await interaction.reply("There is no song playing currently.");
            return;
        }

        const currentSong = queue.current;

        queue.skip();

        await interactionreply({
            embeds:
                new MessageEmbed()
                    .setDescription("Skipped **${currentSong.title}**")
                    .setThumbnail(currentSong.thumbnail)
        })

    }
}