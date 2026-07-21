import type { Logger } from '../contracts/logger'
import type { EventBus } from '../contracts/event-bus'
import { AscendError } from '../errors/ascend.error'
import { SDKEvents } from '../events/sdk-events'
import type { StateChangedPayload } from '../events/sdk-events'

export const SDKStates = [
  'CREATED',
  'INITIALIZING',
  'READY',
  'DEGRADED',
  'OFFLINE',
  'STOPPING',
  'STOPPED',
] as const

export type SDKState = (typeof SDKStates)[number]

const ALLOWED_TRANSITIONS: Record<SDKState, SDKState[]> = {
  CREATED: ['INITIALIZING'],
  INITIALIZING: ['READY', 'DEGRADED', 'STOPPING'],
  READY: ['DEGRADED', 'OFFLINE', 'STOPPING'],
  DEGRADED: ['READY', 'OFFLINE', 'STOPPING'],
  OFFLINE: ['READY', 'DEGRADED', 'STOPPING'],
  STOPPING: ['STOPPED'],
  STOPPED: [],
}

export interface StateChangeEvent {
  from: SDKState
  to: SDKState
  timestamp: number
  reason?: string
}

export type StateChangeHandler = (event: StateChangeEvent) => void

export class Lifecycle {
  private _state: SDKState = 'CREATED'
  private _previousState: SDKState | null = null
  private handlers = new Set<StateChangeHandler>()
  private logger: Logger
  private events: EventBus
  private _startedAt: number | null = null

  constructor(logger: Logger, events: EventBus) {
    this.logger = logger
    this.events = events
  }

  get state(): SDKState {
    return this._state
  }

  get previousState(): SDKState | null {
    return this._previousState
  }

  get startedAt(): number | null {
    return this._startedAt
  }

  canTransition(to: SDKState): boolean {
    const allowed = ALLOWED_TRANSITIONS[this._state]
    return allowed ? allowed.includes(to) : false
  }

  async transition(to: SDKState, reason?: string): Promise<void> {
    if (this._state === to) return

    if (!this.canTransition(to)) {
      throw new AscendError(
        `Invalid state transition: ${this._state} → ${to}`,
        { code: 'INVALID_STATE_TRANSITION', statusCode: 500, details: { from: this._state, to } },
      )
    }

    const from = this._state
    this._previousState = this._state
    this._state = to

    const event: StateChangeEvent = {
      from,
      to,
      timestamp: Date.now(),
      reason,
    }

    if (to === 'READY' && this._startedAt === null) {
      this._startedAt = Date.now()
    }

    this.logger.info(`State transition: ${from} → ${to}`, { reason })

    const payload: StateChangedPayload = {
      from,
      to,
      reason,
    }
    this.events.publish(SDKEvents.StateChanged, payload)

    for (const handler of this.handlers) {
      handler(event)
    }
  }

  onStateChange(handler: StateChangeHandler): () => void {
    this.handlers.add(handler)
    return () => {
      this.handlers.delete(handler)
    }
  }

  reset(): void {
    this._state = 'CREATED'
    this._previousState = null
    this._startedAt = null
    this.handlers.clear()
  }
}
