import { useMemo } from 'react'
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Area,
  AreaChart
} from 'recharts'
import clsx from 'clsx'

export default function TrendChart({
  data,
  title,
  dataKey = 'value',
  xAxisKey = 'date',
  color = '#3b82f6',
  type = 'line', // 'line' or 'area'
  height = 300,
  className = '',
  showGrid = true,
  showTooltip = true
}) {
  const chartData = useMemo(() => {
    return data?.map(item => ({
      ...item,
      [xAxisKey]: item[xAxisKey] instanceof Date
        ? item[xAxisKey].toLocaleDateString()
        : item[xAxisKey]
    })) || []
  }, [data, xAxisKey])

  const CustomTooltip = ({ active, payload, label }) => {
    if (active && payload && payload.length) {
      return (
        <div className="bg-card border border-border rounded-lg p-3 shadow-lg">
          <p className="text-sm font-medium">{label}</p>
          <p className="text-sm text-muted-foreground">
            Value: <span className="font-medium text-foreground">{payload[0].value}</span>
          </p>
        </div>
      )
    }
    return null
  }

  const ChartComponent = type === 'area' ? AreaChart : LineChart
  const DataComponent = type === 'area' ? Area : Line

  return (
    <div className={clsx(
      'bg-card rounded-lg border border-border p-6',
      className
    )}>
      {title && (
        <h3 className="text-lg font-semibold mb-4">{title}</h3>
      )}

      <ResponsiveContainer width="100%" height={height}>
        <ChartComponent data={chartData}>
          {showGrid && (
            <CartesianGrid
              strokeDasharray="3 3"
              className="stroke-muted"
            />
          )}

          <XAxis
            dataKey={xAxisKey}
            className="text-muted-foreground"
            fontSize={12}
            tickLine={false}
            axisLine={false}
          />

          <YAxis
            className="text-muted-foreground"
            fontSize={12}
            tickLine={false}
            axisLine={false}
          />

          {showTooltip && <Tooltip content={<CustomTooltip />} />}

          <DataComponent
            type="monotone"
            dataKey={dataKey}
            stroke={color}
            strokeWidth={2}
            dot={{ fill: color, strokeWidth: 2, r: 4 }}
            activeDot={{ r: 6, stroke: color, strokeWidth: 2 }}
            fill={type === 'area' ? color : 'none'}
            fillOpacity={type === 'area' ? 0.1 : 1}
          />
        </ChartComponent>
      </ResponsiveContainer>
    </div>
  )
}