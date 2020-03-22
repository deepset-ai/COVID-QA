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
import {CheckCircleOutlined} from '@ant-design/icons';
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

  renderTag = (probability) => {
    const value = probability * 100;
    const theme = value >= 80 ? Tag.themes.GREEN : value >= 30 ? Tag.themes.ORANGE : Tag.themes.RED;
    const roundedValue = parseFloat(value).toFixed(2);
    return (
      <Tag
        text={`Relevanz: ${roundedValue}%`}
        theme={theme}
        className={styles.tag + " result-confidence-box"}
      />
    );
  }

  formattedDateDE = (dateString) => {
    // input 2020/03/17, output 17.03.2020 (German date format)
    const splitStringArray = dateString.split(/[.\-/]/);
    return `${splitStringArray[2]}.${splitStringArray[1]}.${splitStringArray[0]}`;

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
            <InputContainer label="Ihre Frage" fluid>
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
              <div>Please Wait – Bitte warten...</div>
            </div>
          ) : (
            <div className={styles.list + ' all-answers-wrapper'}>
              {
                topAnswer.hasOwnProperty('probability') ? (
                  <Fragment>
                    <Row gutter={[24, 40]} className="top-answer-wrapper">
                      <Col span={19}>
                        <div className={styles.topAnswerTitle + ' top-answer-box'}>
                          Beste Antwort
                        </div> 
                        <div className={styles.answerTitle + ' headline-faq-match'}>
                          {topAnswer.question}
                        </div>
                        <div className='headline-faq-match-confidence'>
                          <CheckCircleOutlined style={{ color: 'white' }}/>
                          {this.renderTag(topAnswer.probability)}
                        </div>
                        <div className={styles.answerText + ' answer-text'}>
                          {
                            topAnswer.answer ? (
                              <Fragment>
                                {topAnswerParts[0]}
                                  {topAnswer.answer}
                                {topAnswerParts[1]}
                              </Fragment>
                            ) : topAnswer.context || '-'
                          }
                        </div>
                      </Col>
                    </Row>

                    <Row gutter={[24, 40]} className="top-answer-meta-wrapper">
                      <Col span={19}>
                        <div className={styles.answerMeta + ' answer-meta-info top-answer'}>
                          <div><span>Stand:</span> {this.formattedDateDE(topAnswerMeta.last_update) || '–'}</div>
                          <div>
                            <span>Quelle:</span> {topAnswerMeta.source || '–'}
                            {
                              topAnswerMeta.link && (
                                <a href={topAnswerMeta.link} target="_blank" rel="noopener noreferrer" className={styles.answerDocLink}>
                                  <Icon type="link" />
                                </a>
                              )
                            }
                          </div>
                          <div className="feedback-buttons">
                            <span>Feedback:</span>
                            <a href='#upvote' rel="noopener noreferrer" className={styles.answerDocLink}
                              onClick={this.onFeedbackPositive.bind(this, topAnswerMeta.document_id)}>
                              <Icon type="like" />
                            </a>
                            { !showUserFeedbackPanel && 
                              <a href='#downvote' rel="noopener noreferrer" className={styles.answerDocLink}
                                onClick={this.onFeedbackNegative.bind(this, topAnswerMeta.document_id)}>
                                <Icon type="dislike" />
                              </a>}
                          </div>
                        </div>
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
                      <div className={styles.otherAnswersTitle}>Weitere Antworten</div>
                    </Col>
                  </Row>
                )
              }

              {
                otherAnswers.map((item, i) => {
                  const answerParts = item.context.split(item.answer);
                  const itemMeta = item.meta || {};
                  return (
                    <Row gutter={[24, 40]} key={i} className={`other-answer-row row_${i}`}>
                      <Col span={19}>
                        <div className={styles.answerTitle + ' headline-faq-match other-answer-index-' + i}>{item.question}</div>
                        <div className="headline-faq-match-confidence">
                          <CheckCircleOutlined style={{ color: 'black' }}/>
                          {this.renderTag(item.probability)}
                        </div>
                        <div className={styles.answerText + ' answer-text'}>
                          {
                            item.answer ? (
                              <Fragment>
                                {answerParts[0]}
                                  {item.answer}
                                {answerParts[1]}
                              </Fragment>
                            ) : item.context || '-'
                          }
                        </div>
                        <div className={styles.answerMeta + ' answer-meta-info'}>
                          <div><span>Stand:</span> {this.formattedDateDE(topAnswerMeta.last_update) || '–'}</div>
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
                          <div className="feedback-buttons">
                            <span>Feedback:</span>
                          
                            <a href='#upvote' target="_blank" rel="noopener noreferrer" className={styles.answerDocLink}
                              onClick={this.onFeedbackPositive.bind(this, itemMeta.document_id)}>
                              <Icon type="like" />
                            </a>
                            { !showUserFeedbackPanel && 
                              <a href='#downvote' rel="noopener noreferrer" className={styles.answerDocLink}
                                onClick={this.onFeedbackNegative.bind(this, itemMeta.document_id)}>
                                <Icon type="dislike" />
                              </a>}
                          </div>

                        </div>
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
