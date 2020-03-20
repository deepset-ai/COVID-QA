import { baseUrl } from 'core/constants/env';

class Api {
  token = null;
  headers = {
    'Content-Type': 'application/json'
  }

  setAuthorization (token) {
    this.token = token;

    return this;
  }

  setHeaders (headers) {
    Object.getOwnPropertyNames(headers).forEach(key => {
      if (headers[key]) {
        this.headers[key] = headers[key];
      } else {
        delete this.headers[key];
      }
    });

    return this;
  }

  get (url, query = null) {
    return this.call(url, 'GET', query);
  }

  post (url, query = null, body = null) {
    return this.call(url, 'POST', body ? query : null, body || query);
  }

  put (url, query = null, body = null) {
    return this.call(url, 'PUT', body ? query : null, body || query);
  }

  del (url, query = null) {
    return this.call(url, 'DELETE', query);
  }

  call (url, method, query = null, body = null) {
    const queryString =
      Object.keys(query || {})
        .map(key => {
          let value = query[key];

          if (typeof value === 'object' && value !== null) {
            value = JSON.stringify(value);
          }

          return `${key}=${encodeURIComponent(value)}`;
        })
        .join('&');

    let options = {
      method,
      headers: {
        ...this.headers,
        // 'Authorization': this.token
      }
    };

    if (body) {
      options.body = body.constructor.name !== 'FormData'
        ? JSON.stringify(body)
        : body;
    }

    const urlString = `${baseUrl}${url}${queryString ? `?${queryString}` : ''}`;

    return fetch(urlString, options).then(response => {
      this.response = response;

      if (response.status >= 200 && response.status < 300) {
        return response.json();
      }

      return response.json()
        .catch(() => {
          // if couldn't parse json
          throw new Error(`${response.status} - ${response.statusText}`);
        })
        // if got a valid json response with error
        .then(error => {
          throw error;
        });
    });
  }
}

export default () => new Api();
