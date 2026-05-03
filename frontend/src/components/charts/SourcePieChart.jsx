import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip, Legend } from 'recharts'
import { motion } from 'framer-motion'

const COLORS = ['#16A34A', '#DC2626', '#0EA5E9', '#F59E0B']

export default function SourcePieChart({ data, loading }) {
  const safeData = data || []

  if (loading) {
    return <div className="h-64 flex items-center justify-center">
      Loading source distribution...
    </div>
  }

  if (!safeData.length) {
    return <div className="h-64 flex items-center justify-center text-sm text-muted-foreground">
      Source distribution will appear after more reviews are available.
    </div>
  }

  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="h-80">
      <ResponsiveContainer width="100%" height="100%">
        <PieChart>
          <Pie
            data={data || []}
            cx="50%"
            cy="50%"
            outerRadius={80}
            dataKey="value"
            nameKey="name"
            label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
          >
            {safeData.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
            ))}
          </Pie>
          <Tooltip />
          <Legend />
        </PieChart>
      </ResponsiveContainer>
    </motion.div>
  )
}
