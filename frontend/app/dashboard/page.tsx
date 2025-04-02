'use client'

import { useState, useEffect } from 'react'
import axios from 'axios'
import Link from 'next/link'
import { 
  Chart as ChartJS, 
  CategoryScale, 
  LinearScale, 
  PointElement, 
  LineElement, 
  BarElement,
  Title, 
  Tooltip, 
  Legend, 
  ArcElement 
} from 'chart.js'
import { Line, Bar, Pie } from 'react-chartjs-2'
import { FaChartLine, FaChartBar, FaChartPie, FaTable } from 'react-icons/fa'

// Register ChartJS components
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  ArcElement,
  Title,
  Tooltip,
  Legend
)

// Define types
interface ReviewTrend {
  id: number
  date: string
  total_reviews: number
  avg_sentiment: number
  sentiment_distribution: {
    positive: number
    neutral: number
    negative: number
  }
  top_aspects: Array<{
    aspect: string
    count: number
    avg_sentiment: number
  }>
}

interface TopAspect {
  aspect: string
  count: number
  avg_sentiment: number
  sentiment_label: string
}

interface DashboardData {
  trends: ReviewTrend[]
  topAspects: TopAspect[]
  totalReviews: number
  sentimentDistribution: {
    positive: number
    neutral: number
    negative: number
  }
}

export default function DashboardPage() {
  const [data, setData] = useState<DashboardData | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState('')
  const [timeRange, setTimeRange] = useState('month') // 'week', 'month', 'year'
  
  // API base URL - would come from environment variables in a real app
  const API_URL = 'http://localhost:8000/api'
  
  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        // Fetch sentiment trends
        const trendsResponse = await axios.get(`${API_URL}/sentiment/trends`)
        
        // Fetch top aspects
        const aspectsResponse = await axios.get(`${API_URL}/aspects/top`)
        
        // Calculate total reviews and sentiment distribution
        const totalReviews = trendsResponse.data.reduce(
          (sum: number, trend: ReviewTrend) => sum + trend.total_reviews, 
          0
        )
        
        const sentimentDistribution = {
          positive: 0,
          neutral: 0,
          negative: 0
        }
        
        trendsResponse.data.forEach((trend: ReviewTrend) => {
          sentimentDistribution.positive += trend.sentiment_distribution.positive
          sentimentDistribution.neutral += trend.sentiment_distribution.neutral
          sentimentDistribution.negative += trend.sentiment_distribution.negative
        })
        
        setData({
          trends: trendsResponse.data,
          topAspects: aspectsResponse.data,
          totalReviews,
          sentimentDistribution
        })
      } catch (err) {
        console.error('Error fetching dashboard data:', err)
        setError('An error occurred while fetching dashboard data')
      } finally {
        setIsLoading(false)
      }
    }
    
    fetchDashboardData()
  }, [])
  
  // Prepare chart data
  const prepareSentimentTrendData = () => {
    if (!data || !data.trends || data.trends.length === 0) {
      return {
        labels: [],
        datasets: []
      }
    }
    
    // Sort trends by date
    const sortedTrends = [...data.trends].sort(
      (a, b) => new Date(a.date).getTime() - new Date(b.date).getTime()
    )
    
    return {
      labels: sortedTrends.map(trend => {
        const date = new Date(trend.date)
        return date.toLocaleDateString()
      }),
      datasets: [
        {
          label: 'Average Sentiment',
          data: sortedTrends.map(trend => trend.avg_sentiment),
          borderColor: 'rgb(53, 162, 235)',
          backgroundColor: 'rgba(53, 162, 235, 0.5)',
          tension: 0.3
        }
      ]
    }
  }
  
  const prepareSentimentDistributionData = () => {
    if (!data || !data.sentimentDistribution) {
      return {
        labels: [],
        datasets: []
      }
    }
    
    return {
      labels: ['Positive', 'Neutral', 'Negative'],
      datasets: [
        {
          data: [
            data.sentimentDistribution.positive,
            data.sentimentDistribution.neutral,
            data.sentimentDistribution.negative
          ],
          backgroundColor: [
            'rgba(75, 192, 192, 0.6)',
            'rgba(255, 206, 86, 0.6)',
            'rgba(255, 99, 132, 0.6)'
          ],
          borderColor: [
            'rgba(75, 192, 192, 1)',
            'rgba(255, 206, 86, 1)',
            'rgba(255, 99, 132, 1)'
          ],
          borderWidth: 1
        }
      ]
    }
  }
  
  const prepareTopAspectsData = () => {
    if (!data || !data.topAspects || data.topAspects.length === 0) {
      return {
        labels: [],
        datasets: []
      }
    }
    
    // Sort aspects by count (descending)
    const sortedAspects = [...data.topAspects].sort((a, b) => b.count - a.count).slice(0, 10)
    
    return {
      labels: sortedAspects.map(aspect => aspect.aspect),
      datasets: [
        {
          label: 'Mention Count',
          data: sortedAspects.map(aspect => aspect.count),
          backgroundColor: 'rgba(75, 192, 192, 0.6)',
          borderColor: 'rgba(75, 192, 192, 1)',
          borderWidth: 1
        }
      ]
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
      </div>
    )
  }
  
  // If no data is available yet, show a placeholder
  if (!data || !data.trends || data.trends.length === 0) {
    return (
      <div className="space-y-8">
        <h1 className="text-3xl font-bold">Dashboard</h1>
        <div className="card text-center py-12">
          <h2 className="text-xl font-semibold mb-4">No Data Available</h2>
          <p className="text-gray-600 mb-6">
            Start analyzing reviews to see trends and insights here.
          </p>
          <Link href="/analyze" className="btn-primary">
            Analyze Reviews
          </Link>
        </div>
      </div>
    )
  }
  
  return (
    <div className="space-y-8">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold">Dashboard</h1>
        <div className="flex space-x-2">
          <button 
            className={`px-3 py-1 rounded-md ${timeRange === 'week' ? 'bg-primary-600 text-white' : 'bg-gray-200'}`}
            onClick={() => setTimeRange('week')}
          >
            Week
          </button>
          <button 
            className={`px-3 py-1 rounded-md ${timeRange === 'month' ? 'bg-primary-600 text-white' : 'bg-gray-200'}`}
            onClick={() => setTimeRange('month')}
          >
            Month
          </button>
          <button 
            className={`px-3 py-1 rounded-md ${timeRange === 'year' ? 'bg-primary-600 text-white' : 'bg-gray-200'}`}
            onClick={() => setTimeRange('year')}
          >
            Year
          </button>
        </div>
      </div>
      
      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="card">
          <h2 className="text-lg font-semibold mb-2">Total Reviews</h2>
          <p className="text-3xl font-bold text-primary-600">{data.totalReviews}</p>
        </div>
        
        <div className="card">
          <h2 className="text-lg font-semibold mb-2">Average Sentiment</h2>
          <p className="text-3xl font-bold text-primary-600">
            {data.trends.length > 0 
              ? data.trends.reduce((sum, trend) => sum + trend.avg_sentiment, 0) / data.trends.length
              : 0
            }
          </p>
        </div>
        
        <div className="card">
          <h2 className="text-lg font-semibold mb-2">Top Aspect</h2>
          <p className="text-3xl font-bold text-primary-600 capitalize">
            {data.topAspects.length > 0 ? data.topAspects[0].aspect : 'N/A'}
          </p>
        </div>
      </div>
      
      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Sentiment Trend Chart */}
        <div className="card">
          <div className="flex items-center mb-4">
            <FaChartLine className="text-primary-600 mr-2" />
            <h2 className="text-xl font-semibold">Sentiment Trend</h2>
          </div>
          <div className="h-64">
            <Line 
              data={prepareSentimentTrendData()} 
              options={{
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                  y: {
                    min: -1,
                    max: 1,
                    title: {
                      display: true,
                      text: 'Sentiment Score'
                    }
                  }
                }
              }}
            />
          </div>
        </div>
        
        {/* Sentiment Distribution Chart */}
        <div className="card">
          <div className="flex items-center mb-4">
            <FaChartPie className="text-primary-600 mr-2" />
            <h2 className="text-xl font-semibold">Sentiment Distribution</h2>
          </div>
          <div className="h-64 flex justify-center">
            <div className="w-64">
              <Pie 
                data={prepareSentimentDistributionData()} 
                options={{
                  responsive: true,
                  maintainAspectRatio: false
                }}
              />
            </div>
          </div>
        </div>
        
        {/* Top Aspects Chart */}
        <div className="card">
          <div className="flex items-center mb-4">
            <FaChartBar className="text-primary-600 mr-2" />
            <h2 className="text-xl font-semibold">Top Aspects</h2>
          </div>
          <div className="h-64">
            <Bar 
              data={prepareTopAspectsData()} 
              options={{
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                  y: {
                    beginAtZero: true,
                    title: {
                      display: true,
                      text: 'Mention Count'
                    }
                  }
                }
              }}
            />
          </div>
        </div>
        
        {/* Top Aspects Table */}
        <div className="card">
          <div className="flex items-center mb-4">
            <FaTable className="text-primary-600 mr-2" />
            <h2 className="text-xl font-semibold">Top Aspects</h2>
          </div>
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Aspect
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Mentions
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Sentiment
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {data.topAspects.slice(0, 5).map((aspect, index) => (
                  <tr key={index}>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900 capitalize">
                      {aspect.aspect}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {aspect.count}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm">
                      <span className={`
                        px-2 py-1 rounded-full text-xs font-medium
                        ${aspect.sentiment_label === 'positive' ? 'bg-green-100 text-green-800' : 
                          aspect.sentiment_label === 'negative' ? 'bg-red-100 text-red-800' : 
                          'bg-gray-100 text-gray-800'}
                      `}>
                        {aspect.sentiment_label}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
      
      {/* Action Button */}
      <div className="flex justify-center">
        <Link href="/reviews" className="btn-primary">
          View All Reviews
        </Link>
      </div>
    </div>
  )
}
