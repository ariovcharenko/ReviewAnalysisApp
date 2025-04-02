'use client'

import { useState, useEffect } from 'react'
import axios from 'axios'
import Link from 'next/link'
import { FaSearch, FaFilter, FaThumbsUp, FaThumbsDown, FaMinus, FaEye } from 'react-icons/fa'

// Define types
interface Review {
  id: number
  text: string
  rating?: number
  source: string
  created_at: string
  sentiment_analysis?: {
    sentiment_label: string
    sentiment_score: number
  }
}

export default function ReviewsPage() {
  const [reviews, setReviews] = useState<Review[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState('')
  const [searchTerm, setSearchTerm] = useState('')
  const [filterSentiment, setFilterSentiment] = useState<string | null>(null)
  const [currentPage, setCurrentPage] = useState(1)
  const [totalPages, setTotalPages] = useState(1)
  
  // API base URL - would come from environment variables in a real app
  const API_URL = 'http://localhost:8000/api'
  const ITEMS_PER_PAGE = 10
  
  useEffect(() => {
    fetchReviews()
  }, [currentPage, filterSentiment])
  
  const fetchReviews = async () => {
    setIsLoading(true)
    try {
      // In a real app, we would use pagination and filtering parameters
      const response = await axios.get(`${API_URL}/reviews/`, {
        params: {
          skip: (currentPage - 1) * ITEMS_PER_PAGE,
          limit: ITEMS_PER_PAGE
        }
      })
      
      // Get reviews with their sentiment analysis
      const reviewsWithSentiment = await Promise.all(
        response.data.map(async (review: Review) => {
          try {
            const sentimentResponse = await axios.get(
              `${API_URL}/reviews/${review.id}/full-analysis`
            )
            return {
              ...review,
              sentiment_analysis: sentimentResponse.data.sentiment
            }
          } catch (err) {
            // If sentiment analysis is not available, return the review as is
            return review
          }
        })
      )
      
      // Apply sentiment filter if selected
      let filteredReviews = reviewsWithSentiment
      if (filterSentiment) {
        filteredReviews = reviewsWithSentiment.filter(
          review => review.sentiment_analysis?.sentiment_label === filterSentiment
        )
      }
      
      // Apply search filter if provided
      if (searchTerm) {
        filteredReviews = filteredReviews.filter(
          review => review.text.toLowerCase().includes(searchTerm.toLowerCase())
        )
      }
      
      setReviews(filteredReviews)
      
      // Calculate total pages (in a real app, this would come from the API)
      setTotalPages(Math.ceil(filteredReviews.length / ITEMS_PER_PAGE))
    } catch (err) {
      console.error('Error fetching reviews:', err)
      setError('An error occurred while fetching reviews')
    } finally {
      setIsLoading(false)
    }
  }
  
  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault()
    fetchReviews()
  }
  
  const handleSearchChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setSearchTerm(e.target.value)
  }
  
  const handleFilterChange = (sentiment: string | null) => {
    setFilterSentiment(sentiment)
    setCurrentPage(1) // Reset to first page when changing filters
  }
  
  const handlePageChange = (page: number) => {
    setCurrentPage(page)
  }
  
  // Helper function to get sentiment icon
  const getSentimentIcon = (label?: string) => {
    if (!label) return <FaMinus className="text-gray-500" />
    
    switch (label) {
      case 'positive':
        return <FaThumbsUp className="text-green-500" />
      case 'negative':
        return <FaThumbsDown className="text-red-500" />
      default:
        return <FaMinus className="text-gray-500" />
    }
  }
  
  // Helper function to truncate text
  const truncateText = (text: string, maxLength: number = 150) => {
    if (text.length <= maxLength) return text
    return text.substring(0, maxLength) + '...'
  }
  
  if (isLoading && reviews.length === 0) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary-600"></div>
      </div>
    )
  }
  
  return (
    <div className="space-y-8">
      <h1 className="text-3xl font-bold">Reviews</h1>
      
      {/* Search and Filter */}
      <div className="flex flex-col md:flex-row gap-4">
        <form onSubmit={handleSearch} className="flex-1">
          <div className="relative">
            <input
              type="text"
              placeholder="Search reviews..."
              className="input-field pl-10"
              value={searchTerm}
              onChange={handleSearchChange}
            />
            <FaSearch className="absolute left-3 top-3 text-gray-400" />
            <button type="submit" className="hidden">Search</button>
          </div>
        </form>
        
        <div className="flex items-center space-x-2">
          <span className="text-gray-700 flex items-center">
            <FaFilter className="mr-2" /> Filter:
          </span>
          <button
            className={`px-3 py-1 rounded-md ${filterSentiment === null ? 'bg-primary-600 text-white' : 'bg-gray-200'}`}
            onClick={() => handleFilterChange(null)}
          >
            All
          </button>
          <button
            className={`px-3 py-1 rounded-md ${filterSentiment === 'positive' ? 'bg-primary-600 text-white' : 'bg-gray-200'}`}
            onClick={() => handleFilterChange('positive')}
          >
            Positive
          </button>
          <button
            className={`px-3 py-1 rounded-md ${filterSentiment === 'neutral' ? 'bg-primary-600 text-white' : 'bg-gray-200'}`}
            onClick={() => handleFilterChange('neutral')}
          >
            Neutral
          </button>
          <button
            className={`px-3 py-1 rounded-md ${filterSentiment === 'negative' ? 'bg-primary-600 text-white' : 'bg-gray-200'}`}
            onClick={() => handleFilterChange('negative')}
          >
            Negative
          </button>
        </div>
      </div>
      
      {/* Error Message */}
      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
          <p>{error}</p>
        </div>
      )}
      
      {/* Reviews List */}
      {reviews.length === 0 ? (
        <div className="text-center py-8">
          <p className="text-gray-600">No reviews found</p>
          <Link href="/analyze" className="text-primary-600 hover:underline mt-2 inline-block">
            Add a review
          </Link>
        </div>
      ) : (
        <div className="space-y-4">
          {reviews.map(review => (
            <div key={review.id} className="card">
              <div className="flex justify-between items-start">
                <div className="flex-1">
                  <p className="text-gray-700 whitespace-pre-line mb-2">
                    {truncateText(review.text)}
                  </p>
                  <div className="flex items-center text-sm text-gray-500 space-x-4">
                    <span>ID: {review.id}</span>
                    {review.rating && <span>Rating: {review.rating}/5</span>}
                    <span>Source: {review.source}</span>
                    <span>Date: {new Date(review.created_at).toLocaleDateString()}</span>
                  </div>
                </div>
                <div className="flex flex-col items-center ml-4">
                  <div className="bg-gray-100 rounded-full p-3 mb-2">
                    {getSentimentIcon(review.sentiment_analysis?.sentiment_label)}
                  </div>
                  <Link 
                    href={`/analyze/results?id=${review.id}`}
                    className="text-primary-600 hover:underline flex items-center text-sm"
                  >
                    <FaEye className="mr-1" /> View
                  </Link>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
      
      {/* Pagination */}
      {totalPages > 1 && (
        <div className="flex justify-center mt-8">
          <nav className="flex items-center space-x-2">
            <button
              onClick={() => handlePageChange(currentPage - 1)}
              disabled={currentPage === 1}
              className={`px-3 py-1 rounded-md ${currentPage === 1 ? 'bg-gray-100 text-gray-400 cursor-not-allowed' : 'bg-gray-200 hover:bg-gray-300'}`}
            >
              Previous
            </button>
            
            {Array.from({ length: totalPages }, (_, i) => i + 1).map(page => (
              <button
                key={page}
                onClick={() => handlePageChange(page)}
                className={`px-3 py-1 rounded-md ${currentPage === page ? 'bg-primary-600 text-white' : 'bg-gray-200 hover:bg-gray-300'}`}
              >
                {page}
              </button>
            ))}
            
            <button
              onClick={() => handlePageChange(currentPage + 1)}
              disabled={currentPage === totalPages}
              className={`px-3 py-1 rounded-md ${currentPage === totalPages ? 'bg-gray-100 text-gray-400 cursor-not-allowed' : 'bg-gray-200 hover:bg-gray-300'}`}
            >
              Next
            </button>
          </nav>
        </div>
      )}
      
      {/* Action Button */}
      <div className="flex justify-center">
        <Link href="/analyze" className="btn-primary">
          Analyze New Review
        </Link>
      </div>
    </div>
  )
}
