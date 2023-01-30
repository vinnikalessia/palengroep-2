// #region ***  DOM references                           ***********
let localTime,
  selectedGame,
  gameChoiceArrows,
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
// const IP = '10.42.0.1';         // raspberry pi
const IP = '0.0.0.0';         // local

const endpoint = `http://${IP}:3000/`;

const games = ['redblue', 'zen', 'simonsays'];
// #endregion

// #region ***  Callback-Visualisation - show___         ***********
const timeBubble = function () {
  localTime = document.querySelector('.js-time');
  localTime.innerHTML = new Date().toLocaleTimeString([], {
    hour: '2-digit',
    minute: '2-digit',
    hourCycle: 'h24',
  });

  setTimeout(timeBubble, 1000);
};

const showLeaderboard = function (data) {
  try {
    console.log(data);
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
          <div class="c-gametitle js-gameTitle">${game.display_name}</div>
          <hr class="c-underline__gamename">
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
      htmlGameTitle.innerHTML = game.display_name;
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
    window.location.replace(`http://${IP}/during_game.html`);
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
  setDuration,
  goto
) {
  let myHeaders = new Headers();
  myHeaders.append('accept', 'application/json');
  myHeaders.append('Content-Type', 'application/json');

  let raw = JSON.stringify({
    game: gameName,
    difficulty: difficultyState,
    teamNames: [teamName1, teamName2],
    duration: setDuration,
  });

  let requestOptions = {
    method: 'POST',
    headers: myHeaders,
    body: raw,
    redirect: 'follow',
  };

  fetch(`${endpoint}game/setup`, requestOptions)
    .then((response) => response.json())
    .then((result) => {
      console.log(result);
      if (goto) {
        window.location.href = goto;
      }
    })
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
  for (let arrow of gameChoiceArrows) {
    arrow.addEventListener('click', function () {
      if (arrow.id == 'left') {
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
      } else if (arrow.id == 'right') {
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

const getURLParam = function (param) {
  const urlParams = new URLSearchParams(window.location.search);
  return urlParams.get(param);
};

const listenToSettingsButtonPage = function () {
  htmlSettingsButton.addEventListener('click', function () {
    let difficultyState;
    // let gameName = document.querySelector('.js-gameTitle').innerHTML;

    const gameName = getURLParam('id');

    let difficultyLevel = document.querySelector(
      '.js-difficultyCheckbox'
    ).checked;
    let teamName1 = document.querySelector('.js-team1Name').value;
    let teamName2 = document.querySelector('.js-team2Name').value;
    let setDuration = htmlSlider.value;

    if (difficultyLevel) {
      difficultyState = 'Snel';
    } else {
      difficultyState = 'Traag';
    }

    callbackSendData(
      gameName,
      difficultyState,
      teamName1,
      teamName2,
      setDuration,
      `http://${IP}/countdown.html`
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

// if (window.location.href.endsWith("during_game.html")) {
let latestGameStatus = {};

const showTeamCard = function (team, teamName, teamScore) {

}

const showGameStatus = function (data) {

  // data looks like:
  //   {
  //   "game": "redblue",
  //   "status": "finished",
  //   "elapsed_time": 45,
  //   "total_duration": 45,
  //   "difficulty": "Traag",
  //   "scores": {
  //     "a": 13,
  //     "b": 14
  //   }
  // }


  const teamNames = Object.keys(data.scores);
  const teams = document.querySelector('.js-teams');

  // check if teams are already there
  if (teams.childElementCount === teamNames.length) {

    // update scores
    for (let teamName in data.scores) {
      document.querySelector(`.js-score[data-team="${teamName}"]`).innerHTML = data.scores[teamName];
    }
  } else {
    // remove old teams
    teams.innerHTML = '';

    // add new teams
    for (let teamName in data.scores) {
      const score = data.scores[teamName];
      const index = teamNames.indexOf(teamName);
      const color = index === 0 ? 'red' : 'blue';
      const element = `
      <div class="c-teamcard">
          <div class="c-teamname js-teamname">${teamName}</div>
          <div class="c-current-score">
            <div class="c-svg__${color}score js-score" data-team="${teamName}">${score}</div>
            <img class="c-svg__${color}chest" src="./img/${color}_chest_with_bubbels.svg" alt="${color}">
          </div>
        </div>`;

      teams.insertAdjacentHTML('beforeend', element);
    }
  }
}

const getDuringGameStatus = function () {
  fetch(`${endpoint}game/status`)
    .then((r) => r.json())
    .then((data) => {
      if (JSON.stringify(latestGameStatus) !== JSON.stringify(data)) {
        latestGameStatus = data;
        showGameStatus(data);

        console.log("game status", data)
      }

      if (data.status === 'stopped') {
        window.location.href = `http://${IP}/scoreboard.html`;
      }

      if (data.status !== "finished")
        setTimeout(getDuringGameStatus, 100);

      else {
        console.log("game finished")
        window.location.href = `http://${IP}/scoreboard.html`;
      }
    });
}

const startGame = function () {
  fetch(`${endpoint}sio/start_game`, {method: "PUT"})
    .then((r) => r.json())
    .then((data) => {
      console.log("start game", data);
    });
}

const stopGame = function () {
  fetch(`${endpoint}sio/stop_game`, {method: "PUT"})
    .then((r) => r.json())
    .then((data) => {
      console.log("stop game", data);
    });
}

const pauseGame = function () {
  fetch(`${endpoint}sio/pause_game`, {method: "PUT"})
    .then((r) => r.json())
    .then((data) => {
      console.log("pause game", data);
    });
}

const resumeGame = function () {
  fetch(`${endpoint}sio/resume_game`, {method: "PUT"})
    .then((r) => r.json())
    .then((data) => {
      console.log("resume game", data);
    });
}

const onPausePress = function () {
  console.log(latestGameStatus)
  if (latestGameStatus.status === "running") {
    pauseGame();
  } else if (latestGameStatus.status === "paused") {
    resumeGame();
  }
}


const setupDuringGameListeners = function () {
  document.querySelector('.js-pause').addEventListener('click', onPausePress);
  document.querySelector('.js-stop').addEventListener('click', stopGame);
}

// #endregion

// #region scoreboard

let finishedGameStatus;

const getAfterGameStatus = function () {
  return new Promise((resolve, reject) => {
    fetch(`${endpoint}game/status`)
      .then((r) => r.json())
      .then((data) => {
        resolve(data);
      })
      .catch((err) => {
        reject(err);
      });
  });
}

const checkFinishedGame = function (gameStatus) {
  return new Promise((resolve, reject) => {
    if (gameStatus.status === "finished") {
      resolve(gameStatus);
    } else {
      reject(gameStatus);
    }
  });
}

const setupScoreboardLinks = function (game) {
  document.querySelector('.js-leaderboard-link').href = `http://${IP}/leaderboard.html?id=${game}`;
}

const fillScoreboard = function (gameStatus) {

  console.log("fillScoreboard", gameStatus);

  const scores = gameStatus.scores;

  const teamNames = Object.keys(scores);

  let scoreHtml = '';


  for (const team of teamNames) {

    const score = scores[team];
    scoreHtml += `
    <div class="c-team-score">
      <span class="c-team">${team}</span> behaalde een<br>score van <span class="c-points">${score}</span> punten.
    </div>
    `
  }

  document.querySelector('.js-scores').innerHTML = scoreHtml;
  setupScoreboardLinks(gameStatus.game);
}

const fillScoreBoardStopped = function (gameStatus) {
  document.querySelector('.js-proficiat-text').innerHTML = "Gestopt!";
  document.querySelector('.js-scores').innerHTML = "";

  setupScoreboardLinks(gameStatus.game);
}

// #endregion


// #region ***  Init / DOMContentLoaded                  ***********
const init = function (total) {
  selectedGame = document.querySelectorAll('.js-selectedGame');
  htmlLeaderboardVandaag = document.querySelector('.js-vandaag');
  htmlLeaderboardOoit = document.querySelector('.js-ooit');
  countdownTimer = document.querySelector('.js-countdownTimer');
  gameChoiceArrows = document.querySelectorAll('.js-buttonGameChoice');
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

    if (document.location.href.includes("leaderboardkeuze.html")) {

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
    }
    getData(endpoint + `leaderboard/${currentGame}`).then(showLeaderboard);
    timeBubble();
  }


  if (document.location.href.endsWith("during_game.html")) {
    startGame();

    getDuringGameStatus();
    setupDuringGameListeners();
  }

  if (document.location.href.endsWith("scoreboard.html")) {
    getAfterGameStatus()
      .then(checkFinishedGame)
      .then(fillScoreboard)
      .catch((gameData) => {
        if (gameData.status === "stopped") {
          fillScoreBoardStopped(gameData)
        } else {
          document.location.href = "during_game.html";
        }
      })
  }
};

document.addEventListener('DOMContentLoaded', async function () {
  init();
});
// #endregion
