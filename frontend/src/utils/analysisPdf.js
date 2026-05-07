const PAGE_WIDTH = 1240
const PAGE_HEIGHT = 1754
const MARGIN = 84
const CONTENT_WIDTH = PAGE_WIDTH - MARGIN * 2

const formatNumber = (value, digits = 2) => Number(value ?? 0).toFixed(digits)

const formatDate = (value, withTime = false) => {
  if (!value) return 'Unknown'
  const date = new Date(value)
  return withTime ? date.toLocaleString() : date.toLocaleDateString()
}

const normalizeValue = (value) => {
  if (value === null || value === undefined || value === '') return 'None'
  if (Array.isArray(value)) return value.join(', ') || 'None'
  return String(value)
}

const wrapTextLines = (ctx, text, maxWidth) => {
  const value = String(text ?? '')
  if (!value) return ['']

  const words = value.split(/\s+/)
  const lines = []
  let current = ''

  words.forEach((word) => {
    const candidate = current ? `${current} ${word}` : word
    if (ctx.measureText(candidate).width <= maxWidth) {
      current = candidate
      return
    }

    if (current) {
      lines.push(current)
    }

    if (ctx.measureText(word).width <= maxWidth) {
      current = word
      return
    }

    let segment = ''
    for (const character of word) {
      const testSegment = `${segment}${character}`
      if (ctx.measureText(testSegment).width <= maxWidth) {
        segment = testSegment
      } else {
        if (segment) lines.push(segment)
        segment = character
      }
    }
    current = segment
  })

  if (current) lines.push(current)
  return lines
}

const deriveAlertsFromRootCauses = (events = []) =>
  events.map((event) => ({
    title: event.earliest_degrading_aspect
      ? `${event.earliest_degrading_aspect} sentiment drop detected`
      : 'Sentiment drop detected',
    message: `Sentiment changed by ${formatNumber(event.sentiment_delta ?? 0)} across ${
      event.review_volume ?? 0
    } reviews.`,
    severity:
      event.sentiment_delta <= -0.35 ? 'high' : event.sentiment_delta <= -0.2 ? 'medium' : 'low',
    timestamp: event.event_date || event.created_at,
  }))

const createPage = () => {
  const canvas = document.createElement('canvas')
  canvas.width = PAGE_WIDTH
  canvas.height = PAGE_HEIGHT
  const ctx = canvas.getContext('2d')
  ctx.fillStyle = '#ffffff'
  ctx.fillRect(0, 0, PAGE_WIDTH, PAGE_HEIGHT)
  return { canvas, ctx }
}

const drawRoundedRect = (ctx, x, y, width, height, radius, fill, stroke = '#dbe4f0') => {
  ctx.beginPath()
  ctx.moveTo(x + radius, y)
  ctx.lineTo(x + width - radius, y)
  ctx.quadraticCurveTo(x + width, y, x + width, y + radius)
  ctx.lineTo(x + width, y + height - radius)
  ctx.quadraticCurveTo(x + width, y + height, x + width - radius, y + height)
  ctx.lineTo(x + radius, y + height)
  ctx.quadraticCurveTo(x, y + height, x, y + height - radius)
  ctx.lineTo(x, y + radius)
  ctx.quadraticCurveTo(x, y, x + radius, y)
  ctx.closePath()
  ctx.fillStyle = fill
  ctx.fill()
  ctx.strokeStyle = stroke
  ctx.lineWidth = 2
  ctx.stroke()
}

const drawHeading = (ctx, title, subtitle) => {
  drawRoundedRect(ctx, MARGIN, 54, CONTENT_WIDTH, 154, 28, '#eff6ff', '#c8daf8')
  ctx.fillStyle = '#0f172a'
  ctx.font = '700 40px Arial'
  ctx.fillText(title, MARGIN + 28, 118)
  ctx.fillStyle = '#475569'
  ctx.font = '400 20px Arial'
  ctx.fillText(subtitle, MARGIN + 28, 156)
}

const drawMetricCard = (ctx, x, y, width, label, value, accent) => {
  drawRoundedRect(ctx, x, y, width, 118, 22, '#ffffff', '#dde7f2')
  ctx.fillStyle = accent
  ctx.fillRect(x + 20, y + 20, 10, 10)
  ctx.fillStyle = '#475569'
  ctx.font = '600 18px Arial'
  ctx.fillText(label, x + 42, y + 30)
  ctx.fillStyle = '#0f172a'
  ctx.font = '700 34px Arial'
  ctx.fillText(value, x + 20, y + 82)
}

const drawSectionTitle = (ctx, title, x, y) => {
  ctx.fillStyle = '#0f172a'
  ctx.font = '700 28px Arial'
  ctx.fillText(title, x, y)
}

const drawParagraphLines = (ctx, lines, x, y, maxWidth, lineHeight = 26, color = '#334155') => {
  ctx.fillStyle = color
  ctx.font = '400 18px Arial'
  let cursorY = y
  lines.forEach((line) => {
    wrapTextLines(ctx, line, maxWidth).forEach((wrapped) => {
      ctx.fillText(wrapped, x, cursorY)
      cursorY += lineHeight
    })
  })
  return cursorY
}

const drawFiltersPanel = (ctx, filters, x, y, width, height) => {
  drawRoundedRect(ctx, x, y, width, height, 22, '#f8fafc', '#dde7f2')
  drawSectionTitle(ctx, 'Applied Filters', x + 22, y + 42)
  ctx.font = '400 18px Arial'
  ctx.fillStyle = '#334155'
  const entries = Object.keys(filters).length
    ? Object.entries(filters).map(([key, value]) => `${key}: ${normalizeValue(value)}`)
    : ['No filters applied.']

  let cursorY = y + 78
  entries.forEach((entry) => {
    wrapTextLines(ctx, entry, width - 44).forEach((line) => {
      if (cursorY <= y + height - 18) {
        ctx.fillText(line, x + 22, cursorY)
        cursorY += 24
      }
    })
  })
}

const drawTimelineChart = (ctx, timeline, x, y, width, height) => {
  drawRoundedRect(ctx, x, y, width, height, 22, '#ffffff', '#dde7f2')
  drawSectionTitle(ctx, 'Sentiment Trend and Review Volume', x + 22, y + 42)

  if (!timeline.length) {
    drawParagraphLines(ctx, ['No trend data available.'], x + 22, y + 92, width - 44)
    return
  }

  const chartX = x + 70
  const chartY = y + 78
  const chartWidth = width - 110
  const chartHeight = height - 150
  const points = timeline.slice(0, 10)
  const maxReviews = Math.max(...points.map((item) => item.review_count ?? 0), 1)

  ctx.strokeStyle = '#cbd5e1'
  ctx.lineWidth = 2
  ctx.beginPath()
  ctx.moveTo(chartX, chartY)
  ctx.lineTo(chartX, chartY + chartHeight)
  ctx.lineTo(chartX + chartWidth, chartY + chartHeight)
  ctx.stroke()

  for (let step = 0; step <= 4; step += 1) {
    const gridY = chartY + (chartHeight / 4) * step
    ctx.strokeStyle = '#edf2f7'
    ctx.lineWidth = 1
    ctx.beginPath()
    ctx.moveTo(chartX, gridY)
    ctx.lineTo(chartX + chartWidth, gridY)
    ctx.stroke()
  }

  const gap = chartWidth / points.length
  const barWidth = Math.max(gap * 0.42, 18)
  const linePoints = []

  points.forEach((point, index) => {
    const centerX = chartX + gap * index + gap / 2
    const barHeight = ((point.review_count ?? 0) / maxReviews) * (chartHeight * 0.76)
    const barY = chartY + chartHeight - barHeight

    ctx.fillStyle = '#93c5fd'
    ctx.fillRect(centerX - barWidth / 2, barY, barWidth, barHeight)

    const sentimentRatio = ((point.average_sentiment ?? 0) + 1) / 2
    const pointY = chartY + chartHeight - sentimentRatio * chartHeight
    linePoints.push([centerX, pointY])

    ctx.fillStyle = '#64748b'
    ctx.font = '12px Arial'
    const label = new Date(point.date).toLocaleDateString(undefined, { month: 'short', day: 'numeric' })
    ctx.save()
    ctx.translate(centerX - 14, chartY + chartHeight + 18)
    ctx.rotate(-Math.PI / 6)
    ctx.fillText(label, 0, 0)
    ctx.restore()
  })

  ctx.strokeStyle = '#16a34a'
  ctx.lineWidth = 4
  ctx.beginPath()
  linePoints.forEach(([px, py], index) => {
    if (index === 0) ctx.moveTo(px, py)
    else ctx.lineTo(px, py)
  })
  ctx.stroke()

  ctx.fillStyle = '#16a34a'
  linePoints.forEach(([px, py]) => {
    ctx.beginPath()
    ctx.arc(px, py, 5, 0, Math.PI * 2)
    ctx.fill()
  })

  ctx.fillStyle = '#334155'
  ctx.font = '15px Arial'
  ctx.fillText('Blue bars = review volume', x + 22, y + height - 22)
  ctx.fillText('Green line = average sentiment', x + 240, y + height - 22)
}

const drawAspectChart = (ctx, aspects, x, y, width, height) => {
  drawRoundedRect(ctx, x, y, width, height, 22, '#ffffff', '#dde7f2')
  drawSectionTitle(ctx, 'Top Aspect Mentions', x + 22, y + 42)

  if (!aspects.length) {
    drawParagraphLines(ctx, ['No aspect trend data available.'], x + 22, y + 92, width - 44)
    return
  }

  const rows = aspects.slice(0, 6)
  const maxMentions = Math.max(...rows.map((item) => item.mention_count ?? 0), 1)
  let rowY = y + 92

  rows.forEach((item) => {
    ctx.fillStyle = '#0f172a'
    ctx.font = '600 18px Arial'
    ctx.fillText(item.aspect, x + 22, rowY)

    const barX = x + 210
    const barWidth = ((item.mention_count ?? 0) / maxMentions) * (width - 360)
    drawRoundedRect(ctx, barX, rowY - 16, Math.max(barWidth, 2), 24, 10, '#f59e0b', '#d97706')

    ctx.fillStyle = '#334155'
    ctx.font = '16px Arial'
    ctx.fillText(
      `${item.mention_count ?? 0} mentions | avg ${formatNumber(item.average_score ?? 0)} | delta ${formatNumber(item.delta ?? 0)}`,
      barX + Math.max(barWidth, 2) + 14,
      rowY,
    )
    rowY += 56
  })
}

const drawListPanel = (ctx, title, lines, x, y, width, height) => {
  drawRoundedRect(ctx, x, y, width, height, 22, '#ffffff', '#dde7f2')
  drawSectionTitle(ctx, title, x + 22, y + 42)
  drawParagraphLines(ctx, lines.length ? lines : ['No data available.'], x + 22, y + 84, width - 44, 24)
}

const createCoverPage = ({ title, createdAt, overview, filters }) => {
  const { canvas, ctx } = createPage()
  drawHeading(ctx, title, `Generated ${formatDate(createdAt, true)}`)

  const cardWidth = (CONTENT_WIDTH - 22) / 2
  drawMetricCard(ctx, MARGIN, 250, cardWidth, 'Total Reviews', String(overview.total_reviews ?? 0), '#2563eb')
  drawMetricCard(ctx, MARGIN + cardWidth + 22, 250, cardWidth, 'Average Sentiment', formatNumber(overview.average_sentiment ?? 0), '#16a34a')
  drawMetricCard(ctx, MARGIN, 390, cardWidth, 'Negative Ratio', `${Math.round((overview.negative_ratio ?? 0) * 100)}%`, '#dc2626')
  drawMetricCard(ctx, MARGIN + cardWidth + 22, 390, cardWidth, 'Average Rating', formatNumber(overview.average_rating ?? 0), '#f59e0b')

  drawFiltersPanel(ctx, filters, MARGIN, 548, CONTENT_WIDTH, 290)

  drawRoundedRect(ctx, MARGIN, 872, CONTENT_WIDTH, 130, 22, '#f8fafc', '#dde7f2')
  drawSectionTitle(ctx, 'Report Scope', MARGIN + 22, 914)
  drawParagraphLines(
    ctx,
    [
      'This PDF focuses on dashboard analysis output: metrics, generated charts, top issues, alerts, and root-cause findings.',
      'Raw review rows are intentionally excluded so the document stays executive-friendly and analysis-oriented.',
    ],
    MARGIN + 22,
    952,
    CONTENT_WIDTH - 44,
  )

  return canvas
}

const createChartsPage = ({ snapshot }) => {
  const { canvas, ctx } = createPage()
  drawHeading(ctx, 'Analysis Charts', 'Visual summaries generated from the dashboard snapshot')
  drawTimelineChart(ctx, snapshot?.timeline || [], MARGIN, 250, CONTENT_WIDTH, 520)
  drawAspectChart(ctx, snapshot?.aspect_trends || [], MARGIN, 804, CONTENT_WIDTH, 420)
  return canvas
}

const createFindingsPage = ({ snapshot, rootCauses, alerts }) => {
  const { canvas, ctx } = createPage()
  drawHeading(ctx, 'Findings Summary', 'Issues, alerts, and root-cause signals from the analyzed dataset')

  const issueLines = (snapshot?.aspect_trends || []).slice(0, 6).map((item, index) => {
    const severity = item.delta <= -0.2 ? 'High' : item.delta <= -0.1 ? 'Medium' : 'Low'
    return `${index + 1}. ${item.aspect}: ${item.mention_count} mentions, average ${formatNumber(
      item.average_score ?? 0,
    )}, severity ${severity}.`
  })

  const alertLines = alerts.slice(0, 6).flatMap((alert, index) => [
    `${index + 1}. ${alert.title} (${String(alert.severity || 'low').toUpperCase()})`,
    `   ${alert.message} [${formatDate(alert.timestamp, true)}]`,
  ])

  const rootCauseLines = rootCauses.slice(0, 6).flatMap((event, index) => [
    `${index + 1}. ${event.earliest_degrading_aspect || 'General'} | Delta ${formatNumber(
      event.sentiment_delta ?? 0,
    )} | Reviews ${event.review_volume ?? 0}`,
    `   Date: ${formatDate(event.event_date)}`,
  ])

  drawListPanel(ctx, 'Top Issues', issueLines, MARGIN, 250, CONTENT_WIDTH, 250)
  drawListPanel(ctx, 'Alerts', alertLines, MARGIN, 534, CONTENT_WIDTH, 360)
  drawListPanel(ctx, 'Root Causes', rootCauseLines, MARGIN, 928, CONTENT_WIDTH, 300)
  return canvas
}

const dataUrlToBytes = (dataUrl) => {
  const base64 = dataUrl.split(',')[1]
  const binary = window.atob(base64)
  const bytes = new Uint8Array(binary.length)
  for (let index = 0; index < binary.length; index += 1) {
    bytes[index] = binary.charCodeAt(index)
  }
  return bytes
}

const getJpegDimensions = (bytes) => {
  let offset = 2
  while (offset < bytes.length) {
    if (bytes[offset] !== 0xff) {
      offset += 1
      continue
    }
    const marker = bytes[offset + 1]
    const length = (bytes[offset + 2] << 8) + bytes[offset + 3]
    if ([0xc0, 0xc1, 0xc2, 0xc3, 0xc5, 0xc6, 0xc7, 0xc9, 0xca, 0xcb, 0xcd, 0xce, 0xcf].includes(marker)) {
      return {
        height: (bytes[offset + 5] << 8) + bytes[offset + 6],
        width: (bytes[offset + 7] << 8) + bytes[offset + 8],
      }
    }
    offset += 2 + length
  }
  return { width: PAGE_WIDTH, height: PAGE_HEIGHT }
}

const encoder = new TextEncoder()
const encodeText = (value) => encoder.encode(value)

const joinBytes = (parts) => {
  const totalLength = parts.reduce((sum, part) => sum + part.length, 0)
  const output = new Uint8Array(totalLength)
  let offset = 0
  parts.forEach((part) => {
    output.set(part, offset)
    offset += part.length
  })
  return output
}

const createPdfFromJpegs = (jpegPages) => {
  const objects = []
  const addTextObject = (text) => {
    objects.push(encodeText(text))
    return objects.length
  }
  const addBinaryObject = (prefix, bytes, suffix = '\nendstream') => {
    objects.push(joinBytes([encodeText(prefix), bytes, encodeText(suffix)]))
    return objects.length
  }

  const pageIds = []
  jpegPages.forEach(({ bytes, width, height }) => {
    const imagePrefix =
      `<< /Type /XObject /Subtype /Image /Width ${width} /Height ${height} ` +
      `/ColorSpace /DeviceRGB /BitsPerComponent 8 /Filter /DCTDecode /Length ${bytes.length} >>\nstream\n`
    const imageId = addBinaryObject(imagePrefix, bytes)

    const contentStream = `q\n${PAGE_WIDTH} 0 0 ${PAGE_HEIGHT} 0 0 cm\n/Im1 Do\nQ`
    const contentId = addTextObject(`<< /Length ${contentStream.length} >>\nstream\n${contentStream}\nendstream`)
    const pageId = addTextObject(
      `<< /Type /Page /Parent 0 0 R /MediaBox [0 0 ${PAGE_WIDTH} ${PAGE_HEIGHT}] /Contents ${contentId} 0 R /Resources << /XObject << /Im1 ${imageId} 0 R >> >> >>`,
    )
    pageIds.push(pageId)
  })

  const pagesId = addTextObject(
    `<< /Type /Pages /Count ${pageIds.length} /Kids [${pageIds.map((id) => `${id} 0 R`).join(' ')}] >>`,
  )

  pageIds.forEach((pageId) => {
    const updated = new TextDecoder().decode(objects[pageId - 1]).replace('/Parent 0 0 R', `/Parent ${pagesId} 0 R`)
    objects[pageId - 1] = encodeText(updated)
  })

  const catalogId = addTextObject(`<< /Type /Catalog /Pages ${pagesId} 0 R >>`)

  const chunks = [encodeText('%PDF-1.4\n')]
  const offsets = [0]
  let currentOffset = chunks[0].length

  objects.forEach((body, index) => {
    const objectHeader = encodeText(`${index + 1} 0 obj\n`)
    const objectFooter = encodeText('\nendobj\n')
    offsets.push(currentOffset)
    chunks.push(objectHeader, body, objectFooter)
    currentOffset += objectHeader.length + body.length + objectFooter.length
  })

  const xrefOffset = currentOffset
  let xref = `xref\n0 ${objects.length + 1}\n`
  xref += '0000000000 65535 f \n'
  offsets.slice(1).forEach((offset) => {
    xref += `${String(offset).padStart(10, '0')} 00000 n \n`
  })
  xref += `trailer\n<< /Size ${objects.length + 1} /Root ${catalogId} 0 R >>\nstartxref\n${xrefOffset}\n%%EOF`
  chunks.push(encodeText(xref))

  return new Blob([joinBytes(chunks)], { type: 'application/pdf' })
}

export const downloadAnalysisPdf = ({
  filename,
  title,
  snapshot,
  rootCauses = [],
  filters = {},
  alerts,
  createdAt,
}) => {
  const resolvedAlerts = alerts?.length ? alerts : deriveAlertsFromRootCauses(rootCauses)
  const overview = snapshot?.overview || {}

  const canvases = [
    createCoverPage({
      title: title || 'SentimentIQ Analysis Report',
      createdAt: createdAt || Date.now(),
      overview,
      filters,
    }),
    createChartsPage({ snapshot }),
    createFindingsPage({ snapshot, rootCauses, alerts: resolvedAlerts }),
  ]

  const jpegPages = canvases.map((canvas) => {
    const bytes = dataUrlToBytes(canvas.toDataURL('image/jpeg', 0.92))
    const dimensions = getJpegDimensions(bytes)
    return { bytes, ...dimensions }
  })

  const pdfBlob = createPdfFromJpegs(jpegPages)
  const url = URL.createObjectURL(pdfBlob)
  const anchor = document.createElement('a')
  anchor.href = url
  anchor.download = filename
  anchor.click()
  URL.revokeObjectURL(url)
}
