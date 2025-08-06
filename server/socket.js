const { Server } = require('socket.io');

let io;

function initSocket(server) {
  io = new Server(server, {
    cors: {
      origin: '*',
      methods: ['GET', 'POST']
    }
  });

  io.on('connection', (socket) => {
    console.log(`📡 Client connected: ${socket.id}`);

    socket.on('send_alert', (data) => {
      console.log("🚨 New alert:", data);
      socket.broadcast.emit('receive_alert', data);
    });

    socket.on('disconnect', () => {
      console.log(`❌ Client disconnected: ${socket.id}`);
    });
  });
}

module.exports = { initSocket };
