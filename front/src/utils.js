import React from 'react'

// -------------------------------------------------------------------------------------------------- //
// Misc
// -------------------------------------------------------------------------------------------------- //

function toCamelCase(string) {
  return string.replace(/_([a-z])/g, (_, n) => n.toUpperCase())
}

function toSnakeCase(string) {
  return string.replace(/(.)([A-Z][a-z])/g, "$1_$2").replace(/([a-z0-9])([A-Z])/g, "$1_$2").toLowerCase()
}

function withObjectKeys(object, formatter) {
  if (typeof object === typeof 1 || typeof object === typeof " " || object === undefined || object === null) return object
  if (object instanceof Array) return object.map((element) => withObjectKeys(element, formatter))
  return Object.keys(object).reduce((formatted, key) => {
    const value = object[key]
    formatted[formatter(key)] = withObjectKeys(value, formatter)
    return formatted
  }, {})
}

export function toSnakeCaseObject(object) {
  return withObjectKeys(object, toSnakeCase)
}

export function toCamelCaseObject(object) {
  return withObjectKeys(object, toCamelCase)
}

// -------------------------------------------------------------------------------------------------- //
// Formik, Yup
// -------------------------------------------------------------------------------------------------- //
export const FieldStrap = ({field, form: { touched, errors}, validFeedback, className, ...props}) => (
  <div>
      <input
          className={`
              ${className}
              ${touched[field.name] && errors[field.name] ? "is-invalid": ""}
              ${touched[field.name] && !errors[field.name] ? "is-valid": ""}
          `}
          {...props}
          {...field}
      />
      {touched[field.name] && errors[field.name] && <small className="invalid-feedback">{errors[field.name]}</small>}
      {touched[field.name] && !errors[field.name] && validFeedback && <small className="valid-feedback">{validFeedback}</small>}
  </div>
)


function getErrorsFromValidationError(validationError) {
const FIRST_ERROR = 0
return validationError.inner.reduce((errors, error) => {
  return {
    ...errors,
    [error.path]: error.errors[FIRST_ERROR],
  }
}, {})
}

export const validate = (getValidationSchema) => {
return (values) => {
  const schema = getValidationSchema(values)
  try {
    schema.validateSync(values, {abortEarly: false})
    return {}
  } catch(error) {
    return getErrorsFromValidationError(error)
  }
}
}
