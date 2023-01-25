db = db.getSiblingDB('interactieve-palen');

db.createCollection('scores');


db.createCollection('games');

db.games.insertMany([
    {
        name: "redblue",
        display_name: "Red vs Blue",
        description: "Je speelt het spel met 2 teams. Tik zoveel mogelijk de paal van jouw team aan.",
        players: "2 teams",
        num_teams: 2
    },
    {
        name: "zen",
        display_name: "Zen",
        description: "Tik zo snel mogelijk de oplichtende paal aan",
        players: "1",
        num_teams: 1
    },
    {
        name: "simonsays",
        display_name: "Simon Says",
        description: "De palen geven een bepaalde volgorde aan. Volg deze volgorde en tik de palen aan.",
        players: "1",
        num_teams: 1
    }
])
