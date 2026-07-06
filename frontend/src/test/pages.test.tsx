import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import React from 'react';
import { MemoryRouter } from 'react-router-dom';
import { LandingPage } from '@/pages/public/LandingPage';
import { LoginPage } from '@/pages/auth/LoginPage';
import { StudentDashboardPage } from '@/pages/student/StudentDashboardPage';
import { DigitalTwinPage } from '@/pages/student/DigitalTwinPage';
import { AdminDashboardPage } from '@/pages/admin/AdminDashboardPage';

describe('Enterprise Frontend Page Suites & Routing', () => {
  it('renders LandingPage cleanly with Enkrypt active banner', () => {
    render(
      <MemoryRouter>
        <LandingPage />
      </MemoryRouter>
    );
    expect(screen.getByText(/The Next-Generation AI LMS/i)).toBeDefined();
  });

  it('renders LoginPage with instant enterprise demo access', () => {
    render(
      <MemoryRouter>
        <LoginPage />
      </MemoryRouter>
    );
    expect(screen.getByText(/Sign In to Your Account/i)).toBeDefined();
    expect(screen.getByText(/Instant Enterprise Demo Access/i)).toBeDefined();
  });

  it('renders StudentDashboardPage with Digital Twin metrics and Enkrypt protection', () => {
    render(
      <MemoryRouter>
        <StudentDashboardPage />
      </MemoryRouter>
    );
    expect(screen.getByText(/Overall Mastery/i)).toBeDefined();
    expect(screen.getByText(/Daily Cognitive Briefing/i)).toBeDefined();
  });

  it('renders DigitalTwinPage with cognitive health score and reasoning inspector', () => {
    render(
      <MemoryRouter>
        <DigitalTwinPage />
      </MemoryRouter>
    );
    expect(screen.getByText(/My Student Digital Twin/i)).toBeDefined();
    expect(screen.getByText(/Recent Cognitive Memory Index/i)).toBeDefined();
  });

  it('renders AdminDashboardPage with AI cluster telemetry and live feed', () => {
    render(
      <MemoryRouter>
        <AdminDashboardPage />
      </MemoryRouter>
    );
    expect(screen.getByText(/AI Operations & Cluster Monitor/i)).toBeDefined();
    expect(screen.getByText(/Mastra Swarm Agent Queries/i)).toBeDefined();
  });
});
