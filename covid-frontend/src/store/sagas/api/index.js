import api from 'core/api';

export function * get (path, query = null) {
  return yield apiCall(path, 'GET', query);
}

export function * post (path, query = null, body = null) {
  return yield apiCall(path, 'POST', body ? query : null, body || query);
}

export function * put (url, query = null, body = null) {
  return yield apiCall(url, 'PUT', body ? query : null, body || query);
}

export function * patch (url, query = null, body = null) {
  return yield apiCall(url, 'PATCH', body ? query : null, body || query);
}

export function * del (url, query = null) {
  return yield apiCall(url, 'DELETE', query);
}


function * apiCall (path, method, query, body) {
  const apiInstance = api();
  // const { token } = yield select(state => state.auth);

  // if (token) {
  //   apiInstance.setAuthorization(`Bearer ${token}`);
  // }

  let result;
  try {
    result = yield apiInstance.call(path, method, query, body);
  } catch (error) {
    throw error;
  }

  return result;
}
