import React, { useState } from "react";
import { ChevronDown, ChevronUp, Search } from "lucide-react";
import { Input } from "@/components/ui/Input";

export interface Column<T> {
  key: keyof T | string;
  title: string;
  render?: (item: T, index: number) => React.ReactNode;
  sortable?: boolean;
}

export interface DataTableProps<T> {
  data: T[];
  columns: Column<T>[];
  searchKey?: keyof T;
  searchPlaceholder?: string;
  emptyMessage?: string;
}

export function DataTable<T extends Record<string, any>>({
  data,
  columns,
  searchKey,
  searchPlaceholder = "Search...",
  emptyMessage = "No results found.",
}: DataTableProps<T>) {
  const [searchTerm, setSearchTerm] = useState("");
  const [sortColumn, setSortColumn] = useState<string | null>(null);
  const [sortDirection, setSortDirection] = useState<"asc" | "desc">("asc");

  const handleSort = (key: string) => {
    if (sortColumn === key) {
      setSortDirection(sortDirection === "asc" ? "desc" : "asc");
    } else {
      setSortColumn(key);
      setSortDirection("asc");
    }
  };

  const filteredData = data.filter((item) => {
    if (!searchKey || !searchTerm) return true;
    const val = item[searchKey as string];
    if (val == null) return false;
    return String(val).toLowerCase().includes(searchTerm.toLowerCase());
  });

  const sortedData = [...filteredData].sort((a, b) => {
    if (!sortColumn) return 0;
    const valA = a[sortColumn];
    const valB = b[sortColumn];
    if (valA === valB) return 0;
    if (valA == null) return 1;
    if (valB == null) return -1;
    if (valA < valB) return sortDirection === "asc" ? -1 : 1;
    return sortDirection === "asc" ? 1 : -1;
  });

  return (
    <div className="w-full space-y-4">
      {searchKey && (
        <div className="max-w-xs">
          <Input
            placeholder={searchPlaceholder}
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            leftIcon={<Search className="w-4 h-4" />}
          />
        </div>
      )}
      <div className="w-full overflow-x-auto rounded-xl border border-obsidian-600 bg-obsidian-800">
        <table className="w-full text-left border-collapse">
          <thead>
            <tr className="border-b border-obsidian-600 bg-obsidian-900/50">
              {columns.map((col) => (
                <th
                  key={String(col.key)}
                  onClick={() => col.sortable && handleSort(String(col.key))}
                  className={`px-6 py-3.5 text-xs font-semibold uppercase tracking-wider text-slate-300 ${
                    col.sortable ? "cursor-pointer select-none hover:text-white" : ""
                  }`}
                >
                  <div className="flex items-center space-x-1.5">
                    <span>{col.title}</span>
                    {col.sortable && sortColumn === col.key && (
                      <span className="text-primary-500">
                        {sortDirection === "asc" ? (
                          <ChevronUp className="w-3.5 h-3.5" />
                        ) : (
                          <ChevronDown className="w-3.5 h-3.5" />
                        )}
                      </span>
                    )}
                  </div>
                </th>
              ))}
            </tr>
          </thead>
          <tbody className="divide-y divide-obsidian-600/50">
            {sortedData.length > 0 ? (
              sortedData.map((item, idx) => (
                <tr
                  key={idx}
                  className="hover:bg-white/[0.02] transition-colors"
                >
                  {columns.map((col) => (
                    <td key={String(col.key)} className="px-6 py-4 text-sm text-slate-200">
                      {col.render
                        ? col.render(item, idx)
                        : item[String(col.key)] !== undefined
                        ? String(item[String(col.key)])
                        : "-"}
                    </td>
                  ))}
                </tr>
              ))
            ) : (
              <tr>
                <td
                  colSpan={columns.length}
                  className="px-6 py-12 text-center text-sm text-slate-500"
                >
                  {emptyMessage}
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
