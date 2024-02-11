require("dotenv").config();

const {REST} = require("@discordjs/rest");
const { Routes } = require("discord-api-types");
const { Client, Inents, Collection } = require("discord.js");
const { Player } = require("discord-player");

const fs = require("node.fs");
const path = require("node:path");