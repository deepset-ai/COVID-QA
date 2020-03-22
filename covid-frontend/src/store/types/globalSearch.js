import { prefix } from 'core/utils/string';

const searchPrefix = prefix('globalSearch/');

export const SET_SELECTED_VALUE = searchPrefix('SET_SELECTED_VALUE');

export const UPDATE_SEARCH_VALUE = searchPrefix('UPDATE_SEARCH_VALUE');
export const UPDATE_SEARCH_FILTERS = searchPrefix('UPDATE_SEARCH_FILTES');
export const UPDATE_LAST_SEARCH_VALUE = searchPrefix('UPDATE_LAST_SEARCH_VALUE');
export const UPDATE_SEARCH_OPTIONS = searchPrefix('UPDATE_SEARCH_OPTIONS');

export const SET_LOADING_STATUS = searchPrefix('SET_LOADING_STATUS');

export const RESET = searchPrefix('RESET');
