import type { Logger, LogLevel } from '../contracts/logger'

const LEVEL_PRIORITY: Record<LogLevel, number> = {
  debug: 0,
  info: 1,
  warn: 2,
  error: 3,
}

const PREFIX: Record<LogLevel, string> = {
  debug: '[SDK:DEBUG]',
  info: '[SDK:INFO]',
  warn: '[SDK:WARN]',
  error: '[SDK:ERROR]',
}

export class ConsoleLogger implements Logger {
  private level: LogLevel = 'info'

  constructor(level?: LogLevel) {
    if (level) this.level = level
  }

  debug(message: string, meta?: Record<string, unknown>): void {
    this.log('debug', message, meta)
  }

  info(message: string, meta?: Record<string, unknown>): void {
    this.log('info', message, meta)
  }

  warn(message: string, meta?: Record<string, unknown>): void {
    this.log('warn', message, meta)
  }

  error(message: string, meta?: Record<string, unknown>): void {
    this.log('error', message, meta)
  }

  setLevel(level: LogLevel): void {
    this.level = level
  }

  getLevel(): LogLevel {
    return this.level
  }

  private log(level: LogLevel, message: string, meta?: Record<string, unknown>): void {
    if (LEVEL_PRIORITY[level] < LEVEL_PRIORITY[this.level]) return

    const prefix = PREFIX[level]
    const timestamp = new Date().toISOString()

    if (meta && Object.keys(meta).length > 0) {
      if (level === 'error') {
        console.error(`${timestamp} ${prefix} ${message}`, meta)
      } else if (level === 'warn') {
        console.warn(`${timestamp} ${prefix} ${message}`, meta)
      } else {
        console.log(`${timestamp} ${prefix} ${message}`, meta)
      }
    } else {
      if (level === 'error') {
        console.error(`${timestamp} ${prefix} ${message}`)
      } else if (level === 'warn') {
        console.warn(`${timestamp} ${prefix} ${message}`)
      } else {
        console.log(`${timestamp} ${prefix} ${message}`)
      }
    }
  }
}
