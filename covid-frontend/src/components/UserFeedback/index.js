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

  closeHandler = () => {
    this.props.answersActions.hideUserFeedbackPanel();
  }

  onFeedbackNegative = (feedback, event) => {
    event.preventDefault()

    this.props.answersActions.markAsWrongAnswer({
      question: this.props.globalSearch,
      answerDocumentId: this.props.answers.userFeedbackPopup && this.props.answers.userFeedbackPopup.answerDocumentId,
      feedback
    });

    this.props.answersActions.hideUserFeedbackPanel();

    return false;
  }


  render() {
    return (
      <div className={styles.wrapper}>
        <div>
          <h2>Thank you for giving us feedback.</h2>
          <p>What was wrong with the answer?</p>
          <button rel="noopener noreferrer" className={styles.answerDocLink}
            onClick={this.onFeedbackNegative.bind(this, 'fake')}>
            <Icon type="warning" /> The stated facts were inaccurate or wrong.
          </button>
          <button rel="noopener noreferrer" className={styles.answerDocLink}
            onClick={this.onFeedbackNegative.bind(this, 'outdated')}>
            <Icon type="clock-circle" /> The information were outdated.
          </button>
          <button rel="noopener noreferrer" className={styles.answerDocLink}
            onClick={this.onFeedbackNegative.bind(this, 'irrelevant')}>
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
