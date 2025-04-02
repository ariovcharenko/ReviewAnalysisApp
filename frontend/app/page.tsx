import Link from 'next/link'
import { FaChartLine, FaSearch, FaFileAlt } from 'react-icons/fa'

export default function Home() {
  return (
    <div className="space-y-12">
      <section className="text-center py-12">
        <h1 className="text-4xl font-bold mb-4">Sentiment & Aspect-Based Review Analysis</h1>
        <p className="text-xl text-gray-600 max-w-3xl mx-auto">
          Analyze product reviews semantically, extract key aspects, and detect sentiment to gain valuable insights.
        </p>
        <div className="mt-8">
          <Link href="/analyze" className="btn-primary mr-4">
            Analyze Reviews
          </Link>
          <Link href="/dashboard" className="btn-outline">
            View Dashboard
          </Link>
        </div>
      </section>

      <section className="grid md:grid-cols-3 gap-8">
        <div className="card text-center">
          <div className="flex justify-center mb-4">
            <FaSearch className="text-5xl text-primary-600" />
          </div>
          <h2 className="text-2xl font-bold mb-2">Sentiment Analysis</h2>
          <p className="text-gray-600">
            Detect the overall sentiment of reviews as positive, neutral, or negative using advanced BERT models.
          </p>
        </div>

        <div className="card text-center">
          <div className="flex justify-center mb-4">
            <FaFileAlt className="text-5xl text-primary-600" />
          </div>
          <h2 className="text-2xl font-bold mb-2">Aspect Extraction</h2>
          <p className="text-gray-600">
            Identify key aspects mentioned in reviews (battery, camera, design, etc.) and their associated sentiment.
          </p>
        </div>

        <div className="card text-center">
          <div className="flex justify-center mb-4">
            <FaChartLine className="text-5xl text-primary-600" />
          </div>
          <h2 className="text-2xl font-bold mb-2">Trend Analysis</h2>
          <p className="text-gray-600">
            Track sentiment changes over time and identify recurring themes in customer feedback.
          </p>
        </div>
      </section>

      <section className="bg-gray-50 p-8 rounded-lg">
        <h2 className="text-2xl font-bold mb-4">How It Works</h2>
        <ol className="list-decimal list-inside space-y-4 ml-4">
          <li className="text-lg">
            <span className="font-medium">Input your reviews</span> - Enter text directly or upload a CSV file with multiple reviews.
          </li>
          <li className="text-lg">
            <span className="font-medium">Analyze the content</span> - Our AI models process the text to extract sentiment and key aspects.
          </li>
          <li className="text-lg">
            <span className="font-medium">View the results</span> - See overall sentiment, aspect-based analysis, and AI-generated summaries.
          </li>
          <li className="text-lg">
            <span className="font-medium">Track trends over time</span> - Monitor how sentiment and key aspects change across reviews.
          </li>
        </ol>
      </section>

      <section className="text-center">
        <h2 className="text-2xl font-bold mb-4">Ready to analyze your reviews?</h2>
        <Link href="/analyze" className="btn-primary">
          Get Started
        </Link>
      </section>
    </div>
  )
}
