"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { Menu, X, User, IndianRupee, Briefcase, Map } from "lucide-react";
import { useState } from "react";

const navItems = [
  {
    label: "Candidate Profile",
    href: "/dashboard",
    icon: User,
  },
  {
    label: "Salary Prediction",
    href: "/dashboard/salary",
    icon: IndianRupee,
  },
  {
    label: "Job Recommendations",
    href: "/dashboard/jobs",
    icon: Briefcase,
  },
  {
    label: "Career Roadmap",
    href: "/dashboard/roadmap",
    icon: Map,
  },
];

export default function DashboardSidebar() {
  const [isOpen, setIsOpen] = useState(false);
  const pathname = usePathname();

  return (
    <>
      <div className="fixed left-0 right-0 top-0 z-40 flex items-center justify-between border-b border-slate-800 bg-slate-950 px-4 py-3 md:hidden">
        <h2 className="text-lg font-bold text-white">
          CareerIQ
        </h2>

        <button
          onClick={() => setIsOpen(true)}
          className="rounded-lg border border-slate-700 p-2 text-slate-200"
        >
          <Menu size={20} />
        </button>
      </div>

      {isOpen && (
        <div
          onClick={() => setIsOpen(false)}
          className="fixed inset-0 z-40 bg-black/60 md:hidden"
        />
      )}

      <aside
        className={`fixed left-0 top-0 z-50 h-screen w-72 border-r border-slate-800 bg-slate-950 p-5 transition-transform duration-300 md:translate-x-0 ${
          isOpen ? "translate-x-0" : "-translate-x-full"
        }`}
      >
        <div className="mb-8 flex items-center justify-between">
          <div>
            <h2 className="text-xl font-bold text-white">
              CareerIQ
            </h2>
            <p className="mt-1 text-xs text-slate-500">
              AI Career Intelligence
            </p>
          </div>

          <button
            onClick={() => setIsOpen(false)}
            className="rounded-lg border border-slate-700 p-2 text-slate-300 md:hidden"
          >
            <X size={18} />
          </button>
        </div>

        <nav className="space-y-2">
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = pathname === item.href;

            return (
              <Link
                key={item.href}
                href={item.href}
                onClick={() => setIsOpen(false)}
                className={`flex items-center gap-3 rounded-xl px-4 py-3 text-sm font-medium transition ${
                  isActive
                    ? "bg-emerald-500/10 text-emerald-400"
                    : "text-slate-300 hover:bg-slate-900 hover:text-white"
                }`}
              >
                <Icon size={18} />
                {item.label}
              </Link>
            );
          })}
        </nav>

      </aside>
    </>
  );
}