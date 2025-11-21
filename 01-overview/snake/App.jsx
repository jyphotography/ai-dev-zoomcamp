import React, { useState, useEffect, useRef, useCallback } from 'react';
import { Trophy, Play, RefreshCw, ArrowUp, ArrowDown, ArrowLeft, ArrowRight } from 'lucide-react';

// Game Constants
const TILE_COUNT = 20;
const GAME_SPEED = 100;

export default function App() {
  const canvasRef = useRef(null);
  const requestRef = useRef();
  const previousTimeRef = useRef();
  
  // Game State (Refs for mutable data to avoid closure stale state in loops)
  const gameState = useRef({
    snake: [{ x: 10, y: 10 }],
    velocity: { x: 0, y: 0 }, // Start stationary
    food: { x: 5, y: 5 },
    nextVelocity: { x: 0, y: 0 }, // Buffer for input
    isGameRunning: false
  });

  // UI State (Triggers re-renders)
  const [score, setScore] = useState(0);
  const [highScore, setHighScore] = useState(0);
  const [gameOver, setGameOver] = useState(false);
  const [gameStarted, setGameStarted] = useState(false);

  // Audio Context Ref
  const audioCtxRef = useRef(null);

  // Initialize High Score
  useEffect(() => {
    const saved = localStorage.getItem('snakeHighScore');
    if (saved) setHighScore(parseInt(saved));
  }, []);

  // Sound Engine
  const playSound = useCallback((type) => {
    if (!audioCtxRef.current) {
      audioCtxRef.current = new (window.AudioContext || window.webkitAudioContext)();
    }
    const ctx = audioCtxRef.current;
    const oscillator = ctx.createOscillator();
    const gainNode = ctx.createGain();
    
    oscillator.connect(gainNode);
    gainNode.connect(ctx.destination);
    
    const now = ctx.currentTime;

    if (type === 'eat') {
      oscillator.type = 'sine';
      oscillator.frequency.setValueAtTime(600, now);
      oscillator.frequency.exponentialRampToValueAtTime(1000, now + 0.1);
      gainNode.gain.setValueAtTime(0.1, now);
      gainNode.gain.exponentialRampToValueAtTime(0.01, now + 0.1);
      oscillator.start(now);
      oscillator.stop(now + 0.1);
    } else if (type === 'die') {
      oscillator.type = 'sawtooth';
      oscillator.frequency.setValueAtTime(200, now);
      oscillator.frequency.exponentialRampToValueAtTime(50, now + 0.3);
      gainNode.gain.setValueAtTime(0.2, now);
      gainNode.gain.exponentialRampToValueAtTime(0.01, now + 0.3);
      oscillator.start(now);
      oscillator.stop(now + 0.3);
    }
  }, []);

  // Input Handling
  const handleInput = useCallback((key) => {
    const { velocity } = gameState.current;
    
    // Prevent reversing direction directly
    if ((key === 'ArrowUp' || key === 'w') && velocity.y !== 1) {
      gameState.current.nextVelocity = { x: 0, y: -1 };
    } else if ((key === 'ArrowDown' || key === 's') && velocity.y !== -1) {
      gameState.current.nextVelocity = { x: 0, y: 1 };
    } else if ((key === 'ArrowLeft' || key === 'a') && velocity.x !== 1) {
      gameState.current.nextVelocity = { x: -1, y: 0 };
    } else if ((key === 'ArrowRight' || key === 'd') && velocity.x !== -1) {
      gameState.current.nextVelocity = { x: 1, y: 0 };
    }
  }, []);

  useEffect(() => {
    const handleKeyDown = (e) => handleInput(e.key);
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [handleInput]);

  // Game Logic
  const resetGame = () => {
    gameState.current = {
      snake: [{ x: 10, y: 10 }, { x: 10, y: 11 }], // Initial tail
      velocity: { x: 1, y: 0 }, // Start moving right
      nextVelocity: { x: 1, y: 0 },
      food: { x: 15, y: 10 },
      isGameRunning: true
    };
    setScore(0);
    setGameOver(false);
    setGameStarted(true);
    previousTimeRef.current = performance.now();
    requestRef.current = requestAnimationFrame(gameLoop);
  };

  const spawnFood = () => {
    const { snake } = gameState.current;
    let newFood;
    let isOnSnake = true;
    
    while (isOnSnake) {
      newFood = {
        x: Math.floor(Math.random() * TILE_COUNT),
        y: Math.floor(Math.random() * TILE_COUNT)
      };
      // eslint-disable-next-line no-loop-func
      isOnSnake = snake.some(part => part.x === newFood.x && part.y === newFood.y);
    }
    gameState.current.food = newFood;
  };

  const gameLoop = (time) => {
    if (!gameState.current.isGameRunning) return;

    const deltaTime = time - previousTimeRef.current;

    if (deltaTime >= GAME_SPEED) {
      previousTimeRef.current = time;
      update();
      draw();
    }

    requestRef.current = requestAnimationFrame(gameLoop);
  };

  const update = () => {
    const state = gameState.current;
    
    // Apply buffered input
    state.velocity = state.nextVelocity;
    
    const head = { ...state.snake[0] };
    head.x += state.velocity.x;
    head.y += state.velocity.y;

    // Wall Collision
    if (head.x < 0 || head.x >= TILE_COUNT || head.y < 0 || head.y >= TILE_COUNT) {
      return handleGameOver();
    }

    // Self Collision
    if (state.snake.some(part => part.x === head.x && part.y === head.y)) {
      return handleGameOver();
    }

    state.snake.unshift(head); // Add new head

    // Food Collision
    if (head.x === state.food.x && head.y === state.food.y) {
      playSound('eat');
      setScore(s => {
        const newScore = s + 1;
        if (newScore > highScore) {
            setHighScore(newScore);
            localStorage.setItem('snakeHighScore', newScore);
        }
        return newScore;
      });
      spawnFood();
    } else {
      state.snake.pop(); // Remove tail
    }
  };

  const handleGameOver = () => {
    gameState.current.isGameRunning = false;
    playSound('die');
    setGameOver(true);
    if (requestRef.current) cancelAnimationFrame(requestRef.current);
  };

  const draw = () => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    const { snake, food } = gameState.current;
    const tileSize = canvas.width / TILE_COUNT;

    // Clear Screen
    ctx.fillStyle = '#020617';
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    // Draw Food
    ctx.fillStyle = '#f472b6'; // Pink
    ctx.shadowBlur = 15;
    ctx.shadowColor = '#f472b6';
    ctx.fillRect(food.x * tileSize, food.y * tileSize, tileSize - 2, tileSize - 2);

    // Draw Snake
    ctx.fillStyle = '#22d3ee'; // Cyan
    ctx.shadowBlur = 15;
    ctx.shadowColor = '#22d3ee';
    
    snake.forEach((part, index) => {
      if (index === 0) {
        ctx.fillStyle = '#c084fc'; // Purple head
        ctx.shadowColor = '#c084fc';
      } else {
        ctx.fillStyle = '#22d3ee';
        ctx.shadowColor = '#22d3ee';
      }
      ctx.fillRect(part.x * tileSize, part.y * tileSize, tileSize - 2, tileSize - 2);
    });

    // Reset Shadow
    ctx.shadowBlur = 0;
  };

  // Stop loop on unmount
  useEffect(() => {
    return () => cancelAnimationFrame(requestRef.current);
  }, []);

  return (
    <div className="h-screen w-full flex flex-col items-center justify-center bg-slate-900 text-slate-200 font-mono select-none overflow-hidden touch-none">
      
      {/* Header */}
      <div className="w-full max-w-md px-6 mb-6 flex justify-between items-end">
        <div>
          <h1 className="text-cyan-400 text-3xl font-bold drop-shadow-[0_0_10px_rgba(34,211,238,0.5)]">SNAKE</h1>
          <div className="flex items-center gap-2 text-slate-400 text-sm mt-1">
            <Trophy size={14} className="text-yellow-500" />
            <span>HI: <span className="text-cyan-200">{highScore}</span></span>
          </div>
        </div>
        <div className="text-right">
          <div className="text-4xl font-bold text-cyan-400 drop-shadow-[0_0_10px_rgba(34,211,238,0.5)]">{score}</div>
          <div className="text-xs text-slate-400">SCORE</div>
        </div>
      </div>

      {/* Game Board */}
      <div className="relative group rounded-xl overflow-hidden shadow-[0_0_30px_rgba(34,211,238,0.15)] border-4 border-slate-700">
        <canvas 
          ref={canvasRef}
          width={400}
          height={400}
          className="bg-slate-950 block max-w-[90vw] max-h-[50vh]"
        />

        {/* Overlay */}
        {(!gameStarted || gameOver) && (
          <div className="absolute inset-0 bg-black/80 flex flex-col items-center justify-center z-10 backdrop-blur-sm">
            <h2 className={`text-3xl font-bold mb-6 ${gameOver ? 'text-red-500' : 'text-cyan-400'} drop-shadow-lg`}>
              {gameOver ? 'GAME OVER' : 'READY?'}
            </h2>
            
            <button 
              onClick={resetGame}
              className="group relative px-8 py-3 bg-cyan-600 hover:bg-cyan-500 text-white font-bold rounded-lg border-b-4 border-cyan-800 active:border-b-0 active:translate-y-1 transition-all flex items-center gap-2"
            >
              {gameOver ? <RefreshCw size={20} /> : <Play size={20} />}
              {gameOver ? 'TRY AGAIN' : 'START GAME'}
            </button>
            
            {!gameOver && (
              <p className="mt-6 text-xs text-slate-400 flex flex-col items-center gap-1">
                <span>Desktop: Arrow Keys / WASD</span>
                <span>Mobile: On-screen D-Pad</span>
              </p>
            )}
          </div>
        )}
      </div>

      {/* Mobile Controls */}
      <div className="mt-8 grid grid-cols-3 gap-2 w-48">
        <div />
        <ControlButton onClick={() => handleInput('ArrowUp')} icon={<ArrowUp />} />
        <div />
        <ControlButton onClick={() => handleInput('ArrowLeft')} icon={<ArrowLeft />} />
        <ControlButton onClick={() => handleInput('ArrowDown')} icon={<ArrowDown />} />
        <ControlButton onClick={() => handleInput('ArrowRight')} icon={<ArrowRight />} />
      </div>
    </div>
  );
}

// Helper Component for Buttons
const ControlButton = ({ onClick, icon }) => (
  <button 
    className="bg-slate-800 active:bg-slate-700 p-4 rounded-xl border-b-4 border-slate-950 active:border-b-0 active:translate-y-1 transition-all text-cyan-400 flex items-center justify-center shadow-lg"
    onClick={(e) => {
      e.preventDefault(); // Prevent focus issues
      onClick();
    }}
  >
    {icon}
  </button>
);