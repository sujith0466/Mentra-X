import React from "react";
import { Users, UserPlus, ShieldCheck, Activity } from "lucide-react";
import { DataTable, Column } from "@/components/ui/DataTable";
import { Button } from "@/components/ui/Button";
import { Badge } from "@/components/ui/Badge";
import { Card } from "@/components/ui/Card";

export interface StudentRow {
  id: string;
  name: string;
  email: string;
  twinId: string;
  health: number;
  courses: number;
  status: "Active" | "Suspended" | "Syncing";
}

export const ManageStudentsPage: React.FC = () => {
  const students: StudentRow[] = [
    { id: "STU-101", name: "Sujith Kumar", email: "sujith@mentrax.ai", twinId: "twin_alpha_99", health: 92, courses: 3, status: "Active" },
    { id: "STU-102", name: "Elena Rostova", email: "elena@university.edu", twinId: "twin_beta_14", health: 88, courses: 2, status: "Active" },
    { id: "STU-103", name: "Marcus Vance", email: "marcus@techcorp.io", twinId: "twin_gamma_08", health: 74, courses: 4, status: "Syncing" },
    { id: "STU-104", name: "Sophia Chen", email: "sophia@ai-labs.org", twinId: "twin_delta_42", health: 96, courses: 5, status: "Active" },
  ];

  const columns: Column<StudentRow>[] = [
    { key: "id", title: "Student ID", sortable: true, render: (item) => <span className="font-mono text-xs text-indigo-400">{item.id}</span> },
    { key: "name", title: "Full Name", sortable: true, render: (item) => (
      <div>
        <div className="font-bold text-white">{item.name}</div>
        <div className="text-xs text-slate-400">{item.email}</div>
      </div>
    )},
    { key: "twinId", title: "Digital Twin", sortable: true, render: (item) => <Badge variant="purple" size="sm">{item.twinId}</Badge> },
    { key: "health", title: "Twin Health", sortable: true, render: (item) => (
      <span className={`font-mono font-bold ${item.health >= 90 ? "text-emerald-400" : "text-amber-400"}`}>
        {item.health}/100
      </span>
    )},
    { key: "courses", title: "Enrolled", sortable: true, render: (item) => <span className="text-slate-300">{item.courses} Courses</span> },
    { key: "status", title: "Status", sortable: true, render: (item) => (
      <Badge variant={item.status === "Active" ? "success" : "cyan"} size="sm">{item.status}</Badge>
    )},
    { key: "actions", title: "Actions", render: () => (
      <div className="flex space-x-2">
        <Button size="sm" variant="outline">Inspect Twin</Button>
      </div>
    )}
  ];

  return (
    <div className="space-y-8 py-6">
      <div className="flex flex-col md:flex-row md:items-end justify-between gap-4 border-b border-obsidian-600 pb-6">
        <div>
          <Badge variant="danger" size="sm">Admin Management</Badge>
          <h1 className="text-3xl font-extrabold text-white mt-1">Student Accounts & Digital Twins</h1>
          <p className="text-sm text-slate-400 mt-1">Manage enrolled student profiles, inspect cognitive health graphs, and audit licenses.</p>
        </div>
        <Button size="md" leftIcon={<UserPlus className="w-4 h-4" />}>
          Provision New Student Account
        </Button>
      </div>

      <Card variant="default" className="p-6">
        <DataTable
          data={students}
          columns={columns}
          searchKey="name"
          searchPlaceholder="Search students by name or email..."
        />
      </Card>
    </div>
  );
};
