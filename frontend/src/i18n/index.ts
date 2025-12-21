import nbNO from '../locales/nb-NO.json'

export const locale = 'nb-NO'

export const messages = {
  'nb-NO': nbNO
}

export function t(key: string, params?: Record<string, any>): string {
  const keys = key.split('.')
  let value: any = messages[locale]

  for (const k of keys) {
    value = value?.[k]
    if (!value) return key
  }

  if (typeof value === 'string' && params) {
    return value.replace(/\{(\w+)\}/g, (_, key) => params[key] || '')
  }

  return value || key
}
