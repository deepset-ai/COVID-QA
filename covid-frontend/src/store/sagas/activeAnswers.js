import { all, put, select, takeLatest } from 'redux-saga/effects';
import { message } from 'antd';
import * as api from 'store/sagas/api';
import * as globalSearchTypes from 'store/types/globalSearch';
import * as types from 'store/types/activeAnswers';
import * as actions from 'store/actions/activeAnswers';


export function* get() {
  const { selectedValue } = yield select(state => state.globalSearch);

  // reset active answers and return if no question is selected
  if (!selectedValue) {
    yield put(actions.set([]));

    return;
  }

  yield put(actions.setLoadingStatus(true));
  try {
    const data = yield api.post(`/bert/question`, null, { question: selectedValue });

    yield put(actions.set(data.answers));

  } catch (error) {
    message.error(error.message);
  }
  yield put(actions.setLoadingStatus(false));
}

export function* markAsCorrectAnswer({ question, answerDocumentId }) {
  if (!question.selectedValue || answerDocumentId <= 0) {
    // do nothing
    return;
  }

  try {
    const id = parseInt(answerDocumentId, 10);
    yield api.post(`/feedback`, null, { question: question.selectedValue, document_id: id });

  } catch (error) {
    message.error(error.message);
  }
}

export function* markAsWrongAnswer({ question, answerDocumentId, reason }) {
  if (!question.selectedValue || answerDocumentId <= 0) {
    // do nothing
    return;
  }

  try {
    const id = parseInt(answerDocumentId, 10);
    yield api.post(`/feedback`, null, { question: question.selectedValue, document_id: id, reason });

  } catch (error) {
    message.error(error.message);
  }
}

export default function* () {
  yield all([
    takeLatest([types.GET, globalSearchTypes.SET_SELECTED_VALUE], get),
    takeLatest([types.MARK_AS_CORRECT_ANSWER], ({ payload }) => markAsCorrectAnswer(payload)),
    takeLatest([types.MARK_AS_WRONG_ANSWER], ({ payload }) => markAsWrongAnswer(payload)),
  ]);
}