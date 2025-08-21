import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Ethic Companion V2 - Assistente com Memória Inteligente",
  description: "Chat inteligente com memória persistente usando FastAPI, Weaviate e Google Gemini",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="pt">
      <body className="antialiased">
        {children}
      </body>
    </html>
  );
}
