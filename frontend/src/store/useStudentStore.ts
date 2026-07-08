import { create } from "zustand";
import { persist } from "zustand/middleware";

export interface StudentRow {
  id: string;
  name: string;
  email: string;
  twinId: string;
  health: number;
  courses: number;
  status: "Active" | "Suspended" | "Syncing";
}

export interface StudentState {
  students: StudentRow[];
  addStudent: (student: Omit<StudentRow, "id" | "twinId" | "health" | "courses" | "status">) => void;
  updateStatus: (id: string, status: "Active" | "Suspended" | "Syncing") => void;
}

export const useStudentStore = create<StudentState>()(
  persist(
    (set) => ({
      students: [],
      addStudent: (studentData) => {
        const id = `STU-${100 + Math.floor(Math.random() * 900)}`;
        const newStudent: StudentRow = {
          ...studentData,
          id,
          twinId: `twin_${id.toLowerCase()}`,
          health: 95,
          courses: 1,
          status: "Active",
        };
        set((state) => ({
          students: [newStudent, ...state.students],
        }));
      },
      updateStatus: (id, status) => {
        set((state) => ({
          students: state.students.map((stu) =>
            stu.id === id ? { ...stu, status } : stu
          ),
        }));
      },
    }),
    {
      name: "mentra-student-storage",
    }
  )
);
