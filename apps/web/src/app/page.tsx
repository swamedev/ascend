'use client'

import Link from 'next/link'
import { useRouter } from 'next/navigation'
import { useState } from 'react'
import { Button } from '@/components/ui/button'
import { useDemoStore } from '@/store'
import { api } from '@/lib/api'

export default function HomePage() {
  const router = useRouter()
  const { setDemoData } = useDemoStore()
  const [starting, setStarting] = useState(false)

  async function handleStartDemo() {
    setStarting(true)
    try {
      const data = await api.startDemo()
      setDemoData({ id: data.demoId, builderId: data.builderId, journey: data.journey })
      router.push('/demo/journey')
    } catch {
      router.push('/demo/journey')
    }
  }

  return (
    <main className="flex min-h-screen flex-col items-center justify-center bg-background p-8 text-center">
      <h1 className="text-4xl font-bold tracking-tight">ASCEND</h1>
      <p className="mt-4 max-w-md text-lg text-muted-foreground">
        Competency Development Framework
      </p>
      <p className="mt-2 text-sm text-muted-foreground">
        Aprenda fazendo. Comprove com evidências.
      </p>
      <div className="mt-8 flex gap-4">
        <Link href="/auth">
          <Button variant="primary" size="lg">
            Começar Agora
          </Button>
        </Link>
        <Button
          variant="secondary"
          size="lg"
          loading={starting}
          disabled={starting}
          onClick={handleStartDemo}
        >
          Experimentar Demo
        </Button>
      </div>
    </main>
  )
}
