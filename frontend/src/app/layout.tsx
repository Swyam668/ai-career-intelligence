// for seo
import { Metadata } from "next";
import "./globals.css";

import { AnalysisProvider } from "@/context/AnalysisContext";
// seo
export const metadata: Metadata = {
  title: "AI Career Intelligence",
  description: "Resume Analysis Platform",
};

export default function RootLayout({
  children,
  // for reading only, not modifying
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>
        <AnalysisProvider>
          {children}
        </AnalysisProvider>
      </body>
    </html>
  );
}