db = db.getSiblingDB('interactieve-palen');

db.createCollection('scores');


db.createCollection('games');

db.games.insertMany([
    {
        name: "redblue",
        display_name: "Red vs Blue",
        description: "Het rode en het blauwe team strijden tegen elkaar. Het team dat het meest aantal punten heeft, wint het spel.",
        players: "Minstens 2 spelers",
        num_teams: 2
    },
    {
        name: "zen",
        display_name: "Zen",
        description: "Probeer het oplichtende paaltje zo snel mogelijk uit te tikken.",
        players: "Maximaal 1 speler",
        num_teams: 1
    },
    {
        name: "simonsays",
        display_name: "Simon Says",
        description: "Herhaal de getoonde volgorde zo lang mogelijk.",
        players: "Maximaal 1 speler",
        num_teams: 1
    }
])
