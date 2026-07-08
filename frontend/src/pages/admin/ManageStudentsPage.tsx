import React, { useState } from "react";
import { Users, UserPlus, ShieldCheck, Activity } from "lucide-react";
import { DataTable, Column } from "@/components/ui/DataTable";
import { Button } from "@/components/ui/Button";
import { Badge } from "@/components/ui/Badge";
import { Card } from "@/components/ui/Card";
import { Modal } from "@/components/ui/Modal";
import { Input } from "@/components/ui/Input";
import { useStudentStore, StudentRow } from "@/store/useStudentStore";

export const ManageStudentsPage: React.FC = () => {
  const { students, addStudent } = useStudentStore();
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");

  const handleProvision = (e: React.FormEvent) => {
    e.preventDefault();
    if (!name.trim() || !email.trim()) return;
    addStudent({ name, email });
    setName("");
    setEmail("");
    setIsModalOpen(false);
  };

  const columns: Column<StudentRow>[] = [
    { key: "id", title: "Student ID", sortable: true, render: (item) => <span className="font-mono text-xs text-indigo-400">{item.id}</span> },
    { key: "name", title: "Full Name", sortable: true, render: (item) => (
      <div>
        <div className="font-bold text-slate-900 dark:text-white">{item.name}</div>
        <div className="text-xs text-slate-400">{item.email}</div>
      </div>
    )},
    { key: "twinId", title: "Learning Profile", sortable: true, render: (item) => <Badge variant="purple" size="sm">{item.twinId}</Badge> },
    { key: "health", title: "Twin Health", sortable: true, render: (item) => (
      <span className={`font-mono font-bold ${item.health >= 90 ? "text-emerald-400" : "text-amber-400"}`}>
        {item.health}/100
      </span>
    )},
    { key: "courses", title: "Enrolled", sortable: true, render: (item) => <span className="text-slate-600 dark:text-slate-300">{item.courses} Courses</span> },
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
      <div className="flex flex-col md:flex-row md:items-end justify-between gap-4 border-b border-slate-200 dark:border-obsidian-600 pb-6">
        <div>
          <Badge variant="danger" size="sm">Admin Management</Badge>
          <h1 className="text-3xl font-extrabold text-slate-900 dark:text-white mt-1">Student Accounts & Learning Profiles</h1>
          <p className="text-sm text-slate-400 mt-1">Manage enrolled student profiles, inspect cognitive health graphs, and audit licenses.</p>
        </div>
        <Button size="md" leftIcon={<UserPlus className="w-4 h-4" />} onClick={() => setIsModalOpen(true)}>
          Provision New Student Account
        </Button>
      </div>

      <Card variant="default" className="p-6">
        <DataTable
          data={students}
          columns={columns}
          searchKey="name"
          searchPlaceholder="Search students by name or email..."
          emptyMessage="No student accounts enrolled yet. Provision new student accounts to populate Learning Profiles."
        />
      </Card>

      <Modal isOpen={isModalOpen} onClose={() => setIsModalOpen(false)} title="Provision Student Account">
        <form onSubmit={handleProvision} className="space-y-4 text-slate-600 dark:text-slate-300">
          <Input
            label="Full Name"
            placeholder="Enter student full name"
            value={name}
            onChange={(e) => setName(e.target.value)}
            required
          />
          <Input
            label="Enterprise Email"
            type="email"
            placeholder="student@university.edu"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
          <div className="flex justify-end gap-3 pt-4">
            <Button type="button" variant="ghost" onClick={() => setIsModalOpen(false)}>Cancel</Button>
            <Button type="submit" variant="primary">Provision & Seed Twin</Button>
          </div>
        </form>
      </Modal>
    </div>
  );
};
