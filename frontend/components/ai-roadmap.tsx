"use client"

import React from "react"

import { useEffect, useState } from "react"
import {
  Sparkles,
  Target,
  BookOpen,
  Briefcase,
  Award,
  ChevronRight,
  CheckCircle2,
  Circle,
  ArrowRight,
} from "lucide-react"
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import type { UploadResumeResult } from "@/components/resume-upload"

interface RoadmapStep {
  id: number
  title: string
  description: string
  timeline: string
  status: "complete" | "current" | "upcoming"
  icon: React.ElementType
  tasks: string[]
}

const fallbackRoadmapSteps: RoadmapStep[] = [
  {
    id: 1,
    title: "Foundation Strengthening",
    description: "Build core competencies in data structures and system design",
    timeline: "Month 1-2",
    status: "complete",
    icon: BookOpen,
    tasks: [
      "Complete advanced algorithms course",
      "Build 3 system design case studies",
      "Contribute to 2 open-source projects",
    ],
  },
  {
    id: 2,
    title: "Specialization Track",
    description: "Deep dive into ML Engineering and cloud-native architecture",
    timeline: "Month 3-4",
    status: "current",
    icon: Target,
    tasks: [
      "Complete ML Ops certification",
      "Build end-to-end ML pipeline project",
      "Study distributed systems patterns",
    ],
  },
  {
    id: 3,
    title: "Portfolio Building",
    description: "Create high-impact projects that demonstrate your expertise",
    timeline: "Month 5-6",
    status: "upcoming",
    icon: Briefcase,
    tasks: [
      "Launch a full-stack AI application",
      "Write 3 technical blog posts",
      "Present at a local tech meetup",
    ],
  },
  {
    id: 4,
    title: "Career Positioning",
    description: "Strategic networking and interview preparation",
    timeline: "Month 7-8",
    status: "upcoming",
    icon: Award,
    tasks: [
      "Optimize LinkedIn and portfolio",
      "Complete 20 mock interviews",
      "Apply to target companies",
    ],
  },
]

interface AiRoadmapProps {
  analysis?: UploadResumeResult["quick_analysis"] | null
}

function toRoadmapSteps(analysis?: UploadResumeResult["quick_analysis"] | null): RoadmapStep[] {
  if (!analysis?.roadmap?.length) return fallbackRoadmapSteps

  return analysis.roadmap.map((item, index) => ({
    id: index + 1,
    title: item.title,
    description: item.outcome,
    timeline: `Week ${item.week}`,
    status: index === 0 ? "complete" : index === 1 ? "current" : "upcoming",
    icon: index % 2 === 0 ? BookOpen : Target,
    tasks: [
      `Learn core concepts for ${item.title.toLowerCase()}`,
      `Build one artifact to prove ${item.title.toLowerCase()} skills`,
      "Document measurable outcomes in your portfolio",
    ],
  }))
}

export function AiRoadmap({ analysis }: AiRoadmapProps) {
  const roadmapSteps = toRoadmapSteps(analysis)
  const [expandedStep, setExpandedStep] = useState<number | null>(roadmapSteps[1]?.id ?? roadmapSteps[0]?.id ?? null)
  const [hint, setHint] = useState("Based on your skills and market trends, AI suggests focusing on")

  useEffect(() => {
    setExpandedStep(roadmapSteps[1]?.id ?? roadmapSteps[0]?.id ?? null)
  }, [analysis])

  const refinePlan = () => {
    setExpandedStep(3)
    setHint("Roadmap refined. Prioritize")
  }

  return (
    <Card className="border-border bg-card">
      <CardHeader>
        <div className="flex items-center justify-between">
          <div>
            <div className="flex items-center gap-2">
              <Sparkles className="h-4 w-4 text-primary" />
              <CardTitle className="font-display text-lg">AI Career Roadmap</CardTitle>
            </div>
            <CardDescription className="mt-1">
              Personalized 8-month plan to reach Senior Full-Stack ML Engineer
            </CardDescription>
          </div>
          <Badge className="bg-primary/15 text-primary border-primary/25 hover:bg-primary/15">
            AI Generated
          </Badge>
        </div>
      </CardHeader>
      <CardContent>
        <div className="relative">
          {/* Vertical line */}
          <div className="absolute left-[17px] top-2 bottom-2 w-px bg-border" aria-hidden="true" />

          <div className="flex flex-col gap-2">
            {roadmapSteps.map((step) => {
              const isExpanded = expandedStep === step.id
              const StatusIcon = step.status === "complete" ? CheckCircle2 : Circle

              return (
                <div key={step.id} className="relative">
                  <button
                    type="button"
                    onClick={() => setExpandedStep(isExpanded ? null : step.id)}
                    className={`flex w-full items-start gap-3 rounded-lg p-3 text-left transition-colors ${
                      step.status === "current"
                        ? "bg-primary/5 border border-primary/20"
                        : "hover:bg-secondary/60"
                    }`}
                    aria-expanded={isExpanded}
                  >
                    <div className="relative z-10 mt-0.5">
                      <StatusIcon
                        className={`h-[18px] w-[18px] ${
                          step.status === "complete"
                            ? "text-primary fill-primary"
                            : step.status === "current"
                              ? "text-primary"
                              : "text-muted-foreground"
                        }`}
                      />
                    </div>
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center gap-2">
                        <span
                          className={`text-sm font-medium ${
                            step.status === "upcoming" ? "text-muted-foreground" : "text-foreground"
                          }`}
                        >
                          {step.title}
                        </span>
                        <span className="text-[10px] text-muted-foreground">{step.timeline}</span>
                      </div>
                      <p className="mt-0.5 text-xs text-muted-foreground">{step.description}</p>
                    </div>
                    <ChevronRight
                      className={`mt-0.5 h-4 w-4 shrink-0 text-muted-foreground transition-transform ${
                        isExpanded ? "rotate-90" : ""
                      }`}
                    />
                  </button>

                  {isExpanded && (
                    <div className="ml-10 mt-1 mb-1 flex flex-col gap-1.5 rounded-lg bg-secondary/50 p-3">
                      {step.tasks.map((task) => (
                        <div key={task} className="flex items-center gap-2">
                          <ArrowRight className="h-3 w-3 shrink-0 text-primary" />
                          <span className="text-xs text-muted-foreground">{task}</span>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              )
            })}
          </div>
        </div>

        <div className="mt-4 flex items-center gap-3 rounded-lg bg-secondary/50 p-3">
          <Sparkles className="h-4 w-4 shrink-0 text-primary" />
          <p className="flex-1 text-xs text-muted-foreground">
            {hint}{" "}
            <strong className="text-foreground">ML Ops</strong> and{" "}
            <strong className="text-foreground">Cloud Architecture</strong> for maximum career impact.
          </p>
          <Button
            size="sm"
            className="shrink-0 bg-primary text-primary-foreground hover:bg-primary/90"
            onClick={refinePlan}
          >
            Refine Plan
          </Button>
        </div>
      </CardContent>
    </Card>
  )
}
