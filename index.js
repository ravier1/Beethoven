require("dotenv").config();

const {REST} = require("@discordjs/rest");
const { Routes } = require("discord-api-types");
const { Client, Inents, Collection } = require("discord.js");
const { Player } = require("discord-player");

const fs = require("node.fs");
const path = require("node:path");

const client = new Client({
    intents: [Intents.FLAGS.GUILDS, Intents.FLAGS.GUILD_MESSAGES, Intents.FLAGS.GUILD_VOICE_STATES]
});

//Loadingg all the commmands
const commands = [];
client.commands = new Collection();

const commandsPath = path.join(__dirname, "commands");
const commandFiles = fs.readdirSync(commandsPath).filter(file => file.endsWith(".js"));

for(const file of commandFiles)
{
    const filePath = path.join(commandsPath, file);
    const command = require(filePath);

    client.commands.set(command.data.name, command);
}

