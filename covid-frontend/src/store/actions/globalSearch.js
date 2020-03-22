import * as types from 'store/types/globalSearch';

export const setSelectedValue = (payload) => ({
  type: types.SET_SELECTED_VALUE,
  payload
});

export const updateSearchValue = (payload) => ({
  type: types.UPDATE_SEARCH_VALUE,
  payload
});

export const updateLastSearchValue = (payload) => ({
  type: types.UPDATE_LAST_SEARCH_VALUE,
  payload
});

export const updateSearchOptions = (payload) => ({
  type: types.UPDATE_SEARCH_OPTIONS,
  payload
});
export const updateSearchFilters = (payload) => ({
  type: types.UPDATE_SEARCH_FILTERS,
  payload
});

export const setLoadingStatus = (status) => ({
  type: types.SET_LOADING_STATUS,
  status
});

export const reset = () => ({
  type: types.RESET,
});
