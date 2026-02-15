"use client"

import React from "react"

import { useState, useCallback } from "react"
import { Upload, FileText, CheckCircle2, X } from "lucide-react"
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"

type UploadState = "idle" | "dragging" | "uploading" | "complete"
const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000"

export interface UploadResumeResult {
  parsed_profile: {
    skills: string[]
    parse_warning?: string | null
  }
  quick_analysis: {
    career_health_score: number
    recommended_paths: string[]
    skill_scores: Array<{
      skill_name: string
      status: "obsolete" | "stable" | "high_growth"
      trend_score: number
      insight: string
    }>
    roadmap: Array<{
      week: number
      title: string
      outcome: string
    }>
    trends: Array<{
      skill_name: string
      points: Array<{
        label: string
        demand_score: number
      }>
    }>
  }
}

interface ResumeUploadProps {
  onAnalyzed?: (data: UploadResumeResult) => void
}

export function ResumeUpload({ onAnalyzed }: ResumeUploadProps) {
  const [uploadState, setUploadState] = useState<UploadState>("idle")
  const [fileName, setFileName] = useState<string | null>(null)
  const [progress, setProgress] = useState(0)
  const [error, setError] = useState<string | null>(null)
  const [warning, setWarning] = useState<string | null>(null)


  const uploadResume = async (file: File) => {
    const formData = new FormData()
    formData.append("file", file)

    try {
      setError(null)
      setWarning(null)
      setFileName(file.name)
      setProgress(35)
      setUploadState("uploading")

      const res = await fetch(`${API_BASE_URL}/api/upload-resume`, {
        method: "POST",
        body: formData,
      })

      if (!res.ok) {
        const errorPayload = await res.json().catch(() => null)
        const detail = typeof errorPayload?.detail === "string" ? errorPayload.detail : `Upload failed with status ${res.status}`
        throw new Error(detail)
      }

      const data = (await res.json()) as UploadResumeResult

      console.log("Parsed profile:", data?.parsed_profile)
      const parseWarning =
        typeof data?.parsed_profile?.parse_warning === "string" ? data.parsed_profile.parse_warning : null
      setWarning(parseWarning)
      onAnalyzed?.(data)
      setProgress(100)
      setUploadState("complete")
    } catch (err) {
      console.error(err)
      setUploadState("idle")
      setProgress(0)
      const message = err instanceof Error ? err.message : "Upload failed. Please try again."
      setError(message)
    }
  }

  const handleDrop = useCallback(
    (e: React.DragEvent) => {
      e.preventDefault()
      setUploadState("idle")
      const file = e.dataTransfer.files[0]
      if (file) uploadResume(file)
    },
    [],
  )

  const handleFileChange = useCallback(
    (e: React.ChangeEvent<HTMLInputElement>) => {
      const file = e.target.files?.[0]
      if (file) uploadResume(file)
    },
    [],
  )

  const handleReset = () => {
    setUploadState("idle")
    setFileName(null)
    setProgress(0)
    setError(null)
    setWarning(null)
  }

  return (
    <Card className="border-border bg-card">
      <CardHeader>
        <div className="flex items-center justify-between">
          <div>
            <CardTitle className="font-display text-lg">Resume Upload</CardTitle>
            <CardDescription>Upload your resume to get AI-powered career insights</CardDescription>
          </div>
          {uploadState === "complete" && (
            <Badge className="bg-primary/15 text-primary border-primary/25 hover:bg-primary/15">
              Analyzed
            </Badge>
          )}
        </div>
      </CardHeader>
      <CardContent>
        {uploadState === "complete" ? (
          <div className="flex items-center gap-4 rounded-lg border border-primary/20 bg-primary/5 p-4">
            <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-lg bg-primary/15">
              <CheckCircle2 className="h-5 w-5 text-primary" />
            </div>
            <div className="flex-1">
              <p className="text-sm font-medium text-foreground">{fileName}</p>
              <p className="text-xs text-muted-foreground">Successfully analyzed by AI</p>
            </div>
            <Button variant="ghost" size="icon" onClick={handleReset} aria-label="Remove file">
              <X className="h-4 w-4 text-muted-foreground" />
            </Button>
          </div>
        ) : (
          <div
            onDragOver={(e) => {
              e.preventDefault()
              setUploadState("dragging")
            }}
            onDragLeave={() => setUploadState(uploadState === "dragging" ? "idle" : uploadState)}
            onDrop={handleDrop}
            className={`relative flex flex-col items-center justify-center gap-3 rounded-lg border-2 border-dashed p-8 transition-colors ${
              uploadState === "dragging"
                ? "border-primary bg-primary/5"
                : "border-border hover:border-muted-foreground/30"
            }`}
          >
            {uploadState === "uploading" ? (
              <div className="flex w-full flex-col items-center gap-3">
                <div className="flex h-12 w-12 items-center justify-center rounded-full bg-secondary">
                  <FileText className="h-6 w-6 text-primary" />
                </div>
                <p className="text-sm font-medium text-foreground">{fileName}</p>
                <div className="h-1.5 w-full max-w-xs overflow-hidden rounded-full bg-secondary">
                  <div
                    className="h-full rounded-full bg-primary transition-all duration-300"
                    style={{ width: `${progress}%` }}
                  />
                </div>
                <p className="text-xs text-muted-foreground">
                  {`Analyzing... ${Math.round(progress)}%`}
                </p>
              </div>
            ) : (
              <>
                <div className="flex h-12 w-12 items-center justify-center rounded-full bg-secondary">
                  <Upload className="h-6 w-6 text-muted-foreground" />
                </div>
                <div className="text-center">
                  <p className="text-sm font-medium text-foreground">
                    Drop your resume here or{" "}
                    <label className="cursor-pointer text-primary hover:underline">
                      browse
                      <input
                        type="file"
                        className="sr-only"
                        accept=".pdf,.docx,.txt"
                        onChange={handleFileChange}
                        aria-label="Upload resume file"
                      />
                    </label>
                  </p>
                  <p className="mt-1 text-xs text-muted-foreground">
                    Supports PDF, DOCX, TXT (max 10MB)
                  </p>
                </div>
              </>
            )}
          </div>
        )}

        {error && (
          <p className="mt-3 text-xs text-destructive" role="alert">
            {error}
          </p>
        )}

        {warning && !error && (
          <p className="mt-3 text-xs text-amber-400" role="status">
            {warning}
          </p>
        )}
      </CardContent>
    </Card>
  )
}
