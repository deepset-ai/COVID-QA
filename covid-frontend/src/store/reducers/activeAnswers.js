import * as types from 'store/types/activeAnswers';

const initialState = {
  entries: [],

  isLoading: false,

  // the state of the answer-popup
  userFeedbackPopup: {
    visible: false,
    answerDocumentId: null
  },

  // a list of answers which the user has already given his feedback to
  feedbackGiven: {}
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

    case types.SHOW_USER_FEEDBACK_PANEL:
      return {
        ...state,
        userFeedbackPopup: { ...state.userFeedbackPopup, visible: true, answerDocumentId: action.payload }
      };

    case types.HIDE_USER_FEEDBACK_PANEL:
      return {
        ...state,
        userFeedbackPopup: { ...initialState.userFeedbackPopup }
      };

    case types.MARK_AS_FEEDBACK_GIVEN:
      return {
        ...state,
        feedbackGiven: { ...state.feedbackGiven, ...action.payload }
      };

    case types.CLEAR_FEEDBACK_GIVEN:
      return {
        ...state,
        feedbackGiven: { ...initialState.feedbackGiven }
      };

    case types.RESET:
      return {
        ...initialState
      };

    default:
      return state;
  };
};
