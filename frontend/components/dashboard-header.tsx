"use client"

import { useState } from "react"
import { BrainCircuit, Bell, Search } from "lucide-react"
import { Button } from "@/components/ui/button"

export function DashboardHeader() {
  const [hasNotifications, setHasNotifications] = useState(true)

  return (
    <header className="flex items-center justify-between border-b border-border px-6 py-4">
      <div className="flex items-center gap-3">
        <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-primary">
          <BrainCircuit className="h-5 w-5 text-primary-foreground" />
        </div>
        <span className="font-display text-xl font-bold tracking-tight text-foreground">
          PathFinder AI
        </span>
      </div>

      <div className="hidden items-center gap-1 rounded-lg bg-secondary px-3 py-2 md:flex">
        <Search className="h-4 w-4 text-muted-foreground" />
        <input
          type="text"
          placeholder="Search skills, roles, resources..."
          className="w-64 bg-transparent text-sm text-foreground placeholder:text-muted-foreground focus:outline-none"
          aria-label="Search"
        />
      </div>

      <div className="flex items-center gap-3">
        <Button
          variant="ghost"
          size="icon"
          className="relative"
          aria-label="Notifications"
          onClick={() => setHasNotifications((value) => !value)}
          title={hasNotifications ? "Mark notifications as read" : "No unread notifications"}
        >
          <Bell className="h-5 w-5 text-muted-foreground" />
          {hasNotifications && <span className="absolute right-1.5 top-1.5 h-2 w-2 rounded-full bg-primary" />}
        </Button>
        <div className="flex items-center gap-2">
          <div className="flex h-8 w-8 items-center justify-center rounded-full bg-primary text-sm font-semibold text-primary-foreground">
            A
          </div>
          <span className="hidden text-sm font-medium text-foreground md:block">Alex Chen</span>
        </div>
      </div>
    </header>
  )
}
