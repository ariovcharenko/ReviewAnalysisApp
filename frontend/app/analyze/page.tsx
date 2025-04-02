'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { FaUpload, FaSpinner } from 'react-icons/fa'
import axios from 'axios'

// Define types for our analysis results
interface SentimentResult {
  sentiment_score: number
  sentiment_label: string
  confidence: number
}

interface AspectResult {
  aspect: string
  sentiment_score: number
  sentiment_label: string
  confidence: number
  relevant_text: string
}

interface AnalysisResult {
  sentiment: SentimentResult
  aspects: AspectResult[]
  summary: string
}

export default function AnalyzePage() {
  const router = useRouter()
  const [reviewText, setReviewText] = useState('')
  const [file, setFile] = useState<File | null>(null)
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState('')
  const [result, setResult] = useState<AnalysisResult | null>(null)

  // API base URL - would come from environment variables in a real app
  const API_URL = 'http://localhost:8000/api'

  const handleTextChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setReviewText(e.target.value)
  }

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      setFile(e.target.files[0])
    }
  }

  const analyzeText = async () => {
    if (!reviewText.trim()) {
      setError('Please enter some text to analyze')
      return
    }

    setIsLoading(true)
    setError('')
    
    try {
      // First, create a review
      const reviewResponse = await axios.post(`${API_URL}/reviews/`, {
        text: reviewText,
        source: 'manual'
      })
      
      const reviewId = reviewResponse.data.id
      
      // Analyze sentiment
      const sentimentResponse = await axios.post(
        `${API_URL}/sentiment/analyze-review/${reviewId}`
      )
      
      // Extract aspects
      const aspectsResponse = await axios.post(
        `${API_URL}/aspects/analyze-review/${reviewId}`
      )
      
      // Generate summary
      const summaryResponse = await axios.post(
        `${API_URL}/summarization/summarize-review/${reviewId}`
      )
      
      // Combine results
      setResult({
        sentiment: sentimentResponse.data,
        aspects: aspectsResponse.data,
        summary: summaryResponse.data.summary_text
      })
      
      // Navigate to results page with the review ID
      router.push(`/analyze/results?id=${reviewId}`)
      
    } catch (err) {
      console.error('Error analyzing review:', err)
      setError('An error occurred while analyzing the review. Please try again.')
    } finally {
      setIsLoading(false)
    }
  }

  const uploadFile = async () => {
    if (!file) {
      setError('Please select a file to upload')
      return
    }

    if (!file.name.endsWith('.csv')) {
      setError('Only CSV files are supported')
      return
    }

    setIsLoading(true)
    setError('')
    
    try {
      const formData = new FormData()
      formData.append('file', file)
      
      const response = await axios.post(
        `${API_URL}/reviews/upload-csv`,
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        }
      )
      
      // Navigate to reviews page to see uploaded reviews
      router.push('/reviews')
      
    } catch (err) {
      console.error('Error uploading file:', err)
      setError('An error occurred while uploading the file. Please try again.')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="space-y-8">
      <h1 className="text-3xl font-bold">Analyze Reviews</h1>
      
      <div className="grid md:grid-cols-2 gap-8">
        {/* Text Input Section */}
        <div className="card">
          <h2 className="text-xl font-semibold mb-4">Enter Review Text</h2>
          <div className="space-y-4">
            <div>
              <label htmlFor="reviewText" className="label">Review Text</label>
              <textarea
                id="reviewText"
                className="textarea-field h-40"
                placeholder="Enter the review text to analyze..."
                value={reviewText}
                onChange={handleTextChange}
              />
            </div>
            <button 
              className="btn-primary w-full"
              onClick={analyzeText}
              disabled={isLoading || !reviewText.trim()}
            >
              {isLoading ? (
                <>
                  <FaSpinner className="animate-spin mr-2" />
                  Analyzing...
                </>
              ) : (
                'Analyze Review'
              )}
            </button>
          </div>
        </div>
        
        {/* File Upload Section */}
        <div className="card">
          <h2 className="text-xl font-semibold mb-4">Upload CSV File</h2>
          <div className="space-y-4">
            <div className="border-2 border-dashed border-gray-300 rounded-md p-6 text-center">
              <input
                type="file"
                id="fileUpload"
                className="hidden"
                accept=".csv"
                onChange={handleFileChange}
              />
              <label 
                htmlFor="fileUpload" 
                className="cursor-pointer flex flex-col items-center justify-center"
              >
                <FaUpload className="text-4xl text-gray-400 mb-2" />
                <span className="text-gray-600">
                  {file ? file.name : 'Click to select a CSV file'}
                </span>
              </label>
              <p className="text-sm text-gray-500 mt-2">
                CSV should have a 'text' column with review content
              </p>
            </div>
            <button 
              className="btn-secondary w-full"
              onClick={uploadFile}
              disabled={isLoading || !file}
            >
              {isLoading ? (
                <>
                  <FaSpinner className="animate-spin mr-2" />
                  Uploading...
                </>
              ) : (
                'Upload and Analyze'
              )}
            </button>
          </div>
        </div>
      </div>
      
      {/* Error Message */}
      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
          {error}
        </div>
      )}
      
      {/* Instructions */}
      <div className="bg-gray-50 p-6 rounded-lg">
        <h2 className="text-xl font-semibold mb-2">Instructions</h2>
        <ul className="list-disc list-inside space-y-2 text-gray-700">
          <li>Enter a product review in the text box or upload a CSV file with multiple reviews.</li>
          <li>For CSV uploads, ensure your file has a column named 'text' containing the review content.</li>
          <li>You can optionally include a 'rating' column with numerical ratings.</li>
          <li>The analysis will detect sentiment, extract key aspects, and generate a summary.</li>
          <li>Results will show overall sentiment (positive, neutral, negative) and aspect-specific sentiment.</li>
        </ul>
      </div>
    </div>
  )
}
