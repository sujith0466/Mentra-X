import { describe, it, expect } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import React from 'react';
import { Button } from '@/components/ui/Button';
import { Badge } from '@/components/ui/Badge';
import { Card, CardTitle, CardDescription } from '@/components/ui/Card';
import { SafetyBadge } from '@/components/widgets/SafetyBadge';
import { ConfidenceMeter } from '@/components/widgets/ConfidenceMeter';

describe('Enterprise Atomic Component Library', () => {
  it('renders Button correctly and responds to clicks', () => {
    let clicked = false;
    render(<Button onClick={() => { clicked = true; }}>Click Me</Button>);
    const btn = screen.getByText('Click Me');
    expect(btn).toBeDefined();
    fireEvent.click(btn);
    expect(clicked).toBe(true);
  });

  it('renders Badge with correct variant text', () => {
    render(<Badge variant="success">Enterprise Certified</Badge>);
    expect(screen.getByText('Enterprise Certified')).toBeDefined();
  });

  it('renders Card with header title and description', () => {
    render(
      <Card variant="glass">
        <CardTitle>AI Assistant</CardTitle>
        <CardDescription>Powered by AI Swarm</CardDescription>
      </Card>
    );
    expect(screen.getByText('AI Assistant')).toBeDefined();
    expect(screen.getByText('Powered by AI Swarm')).toBeDefined();
  });

  it('renders SafetyBadge with APPROVE status', () => {
    render(<SafetyBadge status="APPROVE" score={0.98} />);
    expect(screen.getByText('Safety Approved')).toBeDefined();
    expect(screen.getByText('98%')).toBeDefined();
  });

  it('renders ConfidenceMeter percentage correctly', () => {
    render(<ConfidenceMeter score={0.95} label="AI Certainty" />);
    expect(screen.getByText('AI Certainty')).toBeDefined();
    expect(screen.getByText('95%')).toBeDefined();
  });
});
