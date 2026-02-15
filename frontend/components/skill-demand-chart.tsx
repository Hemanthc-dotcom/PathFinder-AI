"use client"

import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/tabs"
import type { UploadResumeResult } from "@/components/resume-upload"
import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  BarChart,
  Bar,
} from "recharts"

const fallbackMonthlyData = [
  { month: "Jul", react: 85, python: 72, cloud: 60, security: 45 },
  { month: "Aug", react: 87, python: 76, cloud: 62, security: 48 },
  { month: "Sep", react: 90, python: 80, cloud: 68, security: 52 },
  { month: "Oct", react: 88, python: 84, cloud: 72, security: 58 },
  { month: "Nov", react: 92, python: 88, cloud: 78, security: 65 },
  { month: "Dec", react: 94, python: 92, cloud: 82, security: 72 },
  { month: "Jan", react: 96, python: 95, cloud: 88, security: 78 },
]

const fallbackRoleData = [
  { role: "Full-Stack Dev", demand: 94 },
  { role: "ML Engineer", demand: 91 },
  { role: "Cloud Architect", demand: 87 },
  { role: "Data Scientist", demand: 85 },
  { role: "DevOps Lead", demand: 80 },
  { role: "Security Eng", demand: 78 },
]

function toDynamicTrendRows(analysis?: UploadResumeResult["quick_analysis"] | null): Array<Record<string, string | number>> {
  if (!analysis?.trends?.length) return fallbackMonthlyData

  const labels = analysis.trends[0].points.map((point) => point.label)
  return labels.map((label, index) => {
    const row: Record<string, string | number> = { month: label }
    analysis.trends.forEach((trend) => {
      row[trend.skill_name] = trend.points[index]?.demand_score ?? 0
    })
    return row
  })
}

function toDynamicRoleRows(analysis?: UploadResumeResult["quick_analysis"] | null): Array<{ role: string; demand: number }> {
  if (!analysis?.recommended_paths?.length) return fallbackRoleData
  return analysis.recommended_paths.slice(0, 6).map((role, index) => ({
    role,
    demand: Math.max(55, Math.min(99, analysis.career_health_score + 8 - index * 5)),
  }))
}

interface SkillDemandChartProps {
  analysis?: UploadResumeResult["quick_analysis"] | null
}

function CustomTooltip({ active, payload, label }: { active?: boolean; payload?: Array<{ color: string; name: string; value: number }>; label?: string }) {
  if (!active || !payload) return null
  return (
    <div className="rounded-lg border border-border bg-card px-3 py-2 shadow-lg">
      <p className="mb-1 text-xs font-medium text-foreground">{label}</p>
      {payload.map((item) => (
        <div key={item.name} className="flex items-center gap-2 text-xs">
          <span className="h-2 w-2 rounded-full" style={{ background: item.color }} />
          <span className="text-muted-foreground capitalize">{item.name}:</span>
          <span className="font-medium text-foreground">{item.value}</span>
        </div>
      ))}
    </div>
  )
}

export function SkillDemandChart({ analysis }: SkillDemandChartProps) {
  const monthlyData = toDynamicTrendRows(analysis)
  const roleData = toDynamicRoleRows(analysis)
  const trendKeys = Object.keys(monthlyData[0] ?? {}).filter((key) => key !== "month")

  return (
    <Card className="border-border bg-card">
      <CardHeader>
        <CardTitle className="font-display text-lg">Skill Demand Trends</CardTitle>
        <CardDescription>Market demand for your skills over time</CardDescription>
      </CardHeader>
      <CardContent>
        <Tabs defaultValue="trend">
          <TabsList className="mb-4">
            <TabsTrigger value="trend">Trend</TabsTrigger>
            <TabsTrigger value="roles">By Role</TabsTrigger>
          </TabsList>

          <TabsContent value="trend">
            <div className="h-[280px] w-full">
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={monthlyData} margin={{ top: 4, right: 4, left: -20, bottom: 0 }}>
                  <defs>
                    <linearGradient id="fillReact" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="0%" stopColor="hsl(160, 84%, 50%)" stopOpacity={0.3} />
                      <stop offset="100%" stopColor="hsl(160, 84%, 50%)" stopOpacity={0} />
                    </linearGradient>
                    <linearGradient id="fillPython" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="0%" stopColor="hsl(200, 75%, 55%)" stopOpacity={0.3} />
                      <stop offset="100%" stopColor="hsl(200, 75%, 55%)" stopOpacity={0} />
                    </linearGradient>
                    <linearGradient id="fillCloud" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="0%" stopColor="hsl(35, 92%, 60%)" stopOpacity={0.2} />
                      <stop offset="100%" stopColor="hsl(35, 92%, 60%)" stopOpacity={0} />
                    </linearGradient>
                  </defs>
                  <CartesianGrid strokeDasharray="3 3" stroke="hsl(220, 14%, 18%)" vertical={false} />
                  <XAxis dataKey="month" tick={{ fill: "hsl(215, 12%, 55%)", fontSize: 12 }} axisLine={false} tickLine={false} />
                  <YAxis tick={{ fill: "hsl(215, 12%, 55%)", fontSize: 12 }} axisLine={false} tickLine={false} />
                  <Tooltip content={<CustomTooltip />} />
                  {trendKeys.map((key, index) => {
                    const style = [
                      { stroke: "hsl(160, 84%, 50%)", fill: "url(#fillReact)", dasharray: undefined },
                      { stroke: "hsl(200, 75%, 55%)", fill: "url(#fillPython)", dasharray: undefined },
                      { stroke: "hsl(35, 92%, 60%)", fill: "url(#fillCloud)", dasharray: undefined },
                      { stroke: "hsl(340, 75%, 55%)", fill: "none", dasharray: "4 4" },
                    ][index % 4]

                    return (
                      <Area
                        key={key}
                        type="monotone"
                        dataKey={key}
                        stroke={style.stroke}
                        fill={style.fill}
                        strokeWidth={2}
                        strokeDasharray={style.dasharray}
                        dot={false}
                      />
                    )
                  })}
                </AreaChart>
              </ResponsiveContainer>
            </div>
            <div className="mt-3 flex flex-wrap gap-4">
              {trendKeys.map((label, index) => {
                const color = ["bg-primary", "bg-chart-2", "bg-chart-3", "bg-chart-5"][index % 4]
                return (
                  <div key={label} className="flex items-center gap-1.5 text-xs text-muted-foreground">
                    <span className={`h-2 w-2 rounded-full ${color}`} />
                    {label}
                  </div>
                )
              })}
            </div>
          </TabsContent>

          <TabsContent value="roles">
            <div className="h-[280px] w-full">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={roleData} layout="vertical" margin={{ top: 4, right: 4, left: 20, bottom: 0 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke="hsl(220, 14%, 18%)" horizontal={false} />
                  <XAxis type="number" tick={{ fill: "hsl(215, 12%, 55%)", fontSize: 12 }} axisLine={false} tickLine={false} domain={[0, 100]} />
                  <YAxis type="category" dataKey="role" tick={{ fill: "hsl(215, 12%, 55%)", fontSize: 11 }} axisLine={false} tickLine={false} width={95} />
                  <Tooltip content={<CustomTooltip />} />
                  <Bar dataKey="demand" fill="hsl(160, 84%, 50%)" radius={[0, 6, 6, 0]} barSize={20} />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </TabsContent>
        </Tabs>
      </CardContent>
    </Card>
  )
}
