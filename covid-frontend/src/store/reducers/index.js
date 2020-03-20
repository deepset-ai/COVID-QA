import { combineReducers } from 'redux';
import globalSearch from './globalSearch';
import activeAnswers from './activeAnswers';

export default combineReducers({
  globalSearch,
  activeAnswers,
});
