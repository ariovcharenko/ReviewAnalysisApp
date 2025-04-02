'use client'

import { useState, useEffect } from 'react'
import { useSearchParams } from 'next/navigation'
import Link from 'next/link'
import axios from 'axios'
import { FaThumbsUp, FaThumbsDown, FaMinus, FaArrowLeft } from 'react-icons/fa'

// Define types for our analysis results
interface Review {
  id: number
  text: string
  rating?: number
  created_at: string
}

interface SentimentAnalysis {
  id: number
  review_id: number
  sentiment_score: number
  sentiment_label: string
  confidence: number
  created_at: string
}

interface AspectAnalysis {
  id: number
  review_id: number
  aspect: string
  sentiment_score: number
  sentiment_label: string
  confidence: number
  relevant_text: string
  created_at: string
}

interface ReviewSummary {
  id: number
  review_id: number
  summary_text: string
  created_at: string
}

interface AnalysisResult {
  review: Review
  sentiment: SentimentAnalysis
  aspects: AspectAnalysis[]
  summary: ReviewSummary
}

export default function ResultsPage() {
  const searchParams = useSearchParams()
  const reviewId = searchParams.get('id')
  
  const [result, setResult] = useState<AnalysisResult | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState('')
  
  // API base URL - would come from environment variables in a real app
  const API_URL = 'http://localhost:8000/api'
  
  useEffect(() => {
    const fetchResults = async () => {
      if (!reviewId) {
        setError('No review ID provided')
        setIsLoading(false)
        return
      }
      
      try {
        const response = await axios.get(`${API_URL}/reviews/${reviewId}/full-analysis`)
        setResult(response.data)
      } catch (err) {
        console.error('Error fetching analysis results:', err)
        setError('An error occurred while fetching the analysis results')
      } finally {
        setIsLoading(false)
      }
    }
    
    fetchResults()
  }, [reviewId])
  
  // Helper function to get sentiment icon
  const getSentimentIcon = (label: string) => {
    switch (label) {
      case 'positive':
        return <FaThumbsUp className="text-green-500" />
      case 'negative':
        return <FaThumbsDown className="text-red-500" />
      default:
        return <FaMinus className="text-gray-500" />
    }
  }
  
  // Helper function to get sentiment color class
  const getSentimentColorClass = (label: string) => {
    switch (label) {
      case 'positive':
        return 'text-green-600'
      case 'negative':
        return 'text-red-600'
      default:
        return 'text-gray-600'
    }
  }
  
  if (isLoading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary-600"></div>
      </div>
    )
  }
  
  if (error) {
    return (
      <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
        <p>{error}</p>
        <Link href="/analyze" className="text-primary-600 hover:underline mt-2 inline-block">
          <FaArrowLeft className="inline mr-1" /> Back to Analysis
        </Link>
      </div>
    )
  }
  
  if (!result) {
    return (
      <div className="text-center py-8">
        <p className="text-gray-600">No results found</p>
        <Link href="/analyze" className="text-primary-600 hover:underline mt-2 inline-block">
          <FaArrowLeft className="inline mr-1" /> Back to Analysis
        </Link>
      </div>
    )
  }
  
  return (
    <div className="space-y-8">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold">Analysis Results</h1>
        <Link href="/analyze" className="btn-outline flex items-center">
          <FaArrowLeft className="mr-2" /> Back to Analysis
        </Link>
      </div>
      
      {/* Original Review */}
      <div className="card">
        <h2 className="text-xl font-semibold mb-2">Original Review</h2>
        <p className="text-gray-700 whitespace-pre-line">{result.review.text}</p>
        {result.review.rating && (
          <p className="mt-2 text-gray-600">Rating: {result.review.rating}/5</p>
        )}
      </div>
      
      {/* Summary */}
      <div className="card">
        <h2 className="text-xl font-semibold mb-2">AI-Generated Summary</h2>
        <p className="text-gray-700">{result.summary.summary_text}</p>
      </div>
      
      {/* Overall Sentiment */}
      <div className="card">
        <h2 className="text-xl font-semibold mb-4">Overall Sentiment</h2>
        <div className="flex items-center space-x-4">
          <div className="bg-gray-100 rounded-full p-4">
            {getSentimentIcon(result.sentiment.sentiment_label)}
          </div>
          <div>
            <p className={`text-2xl font-bold ${getSentimentColorClass(result.sentiment.sentiment_label)}`}>
              {result.sentiment.sentiment_label.charAt(0).toUpperCase() + result.sentiment.sentiment_label.slice(1)}
            </p>
            <p className="text-gray-600">
              Score: {result.sentiment.sentiment_score.toFixed(2)} (Confidence: {(result.sentiment.confidence * 100).toFixed(0)}%)
            </p>
          </div>
        </div>
      </div>
      
      {/* Aspect-Based Analysis */}
      <div className="card">
        <h2 className="text-xl font-semibold mb-4">Aspect-Based Analysis</h2>
        {result.aspects.length === 0 ? (
          <p className="text-gray-600">No specific aspects were identified in this review.</p>
        ) : (
          <div className="space-y-4">
            {result.aspects.map((aspect) => (
              <div key={aspect.id} className="border-b border-gray-200 pb-4 last:border-b-0 last:pb-0">
                <div className="flex items-center justify-between">
                  <h3 className="text-lg font-medium capitalize">{aspect.aspect}</h3>
                  <span className={`flex items-center ${getSentimentColorClass(aspect.sentiment_label)}`}>
                    {getSentimentIcon(aspect.sentiment_label)}
                    <span className="ml-1">{aspect.sentiment_label}</span>
                  </span>
                </div>
                <p className="text-gray-700 mt-1">"{aspect.relevant_text}"</p>
              </div>
            ))}
          </div>
        )}
      </div>
      
      {/* Actions */}
      <div className="flex justify-center space-x-4">
        <Link href={`/reviews/${result.review.id}`} className="btn-primary">
          View Full Details
        </Link>
        <Link href="/dashboard" className="btn-outline">
          Go to Dashboard
        </Link>
      </div>
    </div>
  )
}
