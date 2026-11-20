import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Student Job Application Agent",
  description: "AI-powered Werkstudent/Praktikum job search and application assistant",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="min-h-screen bg-slate-50 text-slate-900">{children}</body>
    </html>
  );
}
