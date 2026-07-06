import React, { useState } from "react";
import { BookOpen, Plus, Search, Sparkles, Tag, Trash2, Edit3, Save, CheckCircle2 } from "lucide-react";
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
      title: "Qdrant HNSW Graph Indexing & Distance Metrics",
      course: "CS-305: Enterprise Vector Databases",
      content: "Hierarchical Navigable Small World (HNSW) graphs construct multi-layer skip lists for high-dimensional vectors. Cosine distance is optimal for normalized embeddings, while Euclidean distance is sensitive to vector magnitude.",
      tags: ["VectorDB", "Qdrant", "Algorithms"],
      lastUpdated: "Yesterday",
    },
    {
      id: "3",
      title: "Enkrypt Layer 6 Prompt Injection Defense Strategies",
      course: "SEC-502: AI Safety & Governance",
      content: "Never rely solely on system prompt instructions for security. Implement external immutable validation layers that evaluate embedding distance and semantic intent before prompt dispatch.",
      tags: ["Security", "Enkrypt", "Governance"],
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
      content: "Start typing your markdown notes here...",
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
      alert("AI Swarm Summary:\n" + activeNote.content.substring(0, 120) + "...\n\n[Synchronized with Qdrant vector memory]");
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
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-white/10 pb-6">
        <div>
          <Badge variant="info" className="mb-2">Cognitive Knowledge Base</Badge>
          <h1 className="text-3xl font-extrabold text-white">Student Notes & Lecture Synthesis</h1>
          <p className="text-sm text-slate-400">Organize academic notes with automatic vector indexing and AI summary swarms.</p>
        </div>
        <Button variant="primary" onClick={handleCreateNew} className="px-5 py-2.5 self-start sm:self-center">
          <Plus className="w-4 h-4 mr-2" />
          Create New Note
        </Button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 items-start">
        {/* Left Column: Notes List & Search */}
        <div className="space-y-4">
          <div className="relative">
            <Search className="w-4 h-4 text-slate-500 absolute left-3.5 top-3.5" />
            <Input
              placeholder="Search notes or tags..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="pl-10 w-full"
            />
          </div>

          <div className="space-y-3 max-h-[650px] overflow-y-auto pr-1">
            {filteredNotes.length === 0 ? (
              <Card variant="glass" className="p-6 text-center text-xs text-slate-400">
                No matching notes found.
              </Card>
            ) : (
              filteredNotes.map((note) => {
                const isActive = note.id === activeNoteId;
                return (
                  <Card
                    key={note.id}
                    variant={isActive ? "glow" : "default"}
                    onClick={() => handleSelectNote(note)}
                    className={`p-4 cursor-pointer transition-all border ${
                      isActive ? "border-indigo-500/50 shadow-md" : "border-white/5 hover:border-white/15"
                    }`}
                  >
                    <div className="flex justify-between items-start gap-2 mb-1">
                      <h4 className="text-sm font-bold text-white line-clamp-1">{note.title}</h4>
                      <button
                        onClick={(e) => { e.stopPropagation(); handleDelete(note.id); }}
                        className="text-slate-500 hover:text-red-400 p-1"
                      >
                        <Trash2 className="w-3.5 h-3.5" />
                      </button>
                    </div>
                    <p className="text-xs text-indigo-400 font-semibold mb-2">{note.course}</p>
                    <p className="text-xs text-slate-400 line-clamp-2 mb-3 font-sans">{note.content}</p>
                    <div className="flex justify-between items-center text-[10px] text-slate-500">
                      <div className="flex gap-1">
                        {note.tags.map((t) => (
                          <span key={t} className="px-1.5 py-0.5 rounded bg-obsidian-900 text-slate-400 border border-white/5">
                            #{t}
                          </span>
                        ))}
                      </div>
                      <span>{note.lastUpdated}</span>
                    </div>
                  </Card>
                );
              })
            )}
          </div>
        </div>

        {/* Right Column: Note Editor / Viewer */}
        <div className="lg:col-span-2">
          {activeNote ? (
            <Card variant="default" className="p-8 space-y-6 min-h-[600px] flex flex-col justify-between">
              <div className="space-y-4">
                <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-4 border-b border-white/10">
                  {isEditing ? (
                    <Input
                      value={editTitle}
                      onChange={(e) => setEditTitle(e.target.value)}
                      className="text-lg font-bold text-white w-full"
                    />
                  ) : (
                    <div>
                      <Badge variant="success" className="mb-1">{activeNote.course}</Badge>
                      <h2 className="text-2xl font-bold text-white">{activeNote.title}</h2>
                    </div>
                  )}

                  <div className="flex items-center gap-2 shrink-0">
                    {!isEditing && (
                      <Button variant="secondary" onClick={handleAISummarize} disabled={summarizing} className="text-xs py-2">
                        <Sparkles className="w-3.5 h-3.5 mr-1.5 text-cyan-400" />
                        {summarizing ? "Synthesizing..." : "AI Swarm Summary"}
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

                {isEditing ? (
                  <textarea
                    rows={16}
                    value={editContent}
                    onChange={(e) => setEditContent(e.target.value)}
                    className="w-full bg-obsidian-900 border border-white/10 rounded-xl p-4 text-sm text-white font-mono placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-indigo-500"
                  />
                ) : (
                  <div className="prose prose-invert max-w-none text-sm text-slate-300 whitespace-pre-line leading-relaxed font-sans pt-2">
                    {activeNote.content}
                  </div>
                )}
              </div>

              <div className="pt-6 border-t border-white/10 flex items-center justify-between text-xs text-slate-400">
                <div className="flex items-center gap-2">
                  <Tag className="w-3.5 h-3.5 text-indigo-400" />
                  <span>Tags: {activeNote.tags.join(", ")}</span>
                </div>
                <span className="inline-flex items-center gap-1 text-emerald-400">
                  <CheckCircle2 className="w-3.5 h-3.5" />
                  Synced with Qdrant Vector DB
                </span>
              </div>
            </Card>
          ) : (
            <Card variant="glass" className="p-12 text-center text-slate-400">
              Select a note from the left sidebar or create a new one.
            </Card>
          )}
        </div>
      </div>
    </div>
  );
};
