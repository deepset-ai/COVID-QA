import * as types from 'store/types/activeAnswers';

const initialState = {
  entries: [],

  isLoading: false,
};

export default (state = initialState, action) => {
  switch (action.type) {
    case types.SET:
      return {
        ...state,
        entries: action.payload
      };
    case types.SET_LOADING_STATUS:
      return {
        ...state,
        isLoading: action.status
      };
    case types.RESET:
      return {
        ...initialState
      };
    default:
      return state;
  };
};
