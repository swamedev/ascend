'use client'

import { useState } from 'react'
import {
  Button,
  Badge,
  Avatar,
  Divider,
  Spinner,
  Skeleton,
  Label,
  Input,
  Textarea,
  Tooltip,
  Card,
  CardHeader,
  CardContent,
  CardFooter,
  Modal,
  Drawer,
  Alert,
  EmptyState,
  LoadingState,
  ErrorState,
  SuccessState,
  IconButton,
} from '@/components/ui'
import {
  Sidebar,
  TopBar,
  TopBarAction,
  Breadcrumb,
  PageContainer,
  Panel,
  PanelHeader,
  BottomNavigation,
} from '@/components/layout'
import {
  AscensionRing,
  XPBar,
  LevelBadge,
  CompetencyBadge,
  MissionStatus,
  JourneyCard,
  ProgressIndicator,
  EvidenceBadge,
  AchievementBadge,
} from '@/components/shared'
import {
  Bell,
  Settings,
  Search,
  Home,
  User,
  Star,
  Trophy,
  Zap,
  Shield,
  BookOpen,
  ChevronLeft,
} from 'lucide-react'
import { useLayoutStore } from '@/store/layout-store'

const section =
  'rounded-lg border p-6 space-y-4'
const h2 =
  'text-lg font-semibold'
const h3 =
  'text-sm font-medium text-muted-foreground'
const row =
  'flex flex-wrap items-center gap-3'

const navItems = [
  { id: 'home', icon: Home, label: 'Home', href: '/' },
  { id: 'journeys', icon: BookOpen, label: 'Journeys', href: '/journeys', badge: 3 },
  { id: 'profile', icon: User, label: 'Profile', href: '/profile' },
]

const navGroups = [
  { id: 'main', label: 'Main', items: navItems },
  { id: 'admin', label: 'Admin', items: [
    { id: 'settings', icon: Settings, label: 'Settings', href: '/settings' },
  ]},
]

export default function ComponentGalleryPage() {
  const [modalOpen, setModalOpen] = useState(false)
  const [drawerOpen, setDrawerOpen] = useState(false)
  const setBreadcrumbs = useLayoutStore((s) => s.setBreadcrumbs)

  useState(() => {
    setBreadcrumbs([
      { label: 'Dev' },
      { label: 'Component Gallery' },
    ])
  })

  return (
    <PageContainer maxWidth="xl" padding="lg">
      <div className="space-y-12">
        <div>
          <h1 className="text-2xl font-bold">Component Gallery</h1>
          <p className="text-muted-foreground mt-1">
            Every component, every variant. For visual review only.
          </p>
        </div>

        {/* ======== TIER 1 — PRIMITIVES ======== */}
        <section className={section}>
          <h2 className={h2}>Tier 1 — Primitives</h2>

          {/* Button */}
          <div>
            <h3 className={h3}>Button</h3>
            <div className={row}>
              <Button variant="primary">Primary</Button>
              <Button variant="secondary">Secondary</Button>
              <Button variant="ghost">Ghost</Button>
              <Button variant="danger">Danger</Button>
              <Button loading>Loading</Button>
              <Button disabled>Disabled</Button>
            </div>
            <div className={row}>
              <Button size="sm">Small</Button>
              <Button size="md">Medium</Button>
              <Button size="lg">Large</Button>
            </div>
          </div>

          {/* IconButton */}
          <div>
            <h3 className={h3}>IconButton</h3>
            <div className={row}>
              <IconButton icon={<Bell />} label="Notifications" />
              <IconButton icon={<Settings />} label="Settings" />
              <IconButton icon={<Search />} label="Search" />
              <IconButton icon={<Bell />} label="Loading" loading />
            </div>
          </div>

          {/* Badge */}
          <div>
            <h3 className={h3}>Badge</h3>
            <div className={row}>
              <Badge variant="default">Default</Badge>
              <Badge variant="primary">Primary</Badge>
              <Badge variant="success">Success</Badge>
              <Badge variant="warning">Warning</Badge>
              <Badge variant="danger">Danger</Badge>
              <Badge variant="info">Info</Badge>
              <Badge variant="xp">+250 XP</Badge>
              <Badge dot variant="primary">Live</Badge>
              <Badge size="sm">Small</Badge>
            </div>
          </div>

          {/* Avatar */}
          <div>
            <h3 className={h3}>Avatar</h3>
            <div className={row}>
              <Avatar initials="JD" size="sm" />
              <Avatar initials="JD" size="md" />
              <Avatar initials="JD" size="lg" />
              <Avatar initials="JD" size="xl" />
              <Avatar src="https://i.pravatar.cc/80?img=3" alt="User" />
            </div>
          </div>

          {/* Divider */}
          <div>
            <h3 className={h3}>Divider</h3>
            <Divider />
            <Divider label="Section" />
            <div className="flex h-12 items-center gap-2">
              <span>Left</span>
              <Divider orientation="vertical" />
              <span>Right</span>
            </div>
          </div>

          {/* Spinner */}
          <div>
            <h3 className={h3}>Spinner</h3>
            <div className={row}>
              <Spinner size="sm" />
              <Spinner size="md" />
              <Spinner size="lg" />
            </div>
          </div>

          {/* Skeleton */}
          <div>
            <h3 className={h3}>Skeleton</h3>
            <div className="w-80 space-y-2">
              <Skeleton variant="circular" width={40} height={40} />
              <Skeleton variant="text" />
              <Skeleton variant="text" width="60%" />
              <Skeleton variant="rectangular" height={80} />
            </div>
          </div>

          {/* Label, Input, Textarea */}
          <div>
            <h3 className={h3}>Form Controls</h3>
            <div className="grid max-w-md gap-4">
              <Label required>Email</Label>
              <Input placeholder="Enter email..." />
              <Input icon={<Search />} placeholder="Search..." error="This field is required" />
              <Textarea label="Bio" placeholder="Tell us about yourself..." />
              <Textarea label="With error" error="Too short" />
            </div>
          </div>

          {/* Tooltip */}
          <div>
            <h3 className={h3}>Tooltip</h3>
            <div className={row}>
              <Tooltip content="Top tooltip" position="top">
                <Button size="sm">Hover top</Button>
              </Tooltip>
              <Tooltip content="Bottom tooltip" position="bottom">
                <Button size="sm">Hover bottom</Button>
              </Tooltip>
              <Tooltip content="Left tooltip" position="left">
                <Button size="sm">Hover left</Button>
              </Tooltip>
              <Tooltip content="Right tooltip" position="right">
                <Button size="sm">Hover right</Button>
              </Tooltip>
            </div>
          </div>

          {/* Card */}
          <div>
            <h3 className={h3}>Card</h3>
            <div className="grid grid-cols-3 gap-4">
              <Card variant="default">
                <CardHeader title="Default" description="No border, no shadow" />
                <CardContent>Content here</CardContent>
              </Card>
              <Card variant="bordered">
                <CardHeader title="Bordered" description="Has a border" />
                <CardContent>Content here</CardContent>
              </Card>
              <Card variant="elevated">
                <CardHeader title="Elevated" description="With shadow" action={<Button size="sm">Action</Button>} />
                <CardContent>Content here</CardContent>
                <CardFooter>
                  <Button size="sm">Save</Button>
                  <Button size="sm" variant="ghost">Cancel</Button>
                </CardFooter>
              </Card>
            </div>
          </div>

          {/* Modal */}
          <div>
            <h3 className={h3}>Modal</h3>
            <Button onClick={() => setModalOpen(true)}>Open Modal</Button>
            <Modal open={modalOpen} onClose={() => setModalOpen(false)} title="Example Modal" description="This is a modal dialog">
              <p className="text-sm text-muted-foreground">Modal content goes here. Press Escape or click X to close.</p>
              <div className="mt-4 flex justify-end gap-2">
                <Button variant="ghost" onClick={() => setModalOpen(false)}>Cancel</Button>
                <Button onClick={() => setModalOpen(false)}>Confirm</Button>
              </div>
            </Modal>
          </div>

          {/* Drawer */}
          <div>
            <h3 className={h3}>Drawer</h3>
            <div className={row}>
              <Button onClick={() => setDrawerOpen(true)}>Open Drawer</Button>
            </div>
            <Drawer open={drawerOpen} onClose={() => setDrawerOpen(false)} title="Example Drawer">
              <p className="text-sm text-muted-foreground">Drawer content goes here.</p>
            </Drawer>
          </div>
        </section>

        {/* ======== TIER 2 — LAYOUT ======== */}
        <section className={section}>
          <h2 className={h2}>Tier 2 — Layout</h2>

          {/* TopBar */}
          <div>
            <h3 className={h3}>TopBar + TopBarAction</h3>
            <div className="rounded-md border">
              <TopBar
                left={<Button size="sm" variant="ghost"><ChevronLeft /> Back</Button>}
                center={<Breadcrumb />}
                right={
                  <>
                    <TopBarAction icon={<Search />} label="Search" />
                    <TopBarAction icon={<Bell />} label="Notifications" badge={5} />
                    <TopBarAction icon={<Settings />} label="Settings" active />
                  </>
                }
              />
            </div>
          </div>

          {/* Breadcrumb */}
          <div>
            <h3 className={h3}>Breadcrumb</h3>
            <Breadcrumb />
          </div>

          {/* Sidebar (preview) */}
          <div>
            <h3 className={h3}>Sidebar + SidebarItem</h3>
            <div className="h-80 rounded-md border">
              <Sidebar
                header={<div className="font-bold px-2">ASCEND</div>}
                groups={navGroups}
                footer={<div className="text-xs text-muted-foreground px-2">v1.0</div>}
              />
            </div>
          </div>

          {/* PageContainer */}
          <div>
            <h3 className={h3}>PageContainer</h3>
            <p className="text-sm text-muted-foreground">(The page you&apos;re viewing uses it)</p>
          </div>

          {/* Panel */}
          <div>
            <h3 className={h3}>Panel + PanelHeader</h3>
            <div className="h-48 rounded-md border">
              <Panel header="Details Panel">
                <PanelHeader title="Section Title" description="Optional description" />
                <p className="text-sm text-muted-foreground">Panel body content</p>
              </Panel>
            </div>
          </div>

          {/* Workspace */}
          <div>
            <h3 className={h3}>Workspace</h3>
            <p className="text-sm text-muted-foreground">(Rendered inside AppShell)</p>
          </div>

          {/* BottomNavigation */}
          <div>
            <h3 className={h3}>BottomNavigation</h3>
            <div className="relative h-16 rounded-md border">
              <BottomNavigation items={navItems} className="!fixed !bottom-auto !relative border rounded-md" />
            </div>
          </div>
        </section>

        {/* ======== TIER 3 — ASCEND DOMAIN ======== */}
        <section className={section}>
          <h2 className={h2}>Tier 3 — ASCEND Domain</h2>

          {/* AscensionRing */}
          <div>
            <h3 className={h3}>AscensionRing</h3>
            <div className={row}>
              <AscensionRing level={5} progress={35} />
              <AscensionRing level={12} progress={72} size={100} />
              <AscensionRing level={1} progress={10} size={64} strokeWidth={4} />
            </div>
          </div>

          {/* XPBar */}
          <div>
            <h3 className={h3}>XPBar</h3>
            <div className="w-80 space-y-3">
              <XPBar current={750} max={1000} label="Level Progress" />
              <XPBar current={5000} max={5000} size="lg" />
              <XPBar current={125} max={500} size="sm" showValues={false} />
            </div>
          </div>

          {/* LevelBadge */}
          <div>
            <h3 className={h3}>LevelBadge</h3>
            <div className={row}>
              <LevelBadge level={1} size="sm" />
              <LevelBadge level={42} size="md" />
              <LevelBadge level={99} size="lg" />
            </div>
          </div>

          {/* CompetencyBadge */}
          <div>
            <h3 className={h3}>CompetencyBadge</h3>
            <div className={row}>
              <CompetencyBadge name="TypeScript" score={9} />
              <CompetencyBadge name="React" score={10} icon={<Star />} />
              <CompetencyBadge name="Python" score={3} size="sm" />
            </div>
          </div>

          {/* MissionStatus */}
          <div>
            <h3 className={h3}>MissionStatus</h3>
            <div className={row}>
              <MissionStatus state="pending" />
              <MissionStatus state="active" />
              <MissionStatus state="completed" />
              <MissionStatus state="failed" />
              <MissionStatus state="locked" />
            </div>
          </div>

          {/* ProgressIndicator */}
          <div>
            <h3 className={h3}>ProgressIndicator</h3>
            <div className="w-80 space-y-3">
              <ProgressIndicator value={45} showLabel />
              <ProgressIndicator value={80} variant="xp" size="lg" />
              <ProgressIndicator value={100} variant="success" />
              <ProgressIndicator value={30} variant="warning" size="sm" />
            </div>
          </div>

          {/* JourneyCard */}
          <div>
            <h3 className={h3}>JourneyCard</h3>
            <div className="grid max-w-md gap-4">
              <JourneyCard
                title="React Foundations"
                description="Master React fundamentals including hooks and state."
                progress={65}
                status="active"
                icon={<BookOpen className="h-6 w-6 text-primary" />}
                action={<Badge variant="xp">+250 XP</Badge>}
              />
              <JourneyCard
                title="TypeScript Mastery"
                description="Advanced types, generics, and patterns."
                progress={100}
                status="completed"
              />
              <JourneyCard
                title="System Design"
                description="Architecture and scalability."
                progress={10}
                status="locked"
              />
            </div>
          </div>

          {/* EvidenceBadge */}
          <div>
            <h3 className={h3}>EvidenceBadge</h3>
            <div className={row}>
              <EvidenceBadge count={3} />
              <EvidenceBadge count={1} label="file" />
              <EvidenceBadge count={12} size="md" />
            </div>
          </div>

          {/* AchievementBadge */}
          <div>
            <h3 className={h3}>AchievementBadge</h3>
            <div className={row}>
              <AchievementBadge icon={<Trophy />} label="First Commit" />
              <AchievementBadge icon={<Zap />} label="Speedrun" unlocked={false} />
              <AchievementBadge icon={<Shield />} label="Security Expert" size="lg" />
              <AchievementBadge icon={<Star />} label="Top Contributor" size="sm" />
            </div>
          </div>
        </section>

        {/* ======== TIER 4 — FEEDBACK ======== */}
        <section className={section}>
          <h2 className={h2}>Tier 4 — Feedback</h2>

          {/* Alert */}
          <div>
            <h3 className={h3}>Alert</h3>
            <div className="space-y-2">
              <Alert variant="success" title="Success">Operation completed successfully.</Alert>
              <Alert variant="error" title="Error">Something went wrong. Please try again.</Alert>
              <Alert variant="warning">Your session will expire in 5 minutes.</Alert>
              <Alert variant="info" title="Did you know?" onDismiss={() => {}}>You can dismiss this alert.</Alert>
            </div>
          </div>

          {/* EmptyState */}
          <div>
            <h3 className={h3}>EmptyState</h3>
            <div className="rounded-md border">
              <EmptyState
                title="No journeys yet"
                description="Complete missions to unlock your first journey."
                action={<Button size="sm">Get Started</Button>}
              />
            </div>
          </div>

          {/* LoadingState */}
          <div>
            <h3 className={h3}>LoadingState</h3>
            <div className="rounded-md border">
              <LoadingState />
            </div>
          </div>

          {/* ErrorState */}
          <div>
            <h3 className={h3}>ErrorState</h3>
            <div className="rounded-md border">
              <ErrorState action={<Button size="sm" variant="secondary">Retry</Button>} />
            </div>
          </div>

          {/* SuccessState */}
          <div>
            <h3 className={h3}>SuccessState</h3>
            <div className="rounded-md border">
              <SuccessState title="Journey complete!" message="You earned 500 XP." action={<Button size="sm">View Rewards</Button>} />
            </div>
          </div>
        </section>
      </div>
    </PageContainer>
  )
}
