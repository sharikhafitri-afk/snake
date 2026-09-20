<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Snake Game</title>
  <style>
    body {
      margin: 0;
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      background: #111827;
      color: white;
      font-family: Arial, sans-serif;
    }

    h1 {
      margin-bottom: 8px;
    }

    #score {
      margin-bottom: 12px;
      font-size: 20px;
    }

    canvas {
      border: 4px solid #22c55e;
      background: #1f2937;
    }

    button {
      margin-top: 16px;
      padding: 10px 18px;
      border: none;
      border-radius: 6px;
      background: #22c55e;
      color: white;
      font-size: 16px;
      cursor: pointer;
    }

    button:hover {
      background: #16a34a;
    }

    p {
      color: #cbd5e1;
    }
  </style>
</head>
<body>
  <h1>Snake</h1>
  <div id="score">Score: 0</div>

  <canvas id="game" width="400" height="400"></canvas>

  <button onclick="restartGame()">Restart</button>
  <p>Use Arrow Keys or WASD to move</p>

  <script>
    const canvas = document.getElementById("game");
    const ctx = canvas.getContext("2d");
    const scoreText = document.getElementById("score");

    const gridSize = 20;
    const tileCount = canvas.width / gridSize;

    let snake;
    let food;
    let direction;
    let nextDirection;
    let score;
    let gameOver;

    function restartGame() {
      snake = [
        { x: 10, y: 10 },
        { x: 9, y: 10 },
        { x: 8, y: 10 }
      ];

      direction = { x: 1, y: 0 };
      nextDirection = { x: 1, y: 0 };
      score = 0;
      gameOver = false;

      createFood();
      updateScore();
    }

    function createFood() {
      food = {
        x: Math.floor(Math.random() * tileCount),
        y: Math.floor(Math.random() * tileCount)
      };

      const foodOnSnake = snake.some(
        segment => segment.x === food.x && segment.y === food.y
      );

      if (foodOnSnake) {
        createFood();
      }
    }

    function updateScore() {
      scoreText.textContent = `Score: ${score}`;
    }

    function update() {
      if (gameOver) return;

      direction = nextDirection;

      const head = {
        x: snake[0].x + direction.x,
        y: snake[0].y + direction.y
      };

      const hitWall =
        head.x < 0 ||
        head.x >= tileCount ||
        head.y < 0 ||
        head.y >= tileCount;

      const hitSnake = snake.some(
        segment => segment.x === head.x && segment.y === head.y
      );

      if (hitWall || hitSnake) {
        gameOver = true;
        draw();
        setTimeout(() => {
          alert(`Game Over! Your score was ${score}.`);
        }, 100);
        return;
      }

      snake.unshift(head);

      if (head.x === food.x && head.y === food.y) {
        score++;
        updateScore();
        createFood();
      } else {
        snake.pop();
      }

      draw();
    }

    function draw() {
      ctx.fillStyle = "#1f2937";
      ctx.fillRect(0, 0, canvas.width, canvas.height);

      // Draw food
      ctx.fillStyle = "#ef4444";
      ctx.fillRect(
        food.x * gridSize,
        food.y * gridSize,
        gridSize - 2,
        gridSize - 2
      );

      // Draw snake
      snake.forEach((segment, index) => {
        ctx.fillStyle = index === 0 ? "#86efac" : "#22c55e";
        ctx.fillRect(
          segment.x * gridSize,
          segment.y * gridSize,
          gridSize - 2,
          gridSize - 2
        );
      });

      if (gameOver) {
        ctx.fillStyle = "rgba(0, 0, 0, 0.6)";
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        ctx.fillStyle = "white";
        ctx.font = "32px Arial";
        ctx.textAlign = "center";
        ctx.fillText("Game Over", canvas.width / 2, canvas.height / 2);
      }
    }

    document.addEventListener("keydown", event => {
      const key = event.key.toLowerCase();

      if ((key === "arrowup" || key === "w") && direction.y !== 1) {
        nextDirection = { x: 0, y: -1 };
      } else if ((key === "arrowdown" || key === "s") && direction.y !== -1) {
        nextDirection = { x: 0, y: 1 };
      } else if ((key === "arrowleft" || key === "a") && direction.x !== 1) {
        nextDirection = { x: -1, y: 0 };
      } else if ((key === "arrowright" || key === "d") && direction.x !== -1) {
        nextDirection = { x: 1, y: 0 };
      }
    });

    restartGame();
    setInterval(update, 120);
  </script>
</body>
</html>
