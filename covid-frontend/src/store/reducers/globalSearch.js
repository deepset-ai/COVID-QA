import * as types from 'store/types/globalSearch';

const initialState = {
  selectedValue: '',
  search: {
    currentString: '',
    lastString: '',
    options: [],
  },
  isLoading: false
};

export default (state = initialState, action) => {
  switch (action.type) {
    case types.SET_SELECTED_VALUE:
      return {
        ...state,
        selectedValue: action.payload,
        search: {
          ...state.search,
          currentString: action.payload
        }
      };
    case types.UPDATE_SEARCH_VALUE:
      return {
        ...state,
        search: {
          ...state.search,
          currentString: action.payload
        }
      };
    case types.UPDATE_LAST_SEARCH_VALUE:
      return {
        ...state,
        search: {
          ...state.search,
          lastString: action.payload
        }
      };
    case types.UPDATE_SEARCH_FILTERS:
      return {
        ...state,
        search: {
          ...state.search,
          filters: action.payload
        }
      };
    case types.UPDATE_SEARCH_OPTIONS:
      return {
        ...state,
        search: {
          ...state.search,
          options: action.payload
        }
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
