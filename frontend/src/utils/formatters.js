const TIMEZONE = 'America/Lima'

export const formatFecha = (fechaStr) => {
  if (!fechaStr) return '-'
  const d = new Date(fechaStr)
  const dia = String(d.getUTCDate()).padStart(2, '0')
  const mes = String(d.getUTCMonth() + 1).padStart(2, '0')
  return `${dia}/${mes}/${d.getUTCFullYear()}`
}

export const formatFechaHora = (fechaStr) => {
  if (!fechaStr) return '-'
  const d = new Date(new Date(fechaStr).toLocaleString('en-US', { timeZone: TIMEZONE }))
  const dia  = String(d.getDate()).padStart(2, '0')
  const mes  = String(d.getMonth() + 1).padStart(2, '0')
  const hora = String(d.getHours()).padStart(2, '0')
  const min  = String(d.getMinutes()).padStart(2, '0')
  return `${dia}/${mes}/${d.getFullYear()} ${hora}:${min}`
}

/** API time ("H:MM", "HH:MM" or "HH:MM:SS") → "HH:MM". Empty string if missing. */
export const toHoraMinutos = (valor) => {
  if (valor == null || valor === '') return ''
  const match = String(valor).match(/^(\d{1,2}):(\d{2})/)
  if (!match) return ''
  return `${match[1].padStart(2, '0')}:${match[2]}`
}

export const formatSize = (bytes) => {
  if (!bytes) return ''
  if (bytes >= 1024 * 1024) return `${(bytes / (1024 * 1024)).toFixed(1)} MB`
  return `${(bytes / 1024).toFixed(1)} KB`
}
