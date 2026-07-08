import React, { useState } from "react";
import { BookOpen, Plus, Search, Sparkles, Tag, Trash2, Edit3, Save, CheckCircle2, FileText } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";
import { Card } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { Input } from "@/components/ui/Input";
import { Badge } from "@/components/ui/Badge";

interface Note {
  id: string;
  title: string;
  course: string;
  content: string;
  tags: string[];
  lastUpdated: string;
}

export const NotesPage: React.FC = () => {
  const [notes, setNotes] = useState<Note[]>([
    {
      id: "1",
      title: "Transformer Attention Mechanics & Scaled Dot-Product",
      course: "CS-401: Advanced Neural Architectures",
      content: "Attention(Q, K, V) = softmax((Q K^T) / sqrt(d_k)) V.\n\nKey takeaway: Dividing by sqrt(d_k) prevents the dot-product values from growing too large, which would push softmax gradients into regions with extremely small gradients (vanishing gradients).",
      tags: ["AI", "Transformers", "Math"],
      lastUpdated: "2 hours ago",
    },
    {
      id: "2",
      title: "Graph Indexing & Distance Metrics",
      course: "CS-305: Database Systems & Algorithms",
      content: "Hierarchical Navigable Small World (HNSW) graphs construct multi-layer skip lists for high-dimensional search. Cosine distance is optimal for normalized data, while Euclidean distance is sensitive to magnitude.",
      tags: ["Indexing", "Algorithms", "Databases"],
      lastUpdated: "Yesterday",
    },
    {
      id: "3",
      title: "AI Safety: Prompt Injection Defense Strategies",
      course: "SEC-502: AI Safety & Governance",
      content: "Never rely solely on system prompt instructions for security. Implement external immutable validation layers that evaluate semantic intent before prompt dispatch.",
      tags: ["Security", "AI Safety", "Governance"],
      lastUpdated: "3 days ago",
    },
  ]);

  const [activeNoteId, setActiveNoteId] = useState<string>("1");
  const [searchQuery, setSearchQuery] = useState("");
  const [isEditing, setIsEditing] = useState(false);
  const [editTitle, setEditTitle] = useState("");
  const [editContent, setEditContent] = useState("");
  const [summarizing, setSummarizing] = useState(false);

  const activeNote = notes.find((n) => n.id === activeNoteId) || notes[0];

  const handleSelectNote = (note: Note) => {
    setActiveNoteId(note.id);
    setIsEditing(false);
    setEditTitle(note.title);
    setEditContent(note.content);
  };

  const handleStartEdit = () => {
    setEditTitle(activeNote.title);
    setEditContent(activeNote.content);
    setIsEditing(true);
  };

  const handleSaveEdit = () => {
    setNotes((prev) =>
      prev.map((n) => (n.id === activeNoteId ? { ...n, title: editTitle, content: editContent, lastUpdated: "Just now" } : n))
    );
    setIsEditing(false);
  };

  const handleCreateNew = () => {
    const newNote: Note = {
      id: Date.now().toString(),
      title: "New Untitled Note",
      course: "CS-101: General Computing",
      content: "Start typing your notes here...",
      tags: ["Draft"],
      lastUpdated: "Just now",
    };
    setNotes([newNote, ...notes]);
    setActiveNoteId(newNote.id);
    setEditTitle(newNote.title);
    setEditContent(newNote.content);
    setIsEditing(true);
  };

  const handleDelete = (id: string) => {
    const filtered = notes.filter((n) => n.id !== id);
    setNotes(filtered);
    if (activeNoteId === id && filtered.length > 0) {
      setActiveNoteId(filtered[0].id);
    }
  };

  const handleAISummarize = () => {
    setSummarizing(true);
    setTimeout(() => {
      setSummarizing(false);
      alert("AI Summary:\n" + activeNote.content.substring(0, 120) + "...\n\n[Saved to your notes]");
    }, 1200);
  };

  const filteredNotes = notes.filter((n) =>
    n.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
    n.content.toLowerCase().includes(searchQuery.toLowerCase()) ||
    n.tags.some((t) => t.toLowerCase().includes(searchQuery.toLowerCase()))
  );

  return (
    <div className="max-w-7xl mx-auto py-8 px-4 sm:px-6 space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-200 dark:border-white/10 pb-6">
        <div>
          <Badge variant="info" className="mb-2">
            <BookOpen className="w-3.5 h-3.5 mr-1.5 inline text-indigo-400" />
            Personal Knowledge Base
          </Badge>
          <h1 className="text-3xl font-extrabold text-slate-900 dark:text-white">My Notes</h1>
          <p className="text-sm text-slate-500 dark:text-slate-400 mt-1">
            Organise your lecture notes, tag topics, and get instant AI summaries.
          </p>
        </div>
        <Button variant="primary" onClick={handleCreateNew} className="px-5 py-2.5 self-start sm:self-center">
          <Plus className="w-4 h-4 mr-2" />
          New Note
        </Button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 items-start">
        {/* Left Column: Notes List & Search */}
        <div className="space-y-4">
          {/* Search */}
          <div className="relative">
            <Search className="w-4 h-4 text-slate-400 absolute left-3.5 top-3.5 pointer-events-none" />
            <Input
              placeholder="Search notes or tags..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="pl-10 w-full"
            />
          </div>

          {/* Notes List */}
          <div className="space-y-2.5 max-h-[650px] overflow-y-auto pr-1">
            {filteredNotes.length === 0 ? (
              <Card variant="glass" className="p-8 text-center space-y-3">
                <FileText className="w-8 h-8 text-slate-300 dark:text-obsidian-600 mx-auto" />
                <p className="text-sm font-medium text-slate-500 dark:text-slate-400">
                  {searchQuery ? "No notes match your search." : "No notes yet."}
                </p>
                {!searchQuery && (
                  <Button variant="secondary" onClick={handleCreateNew} className="text-xs">
                    <Plus className="w-3.5 h-3.5 mr-1" />
                    Create your first note
                  </Button>
                )}
              </Card>
            ) : (
              filteredNotes.map((note) => {
                const isActive = note.id === activeNoteId;
                return (
                  <Card
                    key={note.id}
                    variant={isActive ? "glow" : "default"}
                    onClick={() => handleSelectNote(note)}
                    className={`p-4 cursor-pointer transition-all duration-200 border ${
                      isActive
                        ? "border-indigo-500/50 shadow-md"
                        : "border-slate-200 dark:border-white/5 hover:border-indigo-300 dark:hover:border-white/15 hover:-translate-y-0.5 hover:shadow-sm"
                    }`}
                  >
                    <div className="flex justify-between items-start gap-2 mb-1.5">
                      <h4 className="text-sm font-bold text-slate-900 dark:text-white line-clamp-1 leading-snug">{note.title}</h4>
                      <button
                        onClick={(e) => { e.stopPropagation(); handleDelete(note.id); }}
                        className="text-slate-400 hover:text-red-400 transition-colors p-0.5 shrink-0"
                      >
                        <Trash2 className="w-3.5 h-3.5" />
                      </button>
                    </div>
                    <p className="text-xs text-indigo-400 font-semibold mb-2">{note.course}</p>
                    <p className="text-xs text-slate-400 line-clamp-2 mb-3 leading-relaxed">{note.content}</p>
                    <div className="flex justify-between items-center">
                      <div className="flex flex-wrap gap-1">
                        {note.tags.map((t) => (
                          <span
                            key={t}
                            className="px-1.5 py-0.5 rounded text-[10px] bg-slate-100 dark:bg-obsidian-900 text-slate-500 dark:text-slate-400 border border-slate-200 dark:border-white/5"
                          >
                            #{t}
                          </span>
                        ))}
                      </div>
                      <span className="text-[10px] text-slate-400 shrink-0 ml-2">{note.lastUpdated}</span>
                    </div>
                  </Card>
                );
              })
            )}
          </div>
        </div>

        {/* Right Column: Note Editor / Viewer */}
        <div className="lg:col-span-2">
          <AnimatePresence mode="wait">
            {activeNote ? (
              <motion.div
                key={activeNoteId}
                initial={{ opacity: 0, y: 6 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0 }}
                transition={{ duration: 0.18 }}
              >
                <Card variant="default" className="p-8 space-y-6 min-h-[600px] flex flex-col justify-between">
                  <div className="space-y-5">
                    {/* Note Header */}
                    <div className="flex flex-col sm:flex-row sm:items-start justify-between gap-4 pb-5 border-b border-slate-200 dark:border-white/10">
                      {isEditing ? (
                        <Input
                          value={editTitle}
                          onChange={(e) => setEditTitle(e.target.value)}
                          className="text-lg font-bold w-full"
                          placeholder="Note title..."
                        />
                      ) : (
                        <div>
                          <Badge variant="success" className="mb-1.5">{activeNote.course}</Badge>
                          <h2 className="text-2xl font-bold text-slate-900 dark:text-white leading-snug">{activeNote.title}</h2>
                        </div>
                      )}

                      <div className="flex items-center gap-2 shrink-0">
                        {!isEditing && (
                          <Button
                            variant="secondary"
                            onClick={handleAISummarize}
                            disabled={summarizing}
                            className="text-xs py-2"
                          >
                            <Sparkles className="w-3.5 h-3.5 mr-1.5 text-cyan-400" />
                            {summarizing ? "AI Summarizing..." : "AI Summary"}
                          </Button>
                        )}
                        {isEditing ? (
                          <Button variant="primary" onClick={handleSaveEdit} className="text-xs py-2">
                            <Save className="w-3.5 h-3.5 mr-1.5" />
                            Save Note
                          </Button>
                        ) : (
                          <Button variant="secondary" onClick={handleStartEdit} className="text-xs py-2">
                            <Edit3 className="w-3.5 h-3.5 mr-1.5" />
                            Edit
                          </Button>
                        )}
                      </div>
                    </div>

                    {/* Content */}
                    {isEditing ? (
                      <textarea
                        rows={16}
                        value={editContent}
                        onChange={(e) => setEditContent(e.target.value)}
                        className="w-full bg-slate-50 dark:bg-obsidian-900 border border-slate-200 dark:border-white/10 rounded-xl p-4 text-sm text-slate-900 dark:text-white font-mono placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-indigo-500 resize-none"
                        placeholder="Write your notes here..."
                      />
                    ) : (
                      <div className="prose dark:prose-invert max-w-none text-sm text-slate-600 dark:text-slate-300 whitespace-pre-line leading-relaxed font-sans pt-1">
                        {activeNote.content}
                      </div>
                    )}
                  </div>

                  {/* Footer */}
                  <div className="pt-5 border-t border-slate-200 dark:border-white/10 flex items-center justify-between text-xs text-slate-400">
                    <div className="flex items-center gap-2">
                      <Tag className="w-3.5 h-3.5 text-indigo-400" />
                      <span>{activeNote.tags.join(", ")}</span>
                    </div>
                    <span className="inline-flex items-center gap-1 text-emerald-500 font-semibold">
                      <CheckCircle2 className="w-3.5 h-3.5" />
                      Auto-saved
                    </span>
                  </div>
                </Card>
              </motion.div>
            ) : (
              <Card variant="glass" className="p-16 text-center space-y-4">
                <FileText className="w-12 h-12 text-slate-300 dark:text-obsidian-600 mx-auto" />
                <p className="text-sm font-medium text-slate-500 dark:text-slate-400">Select a note from the list or create a new one.</p>
              </Card>
            )}
          </AnimatePresence>
        </div>
      </div>
    </div>
  );
};
