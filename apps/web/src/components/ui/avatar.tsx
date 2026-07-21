'use client'

import { useState } from 'react'
import { cn } from '@/lib/utils'
import Image from 'next/image'

type AvatarSize = 'sm' | 'md' | 'lg' | 'xl'

interface AvatarProps {
  src?: string
  alt?: string
  initials?: string
  size?: AvatarSize
  className?: string
}

const sizeMap: Record<AvatarSize, string> = {
  sm: 'h-8 w-8 text-xs',
  md: 'h-10 w-10 text-sm',
  lg: 'h-12 w-12 text-base',
  xl: 'h-16 w-16 text-lg',
}

const imgSizeMap: Record<AvatarSize, number> = {
  sm: 32,
  md: 40,
  lg: 56,
  xl: 72,
}

export function Avatar({ src, alt, initials, size = 'md', className }: AvatarProps) {
  const [imgError, setImgError] = useState(false)

  if (src && !imgError) {
    return (
      <Image
        src={src}
        alt={alt ?? ''}
        width={imgSizeMap[size]}
        height={imgSizeMap[size]}
        className={cn('rounded-full object-cover', sizeMap[size], className)}
        onError={() => setImgError(true)}
      />
    )
  }

  return (
    <div
      className={cn(
        'flex items-center justify-center rounded-full bg-accent font-medium text-accent-foreground',
        sizeMap[size],
        className
      )}
      aria-label={alt ?? initials ?? 'Avatar'}
      role="img"
    >
      {initials?.slice(0, 2).toUpperCase() ?? '?'}
    </div>
  )
}
