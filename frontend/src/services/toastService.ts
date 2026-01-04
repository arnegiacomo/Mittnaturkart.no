import type { ToastServiceMethods } from 'primevue/toastservice'
import { t } from '../i18n'

let toastInstance: ToastServiceMethods | null = null

export function initToast(toast: ToastServiceMethods) {
  toastInstance = toast
}

export function showError(detail: string) {
  toastInstance?.add({
    severity: 'error',
    summary: t('toast.error'),
    detail,
    life: 5000
  })
}

export function showSuccess(detail: string) {
  toastInstance?.add({
    severity: 'success',
    summary: t('toast.success'),
    detail,
    life: 3000
  })
}
