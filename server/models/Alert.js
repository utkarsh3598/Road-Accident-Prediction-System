const mongoose = require('mongoose');

const alertSchema = new mongoose.Schema({
  severity: String,
  location: String,
  time: { type: Date, default: Date.now }
});

module.exports = mongoose.model('Alert', alertSchema);
