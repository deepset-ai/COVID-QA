import React, { PureComponent } from 'react';
import PropTypes from 'prop-types';
import { Row, Col, Form, AutoComplete } from 'antd';
import styles from './styles.module.scss';
import logoHackathon from 'assets/images/logo-wirs-vs-virus-projekt-black-font.svg';

class SearchForm extends PureComponent {
  static propTypes = {
    form: PropTypes.object,
    value: PropTypes.string,
    options: PropTypes.array,
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
        if (!err) {
          onSubmit(values.question);
        }
      });
    }
  }

  render() {
    const { form, options } = this.props;
    const { getFieldDecorator } = form;
    const suggestions = options.suggestions || [];
    console.log({suggestions, options})
    const displayLanguages = {'de' : 'Deutsch', 'en': 'English'};
    return (
      <Form className={styles.form}>
        <Row>
          <Col span={24}>
            <Form.Item>
              {getFieldDecorator('question', {
                rules: [{ required: true, message: 'Stellen Sie eine Frage zu Covid-19 (Corona-Virus)' }],
              })(
                <AutoComplete
                  className={styles.autocomplete}
                  autoFocus
                  size="large"
                  defaultActiveFirstOption={false}
                  placeholder="Stellen Sie eine Frage zu Covid-19 (Corona-Virus)"
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
        { options.language ?
              <p className={styles.detectedLanguage}>Fragesprache {displayLanguages[options.language]}</p>
            :
            <div className={styles.poweredBy}>
                  <p className="made-by">Made with <span className="heart">❤</span> and <a href="https://github.com/deepset-ai/haystack">open source</a></p>
            </div>
        }
    </Col></Row>
    <Row> <Col>
            <div className={styles.projectLogo}>
              <a href="https://wirvsvirushackathon.org/" target="_blank" rel="noopener noreferrer">
                <img src={logoHackathon} alt="Logo WirVsVirus Hackathon" />
              </a>
            </div>

          </Col>
        </Row>

      </Form>
    );
  }
}

export const WrappedSearchForm = Form.create()(SearchForm);
