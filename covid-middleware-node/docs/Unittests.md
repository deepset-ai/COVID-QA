

## Assert methods;
assert(value, [message])
assert.ok(value, [message])
assert.equal(actual, expected, [message])
assert.notEqual(actual, expected, [message])
assert.strictEqual(actual, expected, [message])
assert.notStrictEqual(actual, expected, [message])
assert.deepEqual(actual, expected, [message])
assert.notDeepEqual(actual, expected, [message])
assert.deepStrictEqual(actual, expected, [message])
assert.notDeepStrictEqual(actual, expected, [message])
power-assert is fully compatible with assert. So functions below are also available though they are not enhanced (does not produce descriptive message).

assert.fail(actual, expected, message, operator)
assert.throws(block, [error], [message])
assert.doesNotThrow(block, [message])
assert.ifError(value)
