import type { Logger, LogLevel } from '../contracts/logger'

export class SilentLogger implements Logger {
  private level: LogLevel = 'debug'

  debug(_message: string, _meta?: Record<string, unknown>): void {}
  info(_message: string, _meta?: Record<string, unknown>): void {}
  warn(_message: string, _meta?: Record<string, unknown>): void {}
  error(_message: string, _meta?: Record<string, unknown>): void {}

  setLevel(level: LogLevel): void {
    this.level = level
  }

  getLevel(): LogLevel {
    return this.level
  }
}
