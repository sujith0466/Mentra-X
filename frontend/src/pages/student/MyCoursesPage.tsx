import React from "react";
import { Link } from "react-router-dom";
import { BookOpen, Play, CheckCircle2, Award, Clock } from "lucide-react";
import { Card } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { Badge } from "@/components/ui/Badge";
import { LearningProgress } from "@/components/widgets/LearningProgress";

export const MyCoursesPage: React.FC = () => {
  const myCourses = [
    { id: "ai-101", title: "Advanced Agentic Coding & Orchestration", category: "AI & Machine Learning", completed: 8, total: 12, status: "In Progress", grade: "A (94%)" },
    { id: "cs-202", title: "Enterprise Cloud Architecture & Distributed Systems", category: "Cloud & Systems", completed: 5, total: 8, status: "In Progress", grade: "A- (91%)" },
    { id: "ml-303", title: "Vector Memory Systems & Qdrant Engineering", category: "AI & Machine Learning", completed: 9, total: 10, status: "Almost Complete", grade: "A+ (98%)" },
    { id: "sec-404", title: "AI Safety & Enkrypt Governance Layer Implementation", category: "Security & Governance", completed: 6, total: 6, status: "Completed", grade: "A+ (100%)" },
  ];

  return (
    <div className="space-y-8 py-6">
      <div className="flex flex-col md:flex-row md:items-end justify-between gap-4 border-b border-obsidian-600 pb-6">
        <div>
          <h1 className="text-3xl font-extrabold text-white">My Enrolled Courses</h1>
          <p className="text-sm text-slate-400 mt-1">Manage your active learning paths and syllabus completion progress.</p>
        </div>
        <Link to="/courses">
          <Button size="md" variant="outline">Browse More Courses</Button>
        </Link>
      </div>

      <div className="space-y-6">
        {myCourses.map((course) => (
          <Card key={course.id} variant="interactive" className="p-6">
            <div className="grid grid-cols-1 md:grid-cols-4 gap-6 items-center">
              <div className="md:col-span-2 space-y-2">
                <div className="flex items-center space-x-2">
                  <Badge variant="purple" size="sm">{course.category}</Badge>
                  <Badge variant={course.status === "Completed" ? "success" : "primary"} size="sm">{course.status}</Badge>
                </div>
                <h3 className="text-lg font-bold text-white">{course.title}</h3>
                <div className="flex items-center space-x-4 text-xs text-slate-400">
                  <span className="flex items-center gap-1"><Clock className="w-3.5 h-3.5" /> Enrolled Semester 1</span>
                  <span className="flex items-center gap-1 text-emerald-400 font-semibold"><Award className="w-3.5 h-3.5" /> Current Grade: {course.grade}</span>
                </div>
              </div>

              <div className="md:col-span-1">
                <LearningProgress
                  courseTitle={course.title}
                  completedModules={course.completed}
                  totalModules={course.total}
                  estimatedTimeLeft={course.status === "Completed" ? "Certificate Awarded" : "Active Lab"}
                />
              </div>

              <div className="md:col-span-1 flex justify-end">
                {course.status === "Completed" ? (
                  <Button size="md" variant="outline" leftIcon={<CheckCircle2 className="w-4 h-4 text-emerald-400" />}>
                    View Certificate
                  </Button>
                ) : (
                  <Link to={`/student/course/${course.id}`}>
                    <Button size="md" leftIcon={<Play className="w-4 h-4 fill-current" />}>
                      Resume Lesson
                    </Button>
                  </Link>
                )}
              </div>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
};
