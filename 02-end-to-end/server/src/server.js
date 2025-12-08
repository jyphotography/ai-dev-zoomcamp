const express = require('express');
const http = require('http');
const { Server } = require('socket.io');
const cors = require('cors');
const { v4: uuidv4 } = require('uuid');

const app = express();
app.use(cors());
app.use(express.json());

const server = http.createServer(app);
const io = new Server(server, {
  cors: {
    origin: '*',
  }
});

// Simple in-memory session store
const sessions = new Map();

app.post('/session', (req, res) => {
  const id = uuidv4();
  sessions.set(id, { code: '', language: 'javascript' });
  res.json({ id });
});

app.get('/session/:id', (req, res) => {
  const s = sessions.get(req.params.id);
  if (!s) return res.status(404).json({ error: 'Not found' });
  res.json({ id: req.params.id, ...s });
});

io.on('connection', (socket) => {
  socket.on('join', ({ sessionId }) => {
    socket.join(sessionId);
    const s = sessions.get(sessionId) || { code: '', language: 'javascript' };
    socket.emit('init', s);
  });

  socket.on('code:update', ({ sessionId, code }) => {
    const s = sessions.get(sessionId) || { code: '', language: 'javascript' };
    s.code = code;
    sessions.set(sessionId, s);
    socket.to(sessionId).emit('code:update', { code });
  });

  socket.on('language:update', ({ sessionId, language }) => {
    const s = sessions.get(sessionId) || { code: '', language: 'javascript' };
    s.language = language;
    sessions.set(sessionId, s);
    io.in(sessionId).emit('language:update', { language });
  });
});

const PORT = process.env.PORT || 4000;
server.listen(PORT, () => {
  console.log(`Server listening on ${PORT}`);
});
