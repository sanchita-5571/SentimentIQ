import KPICard from '../Dashboard/KPICard'
import { MessageSquare, Gauge, ThumbsDown, Star, Tags, CopyMinus } from 'lucide-react'
import { motion } from 'framer-motion'
import { Skeleton } from './Skeleton'
import { useEffect, useState } from 'react'

export default function StatGrid({ overview, loading }) {
  const [animatedValues, setAnimatedValues] = useState({})

  useEffect(() => {
    if (overview) {
      setAnimatedValues({
        totalReviews: overview.total_reviews || 0,
        averageSentiment: overview.average_sentiment || 0,
        negativeRatio: overview.negative_ratio || 0,
        averageRating: overview.average_rating || 0,
        activeTopics: overview.active_topics || 0,
        duplicatesRemoved: overview.duplicates_removed || 0,
      })
    }
  }, [overview])

  const kpiCards = [
    {
      title: 'Total Reviews',
      value: animatedValues.totalReviews?.toLocaleString() || '0',
      changeType: 'neutral',
      icon: MessageSquare,
    },
    {
      title: 'Average Sentiment',
      value: Number(animatedValues.averageSentiment || 0).toFixed(2),
      changeType: 'neutral',
      icon: Gauge,
    },
    {
      title: 'Negative Sentiment',
      value: `${Math.round((animatedValues.negativeRatio || 0) * 100)}%`,
      changeType: animatedValues.negativeRatio > 0.3 ? 'negative' : 'neutral',
      icon: ThumbsDown,
    },
    {
      title: 'Average Rating',
      value: Number(animatedValues.averageRating || 0).toFixed(1),
      changeType: 'neutral',
      icon: Star,
    },
    {
      title: 'Active Topics',
      value: animatedValues.activeTopics || 0,
      changeType: 'neutral',
      icon: Tags,
    },
    {
      title: 'Duplicates Removed',
      value: animatedValues.duplicatesRemoved || 0,
      changeType: 'neutral',
      icon: CopyMinus,
    },
  ]

  if (loading) {
    return (
      <div className="grid gap-6 md:grid-cols-2 xl:grid-cols-3">
        {Array.from({ length: 6 }).map((_, i) => (
          <Skeleton key={i} className="h-32 w-full rounded-xl" />
        ))}
      </div>
    )
  }

  return (
    <motion.div 
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="grid gap-6 md:grid-cols-2 xl:grid-cols-3"
    >
      {kpiCards.map((card, index) => (
        <motion.div
          key={card.title}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: index * 0.05 }}
        >
          <KPICard {...card} />
        </motion.div>
      ))}
    </motion.div>
  )
}
