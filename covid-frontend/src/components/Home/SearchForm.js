import React, { PureComponent } from 'react';
import PropTypes from 'prop-types';
import { Row, Col, Form, AutoComplete } from 'antd';
import styles from './styles.module.scss';

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

    return (
      <Form className={styles.form}>
        <Row>
          <Col span={24}>
            <Form.Item>
              {getFieldDecorator('question', {
                rules: [{ required: true, message: 'Please insert your question!' }],
              })(
                <AutoComplete
                  className={styles.autocomplete}
                  autoFocus
                  size="large"
                  defaultActiveFirstOption={false}
                  placeholder="Ask any question about Corona..."
                  filterOption={(value, option) =>
                    option.props.children.toLowerCase().startsWith(value.toLowerCase())
                    // option.props.children.toLowerCase().indexOf(value.toLowerCase()) !== -1 // to show all options with substring
                  }
                  onSearch={this.handleSearch}
                  onSelect={this.handleSelect}
                  onInputKeyDown={this.onKeyDown}
                >
                  {
                    options.map(item =>
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
            <div className={styles.poweredBy}>
              Made with <span>❤</span> and <a href="https://github.com/deepset-ai/haystack">open source</a>
            </div>
          </Col>
        </Row>

      </Form>
    );
  }
}

export const WrappedSearchForm = Form.create()(SearchForm);
