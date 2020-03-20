import * as types from 'store/types/activeAnswers';

export const get = () => ({
  type: types.GET
});

export const set = (payload) => ({
  type: types.SET,
  payload
});

export const setLoadingStatus = (status) => ({
  type: types.SET_LOADING_STATUS,
  status
});

export const reset = () => ({
  type: types.RESET,
});
