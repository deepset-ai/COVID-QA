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

export const showUserFeedbackPanel = (payload) => ({
  type: types.SHOW_USER_FEEDBACK_PANEL,
  payload
});

export const hideUserFeedbackPanel = () => ({
  type: types.HIDE_USER_FEEDBACK_PANEL
});

export const reset = () => ({
  type: types.RESET,
});

export const markAsCorrectAnswer = (payload) => ({
  type: types.MARK_AS_CORRECT_ANSWER,
  payload
});

export const markAsWrongAnswer = (payload) => ({
  type: types.MARK_AS_WRONG_ANSWER,
  payload
});

export const markAsFeedbackGiven = (payload) => ({
  type: types.MARK_AS_FEEDBACK_GIVEN,
  payload
});

export const clearFeedbackGiven = () => ({
  type: types.CLEAR_FEEDBACK_GIVEN
});