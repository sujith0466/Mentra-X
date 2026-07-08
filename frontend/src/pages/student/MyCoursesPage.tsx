import React from "react";
import { Link } from "react-router-dom";
import { BookOpen, Play, CheckCircle2, Award, Clock, Sparkles } from "lucide-react";
import { motion } from "framer-motion";
import { Card } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { Badge } from "@/components/ui/Badge";
import { LearningProgress } from "@/components/widgets/LearningProgress";

export const MyCoursesPage: React.FC = () => {
  const myCourses = [
    { id: "ai-101", title: "Advanced Agentic Coding & Orchestration", category: "AI & Machine Learning", completed: 8, total: 12, status: "In Progress", grade: "A (94%)" },
    { id: "cs-202", title: "Cloud Architecture & Distributed Systems", category: "Cloud & Systems", completed: 5, total: 8, status: "In Progress", grade: "A- (91%)" },
    { id: "ml-303", title: "Natural Language Processing", category: "AI & Machine Learning", completed: 9, total: 10, status: "Almost Complete", grade: "A+ (98%)" },
    { id: "sec-404", title: "AI Safety & Governance", category: "Security & Governance", completed: 6, total: 6, status: "Completed", grade: "A+ (100%)" },
  ];

  return (
    <div className="space-y-8 py-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-end justify-between gap-4 border-b border-slate-200 dark:border-obsidian-600 pb-6">
        <div>
          <h1 className="text-3xl font-extrabold text-slate-900 dark:text-white">My Courses</h1>
          <p className="text-sm text-slate-500 dark:text-slate-400 mt-1">
            Track your enrolled courses, grades, and module completion.
          </p>
        </div>
        <Link to="/courses">
          <Button size="md" variant="outline" leftIcon={<BookOpen className="w-4 h-4" />}>
            Browse More Courses
          </Button>
        </Link>
      </div>

      {/* Course Cards */}
      {myCourses.length === 0 ? (
        <Card variant="glass" className="p-16 text-center space-y-5">
          <div className="w-16 h-16 rounded-2xl bg-indigo-500/10 border border-indigo-500/20 flex items-center justify-center mx-auto">
            <BookOpen className="w-8 h-8 text-indigo-400" />
          </div>
          <div className="space-y-2">
            <h3 className="text-xl font-bold text-slate-900 dark:text-white">No courses enrolled yet</h3>
            <p className="text-sm text-slate-500 dark:text-slate-400 max-w-sm mx-auto">
              Browse the course catalogue and enrol in your first course to start learning.
            </p>
          </div>
          <Link to="/courses">
            <Button variant="primary" className="px-8">
              <Sparkles className="w-4 h-4 mr-2" />
              Explore Courses
            </Button>
          </Link>
        </Card>
      ) : (
        <div className="space-y-5">
          {myCourses.map((course, idx) => {
            const pct = Math.round((course.completed / course.total) * 100);
            return (
              <motion.div
                key={course.id}
                initial={{ opacity: 0, y: 8 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: idx * 0.06 }}
              >
                <Card
                  variant="interactive"
                  className="p-6 hover:-translate-y-0.5 hover:shadow-md transition-all duration-200"
                >
                  <div className="grid grid-cols-1 md:grid-cols-4 gap-6 items-center">
                    {/* Course Info */}
                    <div className="md:col-span-2 space-y-2.5">
                      <div className="flex flex-wrap items-center gap-2">
                        <Badge variant="purple" size="sm">{course.category}</Badge>
                        <Badge
                          variant={course.status === "Completed" ? "success" : course.status === "Almost Complete" ? "warning" : "primary"}
                          size="sm"
                        >
                          {course.status}
                        </Badge>
                      </div>
                      <h3 className="text-lg font-bold text-slate-900 dark:text-white leading-snug">{course.title}</h3>
                      <div className="flex flex-wrap items-center gap-4 text-xs text-slate-500 dark:text-slate-400">
                        <span className="flex items-center gap-1.5">
                          <Clock className="w-3.5 h-3.5" />
                          Semester 1
                        </span>
                        <span className="flex items-center gap-1.5 text-emerald-500 font-semibold">
                          <Award className="w-3.5 h-3.5" />
                          Grade: {course.grade}
                        </span>
                      </div>
                    </div>

                    {/* Progress */}
                    <div className="md:col-span-1 space-y-2">
                      <div className="flex justify-between items-center text-xs text-slate-500 dark:text-slate-400">
                        <span>Progress</span>
                        <span className="font-semibold text-slate-700 dark:text-slate-300">{course.completed}/{course.total} modules</span>
                      </div>
                      <div className="h-2 bg-slate-100 dark:bg-obsidian-900 rounded-full overflow-hidden">
                        <motion.div
                          className={`h-full rounded-full ${
                            course.status === "Completed"
                              ? "bg-emerald-400"
                              : "bg-gradient-to-r from-indigo-500 to-cyan-400"
                          }`}
                          initial={{ width: 0 }}
                          animate={{ width: `${pct}%` }}
                          transition={{ duration: 0.7, delay: idx * 0.1, ease: "easeOut" }}
                        />
                      </div>
                      <p className="text-xs text-slate-400 text-right font-medium">{pct}% complete</p>
                    </div>

                    {/* Action Button */}
                    <div className="md:col-span-1 flex justify-end">
                      {course.status === "Completed" ? (
                        <Button size="md" variant="outline" leftIcon={<CheckCircle2 className="w-4 h-4 text-emerald-400" />}>
                          View Certificate
                        </Button>
                      ) : (
                        <Link to={`/student/course/${course.id}`}>
                          <Button size="md" leftIcon={<Play className="w-4 h-4 fill-current" />}>
                            Resume
                          </Button>
                        </Link>
                      )}
                    </div>
                  </div>
                </Card>
              </motion.div>
            );
          })}
        </div>
      )}
    </div>
  );
};
