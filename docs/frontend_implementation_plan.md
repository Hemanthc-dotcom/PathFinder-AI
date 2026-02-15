# Frontend Implementation Plan

## Intelligent Career Counsellor system

### Technology Stack

- **Framework:** Next.js 14 (App Router)
- **Language:** TypeScript
- **Styling:** Tailwind CSS + Shadcn/UI (optional but recommended)
- **Icons:** Lucide React

### Phase 1: Setup & Scaffolding

1.  **Initialize Next.js App**
    ```bash
    npx create-next-app@latest frontend --typescript --tailwind --eslint
    ```
2.  **Clean up boilerplate**: Remove default Next.js home page content.
3.  **Install Libraries**:
    ```bash
    npm install lucide-react recharts axios framer-motion clsx tailwind-merge
    ```

### Phase 2: Component Development

1.  **Layout Components**
    - `Navbar`: specific links (Dashboard, Upload, Chat).
    - `Footer`: simple branding.

2.  **Feature Components**
    - `FileUploader`: Drag & drop area for resumes.
    - `SkillCard`: Display individual skill with a color-coded status (Red=Obsolete, Green=Growing).
    - `TrendGraph`: Recharts line chart for skill demand.
    - `ChatInterface`: Chat bubble UX for the AI mentor.

### Phase 3: Page Construction

1.  **Landing Page (`/`)**
    - Hero section, Value proposition, "Get Started" button.
2.  **Dashboard (`/dashboard`)**
    - The main view after login/upload. Shows the analysis summary.
3.  **Detailed Analysis (`/analysis`)**
    - Deep dive into specific skills and learning paths.

### Phase 4: Integration

- Connect `FileUploader` to Backend `POST /api/upload-resume`.
- Fetch analysis data and populate `TrendGraph`.
- Connect `ChatInterface` to Backend `POST /api/chat`.

### Verification

- **Build Check:** `npm run build` must pass.
- **Lint Check:** `npm run lint` must pass.
- **Visual Check:** Responsive design verification on Mobile/Desktop sizes.
