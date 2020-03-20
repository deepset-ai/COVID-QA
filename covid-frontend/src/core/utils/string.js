
export const prefix = (value) => (string) => `${value}${string}`;

// result example - 12345.67 --> "12,345.67"
export const formatNumber = (value = 0, precision = 2) =>
  value.toFixed(precision).replace(/\d(?=(\d{3})+\.)/g, '$&,');
