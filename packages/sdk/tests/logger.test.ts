import { describe, it, expect, vi } from 'vitest'
import { ConsoleLogger } from '../src/logger/console-logger'
import { SilentLogger } from '../src/logger/silent-logger'

describe('ConsoleLogger', () => {
  it('logs at default level', () => {
    const logger = new ConsoleLogger()
    expect(logger.getLevel()).toBe('info')
  })

  it('sets and gets level', () => {
    const logger = new ConsoleLogger()
    logger.setLevel('debug')
    expect(logger.getLevel()).toBe('debug')
  })

  it('silently filters debug below info', () => {
    const spy = vi.spyOn(console, 'log').mockImplementation(() => {})
    const logger = new ConsoleLogger('info')
    logger.debug('should not appear')
    expect(spy).not.toHaveBeenCalled()
    spy.mockRestore()
  })

  it('logs info at info level', () => {
    const spy = vi.spyOn(console, 'log').mockImplementation(() => {})
    const logger = new ConsoleLogger('info')
    logger.info('hello')
    expect(spy).toHaveBeenCalled()
    spy.mockRestore()
  })

  it('logs error with meta', () => {
    const spy = vi.spyOn(console, 'error').mockImplementation(() => {})
    const logger = new ConsoleLogger('error')
    logger.error('fail', { code: 500 })
    expect(spy).toHaveBeenCalled()
    spy.mockRestore()
  })

  it('logs warn with meta', () => {
    const spy = vi.spyOn(console, 'warn').mockImplementation(() => {})
    const logger = new ConsoleLogger('warn')
    logger.warn('caution', { reason: 'test' })
    expect(spy).toHaveBeenCalled()
    spy.mockRestore()
  })

  it('logs debug with meta', () => {
    const spy = vi.spyOn(console, 'log').mockImplementation(() => {})
    const logger = new ConsoleLogger('debug')
    logger.debug('trace', { detail: 'x' })
    expect(spy).toHaveBeenCalled()
    spy.mockRestore()
  })

  it('logs info without meta', () => {
    const spy = vi.spyOn(console, 'log').mockImplementation(() => {})
    const logger = new ConsoleLogger('info')
    logger.info('just message')
    expect(spy).toHaveBeenCalled()
    spy.mockRestore()
  })

  it('logs error without meta', () => {
    const spy = vi.spyOn(console, 'error').mockImplementation(() => {})
    const logger = new ConsoleLogger('error')
    logger.error('fail without meta')
    expect(spy).toHaveBeenCalled()
    spy.mockRestore()
  })

  it('logs warn without meta', () => {
    const spy = vi.spyOn(console, 'warn').mockImplementation(() => {})
    const logger = new ConsoleLogger('warn')
    logger.warn('warn without meta')
    expect(spy).toHaveBeenCalled()
    spy.mockRestore()
  })
})

describe('SilentLogger', () => {
  it('does not output anything', () => {
    const spy = vi.spyOn(console, 'log').mockImplementation(() => {})
    const logger = new SilentLogger()
    logger.info('silent')
    logger.warn('silent')
    logger.error('silent')
    logger.debug('silent')
    expect(spy).not.toHaveBeenCalled()
    spy.mockRestore()
  })

  it('sets and gets level', () => {
    const logger = new SilentLogger()
    logger.setLevel('error')
    expect(logger.getLevel()).toBe('error')
  })
})
