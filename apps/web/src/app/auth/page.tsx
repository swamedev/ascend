'use client'

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { LogIn } from 'lucide-react'
import { Card, CardContent } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Button } from '@/components/ui/button'
import { useAuthStore } from '@/store/auth-store'
import { api } from '@/lib/api'

export default function AuthPage() {
  const router = useRouter()
  const { isAuthenticated, setAuth } = useAuthStore()
  const [username, setUsername] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    if (isAuthenticated) {
      router.replace('/dashboard')
    }
  }, [isAuthenticated, router])

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    if (!username.trim()) return
    setLoading(true)
    setError(null)
    try {
      const { builder, token } = await api.login(username.trim())
      setAuth(builder.id, token, username.trim())
      router.replace('/dashboard')
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Something went wrong')
    } finally {
      setLoading(false)
    }
  }

  if (isAuthenticated) return null

  return (
    <main className="flex min-h-screen items-center justify-center bg-background p-4">
      <Card variant="elevated" className="w-full max-w-sm">
        <CardContent className="flex flex-col items-center gap-6 pt-8 pb-8">
          <div className="text-center space-y-1">
            <h1 className="text-2xl font-bold text-primary">ASCEND</h1>
            <p className="text-sm text-muted-foreground">
              Competency Development Framework
            </p>
          </div>

          <form onSubmit={handleSubmit} className="w-full space-y-4">
            <Input
              id="username"
              label="Username"
              placeholder="Enter your username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              disabled={loading}
              autoFocus
              icon={<LogIn className="h-4 w-4" />}
              iconPosition="left"
            />

            {error && (
              <p className="text-xs text-[var(--ascend-danger)]" role="alert">
                {error}
              </p>
            )}

            <Button
              type="submit"
              className="w-full"
              loading={loading}
              disabled={!username.trim()}
            >
              Start Your Journey
            </Button>
          </form>
        </CardContent>
      </Card>
    </main>
  )
}
