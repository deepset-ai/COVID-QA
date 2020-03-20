import { prefix } from 'core/utils/string';

const activeAnswersPrefix = prefix('activeAnswers/');

export const GET = activeAnswersPrefix('GET');
export const SET = activeAnswersPrefix('SET');

export const SET_LOADING_STATUS = activeAnswersPrefix('SET_LOADING_STATUS');

export const RESET = activeAnswersPrefix('RESET');
