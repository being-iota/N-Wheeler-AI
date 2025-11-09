import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'N-Wheeler AI',
  description: 'Intelligent Vehicle Maintenance System with Multi-Agent AI',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}

