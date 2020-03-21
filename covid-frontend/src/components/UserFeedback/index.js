import React, { PureComponent } from 'react';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import { bindActionCreators } from 'redux';
import { Icon } from 'antd';
import * as answersActions from 'store/actions/activeAnswers';
import styles from './styles.module.scss';

class UserFeedback extends PureComponent {

  static propTypes = {
    globalSearch: PropTypes.object,
    answersActions: PropTypes.object
  }

  onFeedbackPositive = (answerDocumentId, event) => {
    event.preventDefault()
    this.props.answersActions.markAsCorrectAnswer({
      question: this.props.globalSearch,
      answerDocumentId
    });

    return false;
  }

  closeHandler = () => {
    this.props.answersActions.hideUserFeedbackPanel();
  }

  onFeedbackNegative = (answerDocumentId, reason, event) => {
    event.preventDefault()

    this.props.answersActions.markAsWrongAnswer({
      question: this.props.globalSearch,
      answerDocumentId,
      reason
    });

    this.props.answersActions.hideUserFeedbackPanel();

    return false;
  }


  render() {
    const { entries } = this.props.answers;
    const sortedAnswers = entries.sort((a1, a2) => a2.probability - a1.probability);

    const topAnswer = sortedAnswers.length ? sortedAnswers[0] : { context: '', answer: '' };
    const topAnswerMeta = topAnswer.meta || {};

    return (
      <div className={styles.wrapper}>
        <div>
          <h1>Thank you for giving us feedback.</h1>
          <p>What was wrong with the answer?</p>
          <button rel="noopener noreferrer" className={styles.answerDocLink}
            onClick={this.onFeedbackNegative.bind(this, topAnswerMeta.document_id, 'fake')}>
            <Icon type="warning" /> The stated facts were inaccurate or wrong.
          </button>
          <button rel="noopener noreferrer" className={styles.answerDocLink}
            onClick={this.onFeedbackNegative.bind(this, topAnswerMeta.document_id, 'outdated')}>
            <Icon type="clock-circle" /> The information were outdated.
          </button>
          <button rel="noopener noreferrer" className={styles.answerDocLink}
            onClick={this.onFeedbackNegative.bind(this, topAnswerMeta.document_id, 'irrelevant')}>
            <Icon type="question" /> The answer had nothing to do with my question.
          </button>
          <button rel="noopener noreferrer" className={styles.answerDocLink} onClick={this.closeHandler}>
            <Icon type="like" /> Nothing.
          </button>
        </div>
      </div>
    );
  }
}

export default connect(
  state => ({
    globalSearch: state.globalSearch,
    answers: state.activeAnswers
  }),
  dispatch => ({
    answersActions: bindActionCreators(answersActions, dispatch)
  })
)(UserFeedback);
