"use client"

import { TrendingUp, Target, Zap, BookOpen } from "lucide-react"
import type { UploadResumeResult } from "@/components/resume-upload"

const fallbackStats = [
  {
    label: "Career Match",
    value: "87%",
    change: "+5%",
    icon: Target,
  },
  {
    label: "Skills Analyzed",
    value: "12",
    change: "+3",
    icon: Zap,
  },
  {
    label: "Market Demand",
    value: "High",
    change: "Rising",
    icon: TrendingUp,
  },
  {
    label: "Courses Suggested",
    value: "8",
    change: "New",
    icon: BookOpen,
  },
]

interface StatsOverviewProps {
  analysis?: UploadResumeResult["quick_analysis"] | null
}

export function StatsOverview({ analysis }: StatsOverviewProps) {
  const marketDemand = analysis
    ? analysis.career_health_score >= 80
      ? "High"
      : analysis.career_health_score >= 60
        ? "Medium"
        : "Low"
    : "High"

  const stats = analysis
    ? [
        {
          label: "Career Match",
          value: `${analysis.career_health_score}%`,
          change: "Live",
          icon: Target,
        },
        {
          label: "Skills Analyzed",
          value: String(analysis.skill_scores.length),
          change: `${analysis.skill_scores.filter((item) => item.status === "high_growth").length} trending`,
          icon: Zap,
        },
        {
          label: "Market Demand",
          value: marketDemand,
          change: "Updated",
          icon: TrendingUp,
        },
        {
          label: "Courses Suggested",
          value: String(analysis.roadmap.length),
          change: "Personalized",
          icon: BookOpen,
        },
      ]
    : fallbackStats

  return (
    <div className="grid grid-cols-2 gap-3 lg:grid-cols-4">
      {stats.map((stat) => (
        <div
          key={stat.label}
          className="flex items-center gap-3 rounded-lg border border-border bg-card p-4 transition-colors hover:border-primary/25"
        >
          <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-lg bg-secondary">
            <stat.icon className="h-5 w-5 text-primary" />
          </div>
          <div>
            <p className="text-xs text-muted-foreground">{stat.label}</p>
            <div className="flex items-baseline gap-1.5">
              <span className="text-xl font-bold text-foreground">{stat.value}</span>
              <span className="text-[10px] font-medium text-primary">{stat.change}</span>
            </div>
          </div>
        </div>
      ))}
    </div>
  )
}
