import './globals.css'
import type { Metadata } from 'next'
import { Inter } from 'next/font/google'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'Review Analysis App',
  description: 'Sentiment & Aspect-Based Review Analysis Web App',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <div className="min-h-screen flex flex-col">
          <header className="bg-primary-700 text-white shadow-md">
            <div className="container mx-auto px-4 py-4 flex justify-between items-center">
              <h1 className="text-2xl font-bold">Review Analysis</h1>
              <nav>
                <ul className="flex space-x-6">
                  <li><a href="/" className="hover:text-primary-200 transition-colors">Home</a></li>
                  <li><a href="/dashboard" className="hover:text-primary-200 transition-colors">Dashboard</a></li>
                  <li><a href="/reviews" className="hover:text-primary-200 transition-colors">Reviews</a></li>
                </ul>
              </nav>
            </div>
          </header>
          
          <main className="flex-grow container mx-auto px-4 py-8">
            {children}
          </main>
          
          <footer className="bg-gray-100 border-t border-gray-200">
            <div className="container mx-auto px-4 py-6">
              <p className="text-center text-gray-600">
                &copy; {new Date().getFullYear()} Review Analysis App. All rights reserved.
              </p>
            </div>
          </footer>
        </div>
      </body>
    </html>
  )
}
