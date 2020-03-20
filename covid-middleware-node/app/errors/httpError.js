class HttpError extends Error {

  constructor(status, message) {
    super(message);
    this.status = status;
    this.message = message;
    this.type = 'http';
  }
}

module.exports = HttpError;
