import { ref, Ref } from 'vue'

export type ValidationRule = {
  required?: boolean
  message: string
}

export type ValidationSchema<T> = {
  [K in keyof Partial<T>]: ValidationRule
}

export function useFormValidation<T extends Record<string, any>>() {
  const errors: Ref<Partial<Record<keyof T, string>>> = ref({})

  function validate(data: T, schema: ValidationSchema<T>): boolean {
    errors.value = {}

    for (const [field, rule] of Object.entries(schema) as [keyof T, ValidationRule][]) {
      if (rule.required) {
        const value = data[field]
        if (value === null || value === undefined || (typeof value === 'string' && !value.trim())) {
          errors.value[field] = rule.message
        }
      }
    }

    return Object.keys(errors.value).length === 0
  }

  function clearErrors() {
    errors.value = {}
  }

  function clearError(field: keyof T) {
    delete errors.value[field]
  }

  return {
    errors,
    validate,
    clearErrors,
    clearError
  }
}
