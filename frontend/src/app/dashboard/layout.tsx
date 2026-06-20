"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";

import { useAnalysis } from "@/context/AnalysisContext";
import DashboardSidebar from "@/components/DashboardSidebar";

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const { analysis } = useAnalysis();
  const router = useRouter();

  useEffect(() => {
    if (!analysis) {
      router.replace("/");
    }
  }, [analysis, router]);

  if (!analysis) {
    return (
      <main className="flex min-h-screen items-center justify-center bg-slate-950 text-slate-200">
        <p className="text-slate-400">Loading...</p>
      </main>
    );
  }

  return (
    <main className="min-h-screen bg-gradient-to-b from-slate-950 via-slate-900 to-slate-950 text-slate-100">
      <DashboardSidebar />

      <div className="pt-20 md:pl-72 md:pt-0">
        <div className="mx-auto max-w-7xl p-6 md:p-8">
          {children}
        </div>
      </div>
    </main>
  );
}