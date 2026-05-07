import { useState } from 'react'
import { Download, FileText, X } from 'lucide-react'
import clsx from 'clsx'

export default function ExportModal({
  isOpen,
  onClose,
  onExport,
  title = 'Export Data',
  className = '',
}) {
  const [isExporting, setIsExporting] = useState(false)

  const handleExport = async () => {
    setIsExporting(true)
    try {
      await onExport({
        format: 'pdf',
      })
      onClose()
    } catch (error) {
      console.error('Export failed:', error)
    } finally {
      setIsExporting(false)
    }
  }

  if (!isOpen) return null

  return (
    <>
      <div className="fixed inset-0 bg-black/50 z-50" onClick={onClose} />

      <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
        <div
          className={clsx(
            'bg-card rounded-lg border border-border shadow-xl max-w-sm w-full max-h-[90vh] overflow-y-auto',
            className,
          )}
        >
          <div className="flex items-center justify-between p-6 border-b border-border">
            <h2 className="text-lg font-semibold">{title}</h2>
            <button onClick={onClose} className="p-1 rounded hover:bg-muted" type="button">
              <X className="w-5 h-5" />
            </button>
          </div>

          <div className="p-6 space-y-4">
            <div className="grid grid-cols-1 gap-3">
              <button
                type="button"
                onClick={() => handleExport()}
                disabled={isExporting}
                className={clsx(
                  'flex items-center justify-center gap-2 p-3 rounded-lg border transition-colors',
                  'border-border hover:bg-muted',
                  'disabled:opacity-50'
                )}
              >
                <FileText className="w-5 h-5" />
                <span className="text-sm font-medium">PDF Analysis Report</span>
              </button>
            </div>

            <p className="text-sm text-muted-foreground">
              The PDF includes dashboard analysis summaries such as sentiment trend data, aspect issues, alerts,
              and root-cause findings. Raw review rows are not included.
            </p>

            <div className="flex items-center justify-center text-sm text-muted-foreground min-h-[1.5rem]">
              {isExporting ? (
                <span className="flex items-center gap-2">
                  <span className="w-4 h-4 border-2 border-primary-foreground/30 border-t-primary-foreground rounded-full animate-spin" />
                  Download started...
                  <Download className="w-4 h-4" />
                </span>
              ) : (
                <span>&nbsp;</span>
              )}
            </div>
          </div>
        </div>
      </div>
    </>
  )
}

