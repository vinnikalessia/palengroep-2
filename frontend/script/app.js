// #region ***  DOM references                           ***********
let localTime,
  selectedGame,
  gameChoiseArrows,
  htmlLeaderboardVandaag,
  htmlLeaderboardOoit,
  htmlGameUrl,
  htmlGameChoiceMapUrl,
  htmlGameTitle,
  htmlGameDescription,
  htmlGamePlayers,
  htmlSettingsButton,
  htmlSlider,
  htmlSliderValue,
  previousGame,
  countdownTimer,
  currentGame,
  PrevCurrentGame,
  gameZen,
  gameRedBlue,
  gameSimonSays,
  countdown = 3;

// const IP = '34.241.254.21';  // online
const IP = '10.42.0.1';         // raspberry pi

const endpoint = `http://${IP}:3000/`;

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
      if (game.name === currentGame) {
        let html = '';
        let htmlMap = '';
        htmlMap += `<a href="instellingen.html?id=${currentGame}">
        <img class="c-map" src="./img/kaart_horizontaal.png"
          alt="https://www.freepik.com/free-vector/cartoon-parchment-rolls-blank-scrolls-paper-banners_13100350.htm"
          width="814px" height="400px">
        <div class="c-keuze">
          <hr class="c-underline__gamename">
          <div class="c-gametitle js-gameTitle">${game.name}</div>
          <div class="c-gametussentitel">Beschrijving:</div>
          <div class="c-gametekst js-gameBeschrijving">${game.description}</div>
          <div class="c-gametussentitel">Aantal spelers:</div>
          <div class="c-gametekst js-gameSpelers">${game.players}</div>
        </div>
      </a>`;

        html += `<a class="c-leaderboard-icon js-test" href="leaderboardkeuze.html?id=${currentGame}">
        <img class="c-leaderboard-icon__svg" src="./img/trophee_icon.svg"
          alt="https://www.freepik.com/free-vector/gold-cups-awards-flat-illustrations-set-collection-golden-trophies-medals-winners-isolated-white_20827758.htm">
        Leaderboard
      </a>`;

        htmlGameChoiceMapUrl.innerHTML = htmlMap;
        htmlGameUrl.innerHTML = html;
      }
    }
  } catch (ex) {
    console.info(ex);
  }
};

const showSettingsPage = function (gameData) {
  let urlParams = new URLSearchParams(window.location.search);
  let currentGame = urlParams.get('id');
  for (let game of gameData.games) {
    if (game.name === currentGame) {
      htmlGameTitle.innerHTML = game.name;
      htmlGameDescription.innerHTML = game.description;
      htmlGamePlayers.innerHTML = game.players;
    }
  }
  listenToSettingsButtonPage();
};

const showCountdown = function () {
  if (countdown > 0) {
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
const callbackSendData = function (
  gameName,
  difficultyState,
  teamName1,
  teamName2,
  setDuration
) {
  var myHeaders = new Headers();
  myHeaders.append('accept', 'application/json');
  myHeaders.append('Content-Type', 'application/json');

  var raw = JSON.stringify({
    game: gameName,
    difficulty: difficultyState,
    teamNames: [teamName1, teamName2],
    duration: setDuration,
  });

  var requestOptions = {
    method: 'POST',
    headers: myHeaders,
    body: raw,
    redirect: 'follow',
  };

  fetch('http://34.241.254.21:3000/game/setup', requestOptions)
    .then((response) => response.json())
    .then((result) => console.log(result))
    .catch((error) => console.log('error', error));
};

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
          console.log(currentGame);
        } else {
          currentGame = games[games.indexOf(currentGame) - 1];
          if (currentGame != PrevCurrentGame) {
            getData(endpoint + `games`).then(showGameChoice);
          }
          console.log(currentGame);
        }
      } else if (game.id == 'right') {
        if (games.indexOf(currentGame) == games.length - 1) {
          currentGame = games[0];
          if (currentGame != PrevCurrentGame) {
            getData(endpoint + `games`).then(showGameChoice);
          }
          console.log(currentGame);
        } else {
          currentGame = games[games.indexOf(currentGame) + 1];
          if (currentGame != PrevCurrentGame) {
            getData(endpoint + `games`).then(showGameChoice);
          }
          console.log(currentGame);
        }
      }
      PrevCurrentGame = currentGame;
    });
  }
};

const listenToSettingsButtonPage = function () {
  htmlSettingsButton.addEventListener('click', function () {
    let difficultyState;
    let gameName = document.querySelector('.js-gameTitle').innerHTML;
    let difficultyLevel = document.querySelector(
      '.js-difficultyCheckbox'
    ).checked;
    let teamName1 = document.querySelector('.js-team1Name').value;
    let teamName2 = document.querySelector('.js-team2Name').value;
    let setDuration = htmlSlider.value;

    if (difficultyLevel == true) {
      difficultyState = 'Snel';
    } else {
      difficultyState = 'Traag';
    }

    callbackSendData(
      gameName,
      difficultyState,
      teamName1,
      teamName2,
      setDuration
    );
  });
};

const listenToSlider = function () {
  htmlSlider.oninput = function () {
    htmlSliderValue.innerHTML = `${this.value}s`;
  };
};
// #endregion


// #region mqtt stuff


const mqttURL = `mqtt://${IP}:1883`

const options = {
  // Clean session
  clean: true,
  connectTimeout: 4000,
  // Authentication
  clientId: 'frontend',
  // username: 'emqx_test',
  // password: 'emqx_test',
}


const client  = mqtt.connect(mqttURL, options)
client.on('connect', function () {
  console.log('Connected')
  // Subscribe to a topic
  client.subscribe('test', function (err) {
    if (!err) {
      // Publish a message to a topic
      client.publish('test', 'Hello mqtt')
    }
  })
})

// #endregion

// #region ***  Init / DOMContentLoaded                  ***********
const init = function (total) {
  selectedGame = document.querySelectorAll('.js-selectedGame');
  htmlLeaderboardVandaag = document.querySelector('.js-vandaag');
  htmlLeaderboardOoit = document.querySelector('.js-ooit');
  countdownTimer = document.querySelector('.js-countdownTimer');
  gameChoiseArrows = document.querySelectorAll('.js-buttonGameChoise');
  htmlGameUrl = document.querySelector('.js-gameUrl');
  gameRedBlue = document.querySelector('.js-redblue');
  gameZen = document.querySelector('.js-zen');
  gameSimonSays = document.querySelector('.js-simonsays');
  htmlGameChoiceMapUrl = document.querySelector('.js-gameChoiceMap');
  htmlGameTitle = document.querySelector('.js-gameTitle');
  htmlGameDescription = document.querySelector('.js-gameDescription');
  htmlGamePlayers = document.querySelector('.js-gamePlayers');
  htmlSettingsButton = document.querySelector('.js-settingsButton');
  htmlSlider = document.querySelector('.js-slider');
  htmlSliderValue = document.querySelector('.js-sliderValue');


  if (document.querySelector('.js-index')) {
    timeBubble();
  }
  if (document.querySelector('.js-gameChoice')) {
    currentGame = 'redblue';
    getData(endpoint + `games`).then(showGameChoice);
    listenToArrows();
    timeBubble();
  }
  if (document.querySelector('.js-settings')) {
    getData(endpoint + `games`).then(showSettingsPage);
    listenToSlider();
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
    if (currentGame === 'redblue') {
      gameRedBlue.checked = true;
      gameZen.checked = false;
      gameSimonSays.checked = false;
    } else if (currentGame === 'zen') {
      gameRedBlue.checked = false;
      gameZen.checked = true;
      gameSimonSays.checked = false;
    } else if (currentGame === 'simonsays') {
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
