"use client"

import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Code2, Database, BarChart3, Cloud, Figma, Shield } from "lucide-react"
import type { LucideIcon } from "lucide-react"
import type { UploadResumeResult } from "@/components/resume-upload"

interface Skill {
  name: string
  level: number
  category: string
  icon: LucideIcon
  trending: boolean
}

const fallbackSkills: Skill[] = [
  { name: "React / Next.js", level: 92, category: "Frontend", icon: Code2, trending: true },
  { name: "Python / ML", level: 78, category: "Data Science", icon: BarChart3, trending: true },
  { name: "PostgreSQL", level: 85, category: "Database", icon: Database, trending: false },
  { name: "AWS / Cloud", level: 70, category: "DevOps", icon: Cloud, trending: true },
  { name: "UI / UX Design", level: 65, category: "Design", icon: Figma, trending: false },
  { name: "Cybersecurity", level: 55, category: "Security", icon: Shield, trending: true },
]

function getBarColor(level: number): string {
  if (level >= 80) return "bg-primary"
  if (level >= 60) return "bg-chart-2"
  return "bg-chart-3"
}

function getLevelLabel(level: number): string {
  if (level >= 80) return "Advanced"
  if (level >= 60) return "Intermediate"
  return "Beginner"
}

function categoryFor(name: string): string {
  const key = name.toLowerCase()
  if (["react", "next.js", "typescript", "javascript"].some((item) => key.includes(item))) return "Frontend"
  if (["python", "machine learning", "generative ai", "data analysis"].some((item) => key.includes(item))) return "Data Science"
  if (["postgresql", "sql", "mongodb"].some((item) => key.includes(item))) return "Database"
  if (["docker", "kubernetes", "aws", "azure", "ci/cd"].some((item) => key.includes(item))) return "DevOps"
  if (["figma", "design", "ui", "ux"].some((item) => key.includes(item))) return "Design"
  if (["security", "testing"].some((item) => key.includes(item))) return "Security"
  return "General"
}

function iconFor(category: string): LucideIcon {
  if (category === "Frontend") return Code2
  if (category === "Data Science") return BarChart3
  if (category === "Database") return Database
  if (category === "DevOps") return Cloud
  if (category === "Design") return Figma
  return Shield
}

interface SkillsDisplayProps {
  analysis?: UploadResumeResult["quick_analysis"] | null
}

export function SkillsDisplay({ analysis }: SkillsDisplayProps) {
  const skills: Skill[] = analysis
    ? analysis.skill_scores.map((item) => {
        const category = categoryFor(item.skill_name)
        return {
          name: item.skill_name,
          level: item.trend_score,
          category,
          icon: iconFor(category),
          trending: item.status === "high_growth",
        }
      })
    : fallbackSkills

  return (
    <Card className="border-border bg-card">
      <CardHeader>
        <CardTitle className="font-display text-lg">Your Skills</CardTitle>
        <CardDescription>Extracted from your resume and career profile</CardDescription>
      </CardHeader>
      <CardContent>
        <div className="grid gap-3 sm:grid-cols-2">
          {skills.map((skill) => (
            <div
              key={skill.name}
              className="group flex items-start gap-3 rounded-lg border border-border bg-secondary/40 p-3 transition-colors hover:border-primary/30 hover:bg-secondary/70"
            >
              <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg bg-secondary">
                <skill.icon className="h-4 w-4 text-muted-foreground group-hover:text-primary transition-colors" />
              </div>
              <div className="flex-1 min-w-0">
                <div className="flex items-center justify-between gap-2">
                  <span className="text-sm font-medium text-foreground truncate">{skill.name}</span>
                  {skill.trending && (
                    <Badge variant="outline" className="shrink-0 border-primary/30 text-primary text-[10px] px-1.5 py-0">
                      Trending
                    </Badge>
                  )}
                </div>
                <div className="mt-1.5 flex items-center gap-2">
                  <div className="h-1.5 flex-1 overflow-hidden rounded-full bg-muted">
                    <div
                      className={`h-full rounded-full transition-all duration-500 ${getBarColor(skill.level)}`}
                      style={{ width: `${skill.level}%` }}
                    />
                  </div>
                  <span className="shrink-0 text-[10px] font-medium text-muted-foreground">
                    {getLevelLabel(skill.level)}
                  </span>
                </div>
                <p className="mt-1 text-[11px] text-muted-foreground">{skill.category}</p>
              </div>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  )
}
