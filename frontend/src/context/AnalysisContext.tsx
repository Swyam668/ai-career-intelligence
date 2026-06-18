"use client";

import {
  createContext,
  useContext,
  useState,
  ReactNode,
} from "react";

import { AnalysisResponse } from "@/types";

interface AnalysisContextType {
  analysis: AnalysisResponse | null;
  setAnalysis: (
    analysis: AnalysisResponse | null
  ) => void;
}

const AnalysisContext =
  createContext<AnalysisContextType | null>(
    null
  );

export function AnalysisProvider({
  children,
}: {
  children: ReactNode;
}) {
  const [analysis, setAnalysis] =
    useState<AnalysisResponse | null>(null);

  return (
    <AnalysisContext.Provider
      value={{
        analysis,
        setAnalysis,
      }}
    >
      {children}
    </AnalysisContext.Provider>
  );
}

// prevents us to use useAnalysis() outside provider
export function useAnalysis() {
  const context =
    useContext(AnalysisContext);

  if (!context) {
    throw new Error(
      "useAnalysis must be used inside AnalysisProvider"
    );
  }

  return context;
}