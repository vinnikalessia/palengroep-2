let localTime,
  chosenGame,
  selectedGame,
  htmlLeaderboardVandaag,
  htmlLeaderboardOoit,
  previousGame;
const endpoint = 'http://34.241.254.21:3000/';

const timeBubble = function () {
  localTime = document.querySelector('.js-time');
  localTime.innerHTML = new Date().toLocaleTimeString([], {
    hour: '2-digit',
    minute: '2-digit',
  });

  setTimeout(timeBubble, 1000);
};

const showLeaderboard = function (data) {
  try {
    let htmlVandaag = '';
    let htmlOoit = '';
    let counter = 0;
    for (let person of data.leaderboard.daily) {
      counter += 1;
      htmlVandaag += `<div class="c-grid__item">${counter}</div>
                            <div class="c-grid__item">${person.team_name}</div>
                            <div class="c-grid__item">${person.score}</div>`;
    }
    counter = 0;
    for (let person of data.leaderboard.alltime) {
      counter += 1;
      htmlOoit += `<div class="c-grid__item">${counter}</div>
                            <div class="c-grid__item">${person.team_name}</div>
                            <div class="c-grid__item">${person.score}</div>`;
    }
    console.log(htmlVandaag);
    console.log(htmlOoit);
    htmlLeaderboardVandaag.innerHTML = htmlVandaag;
    htmlLeaderboardOoit.innerHTML = htmlOoit;
  } catch (ex) {
    console.info(ex);
  }
  listenToChosenGame();
};

const listenToChosenGame = function () {
  for (let game of selectedGame) {
    game.addEventListener('change', function () {
      if (game.id != previousGame) {
        getData(endpoint + `leaderboard/${game.id}`).then(showLeaderboard);
      }
      previousGame = game.id;
    });
  }
};

const getData = (endpoint) => {
  return fetch(endpoint)
    .then((r) => r.json())
    .catch((e) => console.error(e));
};

const init = function (total) {
  chosenGame = document.querySelector('.js-chosenGame');
  selectedGame = document.querySelectorAll('.js-selectedGame');
  htmlLeaderboardVandaag = document.querySelector('.js-vandaag');
  htmlLeaderboardOoit = document.querySelector('.js-ooit');

  if (document.querySelector('.js-leaderboard')) {
    getData(endpoint + `leaderboard/${chosenGame.id}`).then(showLeaderboard);
  }

  timeBubble();
};

document.addEventListener('DOMContentLoaded', async function () {
  init();
});
