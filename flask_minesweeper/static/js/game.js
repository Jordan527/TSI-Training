// Script.js
const numRows = 8;
const numCols = 8;
const numMines = 10;

const gameBoard = document.getElementById("board");
const boardFlags = document.getElementById("flags");

function setDifficulty(difficulty) {
  $.get(`/board/${difficulty}`, function (data, status) {
    document.getElementById("game_options").style.display = "none";
    document.getElementById("reset_button").style.display = "block";
    renderBoard(data.grid, data.flags, data.won, data.lost);
  });
}

function renderBoard(grid, flags, won, lost) {
  gameBoard.innerHTML = "";
  boardFlags.innerHTML = `Flags: ${flags}`;

  if (won || lost) {
    gameBoard.appendChild(
      document.createTextNode(won ? "You won!" : "You lost!")
    );
    gameBoard.appendChild(document.createElement("br"));
  }
  for (let i = 0; i < grid.length; i++) {
    for (let j = 0; j < grid[0].length; j++) {
      const cellElem = document.createElement("div");
      cellElem.className = "cell";
      let cell = grid[i][j];
      if (cell.revealed) {
        // if cell is revealed
        cellElem.classList.add("revealed");
        if (cell.value != "empty" && cell.value != "mine") {
          // if cell is not empty or mine
          cellElem.innerHTML = cell.value;
        } else if (cell.value == "mine") {
          // if cell is mine
          cellElem.innerHTML = "💥";
        }
      }

      if ((won || lost) && cell.value == "mine" && !cell.revealed) {
        // if game is over and cell is mine
        cellElem.classList.add("revealed");
        cellElem.innerHTML = "💣";
      } else if (cell.flagged) {
        // if cell is flagged
        cellElem.innerHTML = "🚩";
      }
      if (!(won || lost)&& !cell.revealed) {
        // if game is not over
        cellElem.addEventListener("contextmenu", (e) => {
          e.preventDefault();
          sendFlag(i, j);
        });
        if (!cell.flagged && !cell.revealed) {
          cellElem.addEventListener("click", () => sendMove(i, j));
        }
      } else {
        cellElem.addEventListener("contextmenu", (e) => {
            e.preventDefault();
          });
      }
      gameBoard.appendChild(cellElem);
    }
    gameBoard.appendChild(document.createElement("br"));
  }
}

function sendMove(y, x) {
  $.get(`/move/${y}/${x}`, { x: x, y: y }, function (data, status) {
    renderBoard(data.grid, data.flags, data.won, data.lost);
  });
}

function sendFlag(y, x) {
  $.get(`/flag/${y}/${x}`, { x: x, y: y }, function (data, status) {
    renderBoard(data.grid, data.flags, data.won, data.lost);
  });
}

function reset(){
    document.getElementById("game_options").style.display = "block";
    gameBoard.innerHTML = "";
    boardFlags.innerHTML = "";
    document.getElementById("reset_button").style.display = "none";
}