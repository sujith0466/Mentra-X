import React, { Suspense } from "react";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { AppLayout } from "@/components/layout/AppLayout";
import { AuthLayout } from "@/components/layout/AuthLayout";

// Public Pages
import { LandingPage } from "@/pages/public/LandingPage";
import { AboutPage } from "@/pages/public/AboutPage";
import { ContactPage } from "@/pages/public/ContactPage";
import { CourseCatalogPage } from "@/pages/public/CourseCatalogPage";
import { CourseDetailPage } from "@/pages/public/CourseDetailPage";
import { PricingPage } from "@/pages/public/PricingPage";
import { FAQPage } from "@/pages/public/FAQPage";
import { DocumentationPage } from "@/pages/public/DocumentationPage";
import { HelpPage } from "@/pages/public/HelpPage";

// Auth Pages
import { LoginPage } from "@/pages/auth/LoginPage";
import { RegisterPage } from "@/pages/auth/RegisterPage";
import { ForgotPasswordPage } from "@/pages/auth/ForgotPasswordPage";
import { ProfilePage } from "@/pages/auth/ProfilePage";
import { SettingsPage } from "@/pages/auth/SettingsPage";

// Student Pages
import { StudentDashboardPage } from "@/pages/student/StudentDashboardPage";
import { MyCoursesPage } from "@/pages/student/MyCoursesPage";
import { CourseViewerPage } from "@/pages/student/CourseViewerPage";
import { CareerResumePage } from "@/pages/student/CareerResumePage";
import { CodingArenaPage } from "@/pages/student/CodingArenaPage";
import { InterviewPrepPage } from "@/pages/student/InterviewPrepPage";
import { DigitalTwinPage } from "@/pages/student/DigitalTwinPage";
import { StudyPlannerPage } from "@/pages/student/StudyPlannerPage";
import { AssessmentPage } from "@/pages/student/AssessmentPage";
import { NotesPage } from "@/pages/student/NotesPage";
import { RecommendationsPage } from "@/pages/student/RecommendationsPage";
import { ProjectsPage } from "@/pages/student/ProjectsPage";
import { AITutorPage } from "@/pages/student/AITutorPage";

// Community Pages
import { CommunityDiscussionsPage } from "@/pages/community/CommunityDiscussionsPage";
import { CommunityPostDetailPage } from "@/pages/community/CommunityPostDetailPage";
import { LeaderboardPage } from "@/pages/community/LeaderboardPage";
import { GroupsPage } from "@/pages/community/GroupsPage";
import { EventsPage } from "@/pages/community/EventsPage";

// Admin Pages
import { AdminDashboardPage } from "@/pages/admin/AdminDashboardPage";
import { ManageStudentsPage } from "@/pages/admin/ManageStudentsPage";
import { ManageCoursesPage } from "@/pages/admin/ManageCoursesPage";
import { AuditLogsPage } from "@/pages/admin/AuditLogsPage";
import { AnalyticsPage } from "@/pages/admin/AnalyticsPage";
import { AIMonitoringPage } from "@/pages/admin/AIMonitoringPage";
import { EnkryptDashboardPage } from "@/pages/admin/EnkryptDashboardPage";

const LoadingFallback = () => (
  <div className="min-h-screen bg-slate-50 dark:bg-obsidian-900 flex items-center justify-center text-slate-600 dark:text-slate-400 font-mono text-sm">
    <div className="flex flex-col items-center space-y-3">
      <div className="w-8 h-8 rounded-full border-2 border-indigo-500 border-t-transparent animate-spin" />
      <span>Loading Mentra X Enterprise Workspace...</span>
    </div>
  </div>
);

export default function App() {
  return (
    <BrowserRouter>
      <Suspense fallback={<LoadingFallback />}>
        <Routes>
          {/* Main App Layout Shell */}
          <Route element={<AppLayout />}>
            {/* Public Routes */}
            <Route path="/" element={<LandingPage />} />
            <Route path="/about" element={<AboutPage />} />
            <Route path="/contact" element={<ContactPage />} />
            <Route path="/courses" element={<CourseCatalogPage />} />
            <Route path="/course/:id" element={<CourseDetailPage />} />
            <Route path="/pricing" element={<PricingPage />} />
            <Route path="/faq" element={<FAQPage />} />
            <Route path="/docs" element={<DocumentationPage />} />
            <Route path="/help" element={<HelpPage />} />

            {/* User Profile & Settings */}
            <Route path="/profile" element={<ProfilePage />} />
            <Route path="/settings" element={<SettingsPage />} />

            {/* Student Portal Routes */}
            <Route path="/student/dashboard" element={<StudentDashboardPage />} />
            <Route path="/student/my-courses" element={<MyCoursesPage />} />
            <Route path="/student/course/:id" element={<CourseViewerPage />} />
            <Route path="/student/career/resume" element={<CareerResumePage />} />
            <Route path="/student/career/roadmap" element={<CareerResumePage />} />
            <Route path="/student/coding" element={<CodingArenaPage />} />
            <Route path="/student/interview" element={<InterviewPrepPage />} />
            <Route path="/student/twin" element={<DigitalTwinPage />} />
            <Route path="/student/ai/planner" element={<StudyPlannerPage />} />
            <Route path="/student/assessment" element={<AssessmentPage />} />
            <Route path="/student/notes" element={<NotesPage />} />
            <Route path="/student/recommendations" element={<RecommendationsPage />} />
            <Route path="/student/projects" element={<ProjectsPage />} />
            <Route path="/student/ai/tutor" element={<AITutorPage />} />

            {/* Legacy Student Route Redirects for 100% Backward Compatibility */}
            <Route path="/student/ai/notes" element={<Navigate to="/student/notes" replace />} />
            <Route path="/student/ai/recommendations" element={<Navigate to="/student/recommendations" replace />} />
            <Route path="/student/ai/practice" element={<Navigate to="/student/ai/tutor" replace />} />
            <Route path="/student/ai/revision" element={<Navigate to="/student/ai/tutor" replace />} />
            <Route path="/student/ai/project-ideas" element={<Navigate to="/student/projects" replace />} />
            <Route path="/student/devtools/explainer" element={<Navigate to="/student/coding" replace />} />
            <Route path="/student/devtools/debug" element={<Navigate to="/student/ai/tutor" replace />} />

            {/* Community Portal Routes */}
            <Route path="/community" element={<CommunityDiscussionsPage />} />
            <Route path="/community/discussions" element={<CommunityDiscussionsPage />} />
            <Route path="/community/discussions/:id" element={<CommunityPostDetailPage />} />
            <Route path="/community/leaderboard" element={<LeaderboardPage />} />
            <Route path="/community/groups" element={<GroupsPage />} />
            <Route path="/community/events" element={<EventsPage />} />

            {/* Admin Portal Routes */}
            <Route path="/admin/dashboard" element={<AdminDashboardPage />} />
            <Route path="/admin/students" element={<ManageStudentsPage />} />
            <Route path="/admin/courses" element={<ManageCoursesPage />} />
            <Route path="/admin/audit-logs" element={<AuditLogsPage />} />
            <Route path="/admin/analytics" element={<AnalyticsPage />} />
            <Route path="/admin/ai-monitoring" element={<AIMonitoringPage />} />
            <Route path="/admin/enkrypt" element={<EnkryptDashboardPage />} />
          </Route>

          {/* Auth Layout Shell */}
          <Route element={<AuthLayout />}>
            <Route path="/login" element={<LoginPage />} />
            <Route path="/register" element={<RegisterPage />} />
            <Route path="/forgot-password" element={<ForgotPasswordPage />} />
          </Route>

          {/* Fallback */}
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </Suspense>
    </BrowserRouter>
  );
}
