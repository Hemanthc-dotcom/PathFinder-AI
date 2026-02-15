"use client"

import { useState } from "react"
import { DashboardHeader } from "@/components/dashboard-header"
import { StatsOverview } from "@/components/stats-overview"
import { ResumeUpload, type UploadResumeResult } from "@/components/resume-upload"
import { SkillsDisplay } from "@/components/skills-display"
import { SkillDemandChart } from "@/components/skill-demand-chart"
import { AiRoadmap } from "@/components/ai-roadmap"


export default function Page() {
  const [analysisResult, setAnalysisResult] = useState<UploadResumeResult | null>(null)

  return (
    <div className="min-h-screen bg-background">
      <DashboardHeader />

      <main className="mx-auto max-w-7xl px-4 py-6 sm:px-6 lg:px-8">
        {/* Welcome */}
        <div className="mb-6">
          <h1 className="font-display text-2xl font-bold tracking-tight text-foreground sm:text-3xl">
            Welcome back, Alex
          </h1>
          <p className="mt-1 text-sm text-muted-foreground">
            {"Here's your AI-powered career dashboard. Let's build your future."}
          </p>
        </div>

        {/* Stats */}
        <section aria-label="Career statistics" className="mb-6">
          <StatsOverview analysis={analysisResult?.quick_analysis ?? null} />
        </section>

        {/* Two-column layout */}
        <div className="grid gap-6 lg:grid-cols-2">
          {/* Left column */}
          <div className="flex flex-col gap-6">
            <section aria-label="Resume upload">
              <ResumeUpload onAnalyzed={setAnalysisResult} />
            </section>
            <section aria-label="Skill demand trends">
              <SkillDemandChart analysis={analysisResult?.quick_analysis ?? null} />
            </section>
          </div>

          {/* Right column */}
          <div className="flex flex-col gap-6">
            <section aria-label="Skills display">
              <SkillsDisplay analysis={analysisResult?.quick_analysis ?? null} />
            </section>
            <section aria-label="AI career roadmap">
              <AiRoadmap analysis={analysisResult?.quick_analysis ?? null} />
            </section>
          </div>
        </div>
      </main>
    </div>
  )
}
