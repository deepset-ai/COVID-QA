import React, { PureComponent } from 'react';
import PropTypes from 'prop-types';
import { Row, Col, Form, AutoComplete } from 'antd';
import styles from './styles.module.scss';
import logoHackathon from 'assets/images/logo-wirs-vs-virus-projekt-black-font.svg';
import { withTranslation } from 'react-i18next';

class SearchForm extends PureComponent {
  static propTypes = {
    form: PropTypes.object,
    value: PropTypes.string,
    options: PropTypes.array,
    filters: PropTypes.object,
    onSearch: PropTypes.func,
    onSubmit: PropTypes.func,
  }

  handleSearch = (value) => {
    this.props.onSearch(value);
  }

  handleSelect = (value, option) => {
    this.props.onSubmit(option.props.children);
  }

  onKeyDown = ({ keyCode }) => {
    const { form, onSubmit } = this.props;

    // if enter pressed and no options
    if (keyCode === 13) {
      form.validateFields((err, values) => {
        if (err) {
          return;
        }
        for (let option of this.props.options){
          if (option.id === parseInt(values.question)){
            onSubmit(option.question);
            return;
          }
        }
        onSubmit(values.question);

      });
    }
  }

  render() {
    const { form, options, filters, t } = this.props;
    const { getFieldDecorator } = form;
    const suggestions = options || [];
    const displayLanguages = {'de' : t('languages.de'), 'en': t('languages.en')};
    const language = filters && filters.language;

    return (
      <Form className={styles.form}>
        <Row>
          <Col span={24}>
            <Form.Item>
              {getFieldDecorator('question', {
                rules: [{ required: true, message: t('inputs.question.placeholder') }],
              })(
                <AutoComplete
                  className={styles.autocomplete}
                  autoFocus
                  size="large"
                  defaultActiveFirstOption={false}
                  placeholder={t('inputs.question.placeholder')}
                  filterOption={(value, option) =>
                    option.props.children.toLowerCase().startsWith(value.toLowerCase())
                    // option.props.children.toLowerCase().indexOf(value.toLowerCase()) !== -1 // to show all options with substring
                  }
                  onSearch={this.handleSearch}
                  onSelect={this.handleSelect}
                  onInputKeyDown={this.onKeyDown}
                >
                  {
                    suggestions.map(item =>
                      <AutoComplete.Option key={item.id}>{item.question}</AutoComplete.Option>
                    )
                  }
                </AutoComplete>
              )}
            </Form.Item>
          </Col>
        </Row>
    <Row gutter={32}>
        <Col>
        { language ?
              <p className={styles.detectedLanguage}>Fragesprache {displayLanguages[language]}</p>
            :
            <div className={styles.poweredBy}>
                  <p className="made-by">Made with <span className="heart">❤</span> and <a href="https://github.com/deepset-ai/haystack">open source</a></p>
            </div>
        }
    </Col></Row>
    <Row> <Col>
            <div className={styles.projectLogo}>
              <a href="https://wirvsvirushackathon.org/" target="_blank" rel="noopener noreferrer">
                <img src={logoHackathon} alt="WirVsVirus Hackathon" />
              </a>
            </div>

          </Col>
        </Row>

      </Form>
    );
  }
}

export const WrappedSearchForm = Form.create()(withTranslation()(SearchForm));
