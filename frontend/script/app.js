// #region ***  DOM references                           ***********
let localTime,
  selectedGame,
  gameChoiseArrows,
  htmlLeaderboardVandaag,
  htmlLeaderboardOoit,
  htmlGameTitle,
  htmlGameDescription,
  htmlGamePlayers,
  htmlGameUrl,
  previousGame,
  countdownTimer,
  currentGame,
  PrevCurrentGame,
  gameZen,
  gameRedBlue,
  gameSimonSays,
  countdown = 3;
const endpoint = 'http://34.241.254.21:3000/';
const games = ['redblue', 'zen', 'simonsays'];
// #endregion

// #region ***  Callback-Visualisation - show___         ***********
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

const showGameChoice = function (gameData) {
  try {
    for (let game of gameData.games) {
      if (game.name == currentGame) {
        let html = '';
        html += `<a class="c-leaderboard-icon js-test" href="leaderboardkeuze.html?id=${currentGame}">
        <img class="c-leaderboard-icon__svg" src="./img/trophee_icon.svg"
          alt="https://www.freepik.com/free-vector/gold-cups-awards-flat-illustrations-set-collection-golden-trophies-medals-winners-isolated-white_20827758.htm">
        Leaderboard
      </a>`;

        htmlGameUrl.innerHTML = html;
        htmlGameTitle.innerHTML = game.name;
        htmlGameDescription.innerHTML = game.description;
        htmlGamePlayers.innerHTML = game.players;
      }
    }
  } catch (ex) {
    console.info(ex);
  }
  listenToArrows();
};

const showCountdown = function () {
  if (countdown != 0) {
    countdownTimer.innerHTML = countdown;
  } else {
    window.location.replace('http://127.0.0.1:5501/frontend/during_game.html');
    countdown = 3;
  }
  countdown -= 1;
  setTimeout(showCountdown, 1000);
};
// #endregion

// #region ***  Callback-No Visualisation - callback___  ***********

// #endregion

// #region ***  Data Access - get___                     ***********
const getData = (endpoint) => {
  return fetch(endpoint)
    .then((r) => r.json())
    .catch((e) => console.error(e));
};
// #endregion

// #region ***  Event Listeners - listenTo___            ***********
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

const listenToArrows = function () {
  for (let game of gameChoiseArrows) {
    game.addEventListener('click', function () {
      if (game.id == 'left') {
        if (games.indexOf(currentGame) == 0) {
          currentGame = games[games.length - 1];
          if (currentGame != PrevCurrentGame) {
            getData(endpoint + `games`).then(showGameChoice);
          }
        } else {
          currentGame = games[games.indexOf(currentGame) - 1];
          if (currentGame != PrevCurrentGame) {
            getData(endpoint + `games`).then(showGameChoice);
          }
        }
      } else if (game.id == 'right') {
        if (games.indexOf(currentGame) == games.length - 1) {
          currentGame = games[0];
          if (currentGame != PrevCurrentGame) {
            getData(endpoint + `games`).then(showGameChoice);
          }
        } else {
          currentGame = games[games.indexOf(currentGame) + 1];
          if (currentGame != PrevCurrentGame) {
            getData(endpoint + `games`).then(showGameChoice);
          }
        }
      }
      PrevCurrentGame = currentGame;
    });
  }
};
// #endregion

// #region ***  Init / DOMContentLoaded                  ***********
const init = function (total) {
  selectedGame = document.querySelectorAll('.js-selectedGame');
  htmlLeaderboardVandaag = document.querySelector('.js-vandaag');
  htmlLeaderboardOoit = document.querySelector('.js-ooit');
  htmlGameTitle = document.querySelector('.js-gameTitle');
  htmlGameDescription = document.querySelector('.js-gameBeschrijving');
  htmlGamePlayers = document.querySelector('.js-gameSpelers');
  countdownTimer = document.querySelector('.js-countdownTimer');
  gameChoiseArrows = document.querySelectorAll('.js-buttonGameChoise');
  htmlGameUrl = document.querySelector('.js-gameUrl');
  gameRedBlue = document.querySelector('.js-redblue');
  gameZen = document.querySelector('.js-zen');
  gameSimonSays = document.querySelector('.js-simonsays');

  if (document.querySelector('.js-index')) {
    timeBubble();
  }
  if (document.querySelector('.js-gameChoice')) {
    currentGame = 'redblue';
    getData(endpoint + `games`).then(showGameChoice);
    timeBubble();
  }
  if (document.querySelector('.js-settings')) {
    timeBubble();
  }
  if (document.querySelector('.js-countdown')) {
    showCountdown();
  }
  if (document.querySelector('.js-duringGame')) {
    timeBubble();
  }
  if (document.querySelector('.js-scoreboard')) {
    timeBubble();
  }
  if (document.querySelector('.js-leaderboard')) {
    let urlParams = new URLSearchParams(window.location.search);
    let currentGame = urlParams.get('id');
    if (currentGame == 'redblue') {
      gameRedBlue.checked = true;
      gameZen.checked = false;
      gameSimonSays.checked = false;
    } else if (currentGame == 'zen') {
      gameRedBlue.checked = false;
      gameZen.checked = true;
      gameSimonSays.checked = false;
    } else if (currentGame == 'simonsays') {
      gameRedBlue.checked = false;
      gameZen.checked = false;
      gameSimonSays.checked = true;
    }
    getData(endpoint + `leaderboard/${currentGame}`).then(showLeaderboard);
    timeBubble();
  }
};

document.addEventListener('DOMContentLoaded', async function () {
  init();
});
// #endregion
