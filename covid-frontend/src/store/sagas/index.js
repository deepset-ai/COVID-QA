import { all, fork } from 'redux-saga/effects';
import activeAnswersSaga from './activeAnswers';
import globalSearchSaga from './globalSearch';

export default function* rootSaga() {
  yield all([
    fork(activeAnswersSaga),
    fork(globalSearchSaga),
  ]);
}
