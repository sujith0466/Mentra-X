import { describe, it, expect, beforeAll } from 'vitest';
import { render, screen } from '@testing-library/react';
import React from 'react';
import { MemoryRouter } from 'react-router-dom';
import { LandingPage } from '@/pages/public/LandingPage';
import { LoginPage } from '@/pages/auth/LoginPage';
import { StudentDashboardPage } from '@/pages/student/StudentDashboardPage';
import { DigitalTwinPage } from '@/pages/student/DigitalTwinPage';
import { AdminDashboardPage } from '@/pages/admin/AdminDashboardPage';
import { CourseCatalogPage } from '@/pages/public/CourseCatalogPage';
import { ProfilePage } from '@/pages/auth/ProfilePage';
import { CommunityDiscussionsPage } from '@/pages/community/CommunityDiscussionsPage';
import { CodingArenaPage } from '@/pages/student/CodingArenaPage';
import { ManageCoursesPage } from '@/pages/admin/ManageCoursesPage';

describe('Enterprise Frontend Page Suites & Routing', () => {
  beforeAll(() => {
    // Mock IntersectionObserver which is not available in jsdom
    // framer-motion whileInView requires it
    if (typeof window !== 'undefined' && !window.IntersectionObserver) {
      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      (window as any).IntersectionObserver = class {
        observe() {}
        unobserve() {}
        disconnect() {}
        takeRecords() { return []; }
      };
    }
  });

  it('renders LandingPage cleanly with student-centric hero', () => {
    render(
      <MemoryRouter>
        <LandingPage />
      </MemoryRouter>
    );
    expect(screen.getByRole('heading', { level: 1 })).toBeDefined();
  });

  it('renders LoginPage with instant enterprise demo access', () => {
    render(
      <MemoryRouter>
        <LoginPage />
      </MemoryRouter>
    );
    expect(screen.getByText(/Welcome back/i)).toBeDefined();
    expect(screen.getByText(/Sign in to continue your learning journey/i)).toBeDefined();
  });

  it('renders StudentDashboardPage with Digital Twin metrics and Enkrypt protection', () => {
    render(
      <MemoryRouter>
        <StudentDashboardPage />
      </MemoryRouter>
    );
    expect(screen.getByText(/Overall Mastery/i)).toBeDefined();
    expect(screen.getByText(/Today's Study Brief/i)).toBeDefined();
  });

  it('renders DigitalTwinPage with cognitive health score and reasoning inspector', () => {
    render(
      <MemoryRouter>
        <DigitalTwinPage />
      </MemoryRouter>
    );
    expect(screen.getByText(/My Student Learning Profile/i)).toBeDefined();
    expect(screen.getByText(/Recent Cognitive Memory Index/i)).toBeDefined();
  });

  it('renders AdminDashboardPage with AI cluster telemetry and live feed', () => {
    render(
      <MemoryRouter>
        <AdminDashboardPage />
      </MemoryRouter>
    );
    expect(screen.getByText(/AI Operations & Cluster Monitor/i)).toBeDefined();
    expect(screen.getByText(/Mentra tutor Agent Queries/i)).toBeDefined();
  });

  it('renders CourseCatalogPage with enterprise courses and AI filters', () => {
    render(
      <MemoryRouter>
        <CourseCatalogPage />
      </MemoryRouter>
    );
    expect(screen.getByText(/Enterprise Course Catalog/i)).toBeDefined();
    expect(screen.getByText(/Introduction to Artificial Intelligence/i)).toBeDefined();
  });

  it('renders ProfilePage with verified student badge and user identity', () => {
    render(
      <MemoryRouter>
        <ProfilePage />
      </MemoryRouter>
    );
    expect(screen.getByText(/Student Profile & Settings/i)).toBeDefined();
    expect(screen.getByText(/Verified Student/i)).toBeDefined();
  });

  it('renders CommunityDiscussionsPage with scholar discussions and sanitized topics', () => {
    render(
      <MemoryRouter>
        <CommunityDiscussionsPage />
      </MemoryRouter>
    );
    expect(screen.getByText(/Community Forum & Discussions/i)).toBeDefined();
    expect(screen.getByText(/No discussions found matching your filter criteria/i)).toBeDefined();
  });

  it('renders CodingArenaPage with test runner and code editor', () => {
    render(
      <MemoryRouter>
        <CodingArenaPage />
      </MemoryRouter>
    );
    expect(screen.getByText(/Interactive Coding Challenge/i)).toBeDefined();
  });

  it('renders ManageCoursesPage with admin syllabus management', () => {
    render(
      <MemoryRouter>
        <ManageCoursesPage />
      </MemoryRouter>
    );
    expect(screen.getByText(/Syllabus & Course Catalog Management/i)).toBeDefined();
    expect(screen.getAllByText(/AI Tutor/i).length).toBeGreaterThan(0);
  });
});

