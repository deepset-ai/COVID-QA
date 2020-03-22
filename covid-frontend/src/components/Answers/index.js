import React, { PureComponent, Fragment } from 'react';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import { bindActionCreators } from 'redux';
import { Row, Col, AutoComplete, Empty, Icon } from 'antd';
import links from 'routes/links';
import * as globalSearchActions from 'store/actions/globalSearch';
import * as answersActions from 'store/actions/activeAnswers';
import { InputContainer, Tag } from 'components/common';
import styles from './styles.module.scss';
import UserFeedback from 'components/UserFeedback';

class Answers extends PureComponent {

  static propTypes = {
    history: PropTypes.object,
    globalSearch: PropTypes.object,
    globalSearchActions: PropTypes.object,
    answersActions: PropTypes.object
  }

  handleQuestionSearch = (value) => {
    this.props.globalSearchActions.updateSearchValue(value);
  }

  handleQuestionSelect = (value, option) => {
    this.props.globalSearchActions.setSelectedValue(option.props.children);
  }

  onKeyDown = ({ keyCode, target }) => {
    if (keyCode === 13) {
      this.props.globalSearchActions.setSelectedValue(target.value);
    }
  }

  onFeedbackPositive = (answerDocumentId, event) => {
    event.preventDefault()
    this.props.answersActions.markAsCorrectAnswer({
      question: this.props.globalSearch,
      answerDocumentId
    });

    return false;
  }

  onFeedbackNegative = (answerDocumentId, event) => {
    event.preventDefault()

    this.props.answersActions.showUserFeedbackPanel(answerDocumentId);
    return false;
  }

  feedbackGiven = (answerDocumentId, feedbackPositive) => {
    const feedback = feedbackPositive ? ['relevant'] : ['irrelevant', 'outdated', 'fake']
    return feedback.indexOf(this.props.answers.feedbackGiven[answerDocumentId]) >= 0;
  }

  renderFeedbackLink = ({document_id}, feedbackPositive) => {
    const contraryFeedbackAlreadyGiven = this.feedbackGiven(document_id, !feedbackPositive);

    // hide the button if the contrary feedback has been given
    if (contraryFeedbackAlreadyGiven) {
      return '';
    }

    const feedbackAlreadyGiven = this.feedbackGiven(document_id, feedbackPositive);
    const theme = feedbackAlreadyGiven ? 'filled' : 'outlined';
    const clazz = feedbackPositive ? styles.answerDocLinkPositive : styles.answerDocLinkNegative;
    const className = feedbackAlreadyGiven ? clazz : styles.answerDocLink;
    const icon = feedbackPositive ? 'like' : 'dislike'
    let onClickHandler = (e) => e.preventDefault();

    if (!feedbackAlreadyGiven) {
      onClickHandler = feedbackPositive
        ? this.onFeedbackPositive.bind(this, document_id)
        : this.onFeedbackNegative.bind(this, document_id);
    }

    return (
      <a href='#upvote' rel="noopener noreferrer" className={className} 
        onClick={onClickHandler}>
        <Icon type={icon} theme={theme}/>
      </a>
    );
  }

  renderTag = (probability) => {
    const value = probability * 100;
    const theme = value >= 80 ? Tag.themes.GREEN : value >= 30 ? Tag.themes.ORANGE : Tag.themes.RED;
    const roundedValue = parseFloat(value).toFixed(2);
    return (
      <Tag
        text={`Confidence: ${roundedValue}%`}
        theme={theme}
        className={styles.tag}
      />
    );
  }

  componentDidMount () {
    const { selectedValue } = this.props.globalSearch;

    if (!selectedValue.length) {
      this.props.history.push(links.home);

      return;
    }

    this.props.answersActions.get();
  }

  render() {
    const { search } = this.props.globalSearch;
    const { entries, isLoading } = this.props.answers;
    const showUserFeedbackPanel = this.props.answers.userFeedbackPopup && !!this.props.answers.userFeedbackPopup.visible;
    const sortedAnswers = entries.sort((a1, a2) => a2.probability - a1.probability);

    const topAnswer = sortedAnswers.length ? sortedAnswers[0] : { context: '', answer: '' };
    const topAnswerParts = topAnswer.context.split(topAnswer.answer);
    const topAnswerMeta = topAnswer.meta || {};

    const otherAnswers = sortedAnswers.slice(1);

    return (
      <div className={styles.wrapper}>
        { showUserFeedbackPanel && <UserFeedback></UserFeedback> }

        <Row gutter={24} className={styles.titleRow}>
          <Col span={24}>
            <InputContainer label="Question" fluid>
              <AutoComplete
                className={styles.autocomplete}
                size="large"
                value={search.currentString}
                defaultActiveFirstOption={false}
                placeholder="Ask any question about Corona..."
                filterOption={(value, option) =>
                  option.props.children.toLowerCase().startsWith(value.toLowerCase())
                  // option.props.children.toLowerCase().indexOf(value.toLowerCase()) !== -1 // to show all options with substring
                }
                onSearch={this.handleQuestionSearch}
                onSelect={this.handleQuestionSelect}
                onInputKeyDown={this.onKeyDown}
              >
                {
                  search.options.map(item =>
                    <AutoComplete.Option key={item.id}>{item.question}</AutoComplete.Option>
                  )
                }
              </AutoComplete>
            </InputContainer>
          </Col>
        </Row>

        {
          isLoading ? (
            <div className={styles.loaderContainer}>
              <div className="loader">
                <div className="loader-part l1" />
                <div className="loader-part l2" />
                <div className="loader-part l3" />
              </div>
              <h2>The BERT is working</h2>
              <div>Please Wait</div>
            </div>
          ) : (
            <div className={styles.list}>
              {
                topAnswer.hasOwnProperty('probability') ? (
                  <Fragment>
                    <Row>
                      <Col>
                        <div className={styles.topAnswerTitle}>
                          Top answer
                        </div>
                      </Col>
                    </Row>
                    <Row gutter={[24, 40]}>
                      <Col span={19}>
                        <div
                          className={styles.answerTitle}>{topAnswer.question}</div>
                        <div className={styles.answerText}>
                          {
                            topAnswer.answer ? (
                              <Fragment>
                                {topAnswerParts[0]}
                                <span>{topAnswer.answer}</span>
                                {topAnswerParts[1]}
                              </Fragment>
                            ) : topAnswer.context || '-'
                          }

                        </div>
                        <div className={styles.answerMeta}>
                          <div><span>Updated:</span>{topAnswerMeta.last_update || '–'}</div>
                          <div>
                            <span>Source:</span> {topAnswerMeta.source || '–'}
                            {
                              topAnswerMeta.link && (
                                <a href={topAnswerMeta.link} target="_blank" rel="noopener noreferrer" className={styles.answerDocLink}>
                                  <Icon type="link" />
                                </a>
                              )
                            }
                          </div>
                          <div>
                            <span>Feedback:</span>
                          { this.renderFeedbackLink(topAnswerMeta, true) }
                          { this.renderFeedbackLink(topAnswerMeta, false) }
                          </div>
                        </div>
                      </Col>
                      <Col span={5}>
                        {this.renderTag(topAnswer.probability)}
                      </Col>
                    </Row>
                  </Fragment>
                ) : (
                  <Empty description="No answers" image={Empty.PRESENTED_IMAGE_SIMPLE} />
                )
              }

              {
                !!otherAnswers.length && (
                  <Row>
                    <Col>
                      <div className={styles.otherAnswersTitle}>Other answers</div>
                    </Col>
                  </Row>
                )
              }

              {
                otherAnswers.map((item, i) => {
                  const answerParts = item.context.split(item.answer);
                  const itemMeta = item.meta || {};
                  return (
                    <Row gutter={[24, 40]} key={i}>
                      <Col span={19}>
                        <div className={styles.answerTitle}>{item.question}</div>
                        <div className={styles.answerText}>
                          {
                            item.answer ? (
                              <Fragment>
                                {answerParts[0]}
                                <span>{item.answer}</span>
                                {answerParts[1]}
                              </Fragment>
                            ) : item.context || '-'
                          }
                        </div>
                        <div className={styles.answerMeta}>
                          <div><span>Updated:</span> {itemMeta.last_update || '–'}</div>
                          <div>
                            <span>Source:</span> {itemMeta.source || '–'}
                            {
                              itemMeta.link && (
                                <a href={itemMeta.link} target="_blank" rel="noopener noreferrer" className={styles.answerDocLink}>
                                  <Icon type="link" />
                                </a>
                              )
                            }
                          </div>
                          <div>
                            <span>Feedback:</span>
                            { this.renderFeedbackLink(itemMeta, true) }
                            { this.renderFeedbackLink(itemMeta, false) }
                          </div>

                        </div>
                      </Col>
                      <Col span={5}>
                        {this.renderTag(item.probability)}
                      </Col>
                    </Row>
                  );
                })
              }
            </div>
          )
        }
      </div>
    );
  }

  componentWillUnmount() {
    // reset question filter field
    this.props.globalSearchActions.reset();
    this.props.answersActions.reset();
  }
}

export default connect(
  state => ({
    globalSearch: state.globalSearch,
    answers: state.activeAnswers
  }),
  dispatch => ({
    globalSearchActions: bindActionCreators(globalSearchActions, dispatch),
    answersActions: bindActionCreators(answersActions, dispatch)
  })
)(Answers);
