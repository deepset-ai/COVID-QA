import React, { PureComponent } from 'react';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import { bindActionCreators } from 'redux';
import { Icon } from 'antd';
import * as answersActions from 'store/actions/activeAnswers';
import styles from './styles.module.scss';
import { withTranslation } from 'react-i18next';

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
    const { t } = this.props;

    return (
      <div className={styles.wrapper}>
        <div>
          <h2>{t('feedback.title')}</h2>
          <p>{t('feedback.text')}</p>
          <button rel="noopener noreferrer" className={styles.answerDocLink}
            onClick={this.onFeedbackNegative.bind(this, 'fake')}>
            <Icon type="warning" /> {t('feedback.fake')}
          </button>
          <button rel="noopener noreferrer" className={styles.answerDocLink}
            onClick={this.onFeedbackNegative.bind(this, 'outdated')}>
            <Icon type="clock-circle" /> {t('feedback.outdated')}
          </button>
          <button rel="noopener noreferrer" className={styles.answerDocLink}
            onClick={this.onFeedbackNegative.bind(this, 'irrelevant')}>
            <Icon type="question" /> {t('feedback.irrelevant')}
          </button>
          <button rel="noopener noreferrer" className={styles.answerDocLink} onClick={this.closeHandler}>
            <Icon type="like" /> {t('feedback.nothing')}
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
)(withTranslation()(UserFeedback));
