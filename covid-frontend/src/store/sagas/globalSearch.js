import { all, put, select, takeLatest, delay } from 'redux-saga/effects';
import { message } from 'antd';
import * as api from 'store/sagas/api';
import * as types from 'store/types/globalSearch';
import * as actions from 'store/actions/globalSearch';


export function* getOptions(value) {
  const { currentString, lastString } = yield select(state => state.globalSearch.search);

  // return and reset fields if string is empty
  if (!currentString.length) {
    yield put(actions.updateSearchOptions([]));
    yield put(actions.updateLastSearchValue(''));

    return;
  }

  // return if options for the string already exist
  if (currentString.length && lastString.startsWith(currentString) && currentString.length <= lastString.length) {
    return;
  }

  yield put(actions.setLoadingStatus(true));

  try {
    yield put(actions.updateLastSearchValue(value));
    yield delay(400);
    const data = yield api.get(`/query/autocomplete`, { search: currentString });
    let i = 0;
    const searchResults = data.results.map(question =>{
      return {question, id: i++ };
    });
    console.log('language detection from autocomplete: ', data.language)

    yield put(actions.updateSearchOptions(searchResults));

  } catch (error) {
    message.error(error.message);
  }
  yield put(actions.setLoadingStatus(false));
}

export default function* () {
  yield all([
    takeLatest(types.UPDATE_SEARCH_VALUE, ({ payload }) => getOptions(payload)),
  ]);
}
