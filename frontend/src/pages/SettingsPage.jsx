import { useEffect, useState } from 'react'
import toast from 'react-hot-toast'
import { Card, SectionTitle } from '../components/UI/Card'
import { Button } from '../components/UI/button'
import { Badge } from '../components/UI/badge'
import { useUIStore } from '../stores/uiStore'
import { getErrorMessage, settingsApi } from '../api/client'

export default function SettingsPage() {
  const darkMode = useUIStore((state) => state.darkMode)
  const setDarkMode = useUIStore((state) => state.setDarkMode)
  const refreshInterval = useUIStore((state) => state.refreshInterval)
  const emailAlerts = useUIStore((state) => state.emailAlerts)
  const browserAlerts = useUIStore((state) => state.browserAlerts)
  const setRefreshInterval = useUIStore((state) => state.setRefreshInterval)
  const setEmailAlerts = useUIStore((state) => state.setEmailAlerts)
  const setBrowserAlerts = useUIStore((state) => state.setBrowserAlerts)
  const applyPreferences = useUIStore((state) => state.applyPreferences)
  const [saving, setSaving] = useState(false)
  const defaultPreferences = {
    refreshInterval: 15,
    emailAlerts: false,
    browserAlerts: true,
    darkMode: false,
  }

  useEffect(() => {
    // Hydrate saved settings from the backend so the settings page reflects the actual persisted project state.
    const loadSettings = async () => {
      try {
        const response = await settingsApi.get()
        applyPreferences(response.data)
      } catch (error) {
        toast.error(getErrorMessage(error) || 'Failed to load settings')
      }
    }

    loadSettings()
  }, [applyPreferences])

  const saveSettings = async () => {
    setSaving(true)
    try {
      await settingsApi.update({
        refreshInterval,
        emailAlerts,
        browserAlerts,
        theme: darkMode ? 'dark' : 'light',
        darkMode,
      })
      toast.success('Preferences saved')
    } catch (error) {
      toast.error(getErrorMessage(error) || 'Failed to save settings')
    } finally {
      setSaving(false)
    }
  }

  const resetSettings = async () => {
    setRefreshInterval(defaultPreferences.refreshInterval)
    setEmailAlerts(defaultPreferences.emailAlerts)
    setBrowserAlerts(defaultPreferences.browserAlerts)
    setDarkMode(defaultPreferences.darkMode)

    setSaving(true)
    try {
      await settingsApi.update({
        refreshInterval: defaultPreferences.refreshInterval,
        emailAlerts: defaultPreferences.emailAlerts,
        browserAlerts: defaultPreferences.browserAlerts,
        theme: 'light',
        darkMode: defaultPreferences.darkMode,
      })
      toast.success('Preferences reset')
    } catch (error) {
      toast.error(getErrorMessage(error) || 'Failed to reset settings')
    } finally {
      setSaving(false)
    }
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-4">
        <h1 className="text-3xl font-bold">Settings</h1>
        <Badge variant="secondary">Local preferences</Badge>
      </div>

      <div className="grid gap-6 lg:grid-cols-2">
        <Card className="p-8">
          <SectionTitle
            eyebrow="Display"
            title="Interface preferences"
            body="These settings are stored locally in the browser and affect only this device."
          />
          <div className="space-y-5">
            <ToggleRow
              label="Dark mode"
              description="Switch the interface between light and dark presentation."
              checked={!!darkMode}
              onChange={(checked) => setDarkMode(checked)}
            />
            <div className="space-y-2">
              <label className="text-sm font-medium">Dashboard refresh interval</label>
              <select
                value={String(refreshInterval)}
                onChange={(event) => setRefreshInterval(event.target.value)}
                className="w-full rounded-xl border border-input bg-background px-4 py-3 text-sm"
              >
                <option value="15">15 seconds</option>
                <option value="30">30 seconds</option>
                <option value="60">60 seconds</option>
              </select>
              <p className="text-xs text-muted-foreground">
                The dashboard uses this saved interval immediately, so changing it updates live polling behavior.
              </p>
            </div>
          </div>
        </Card>

        <Card className="p-8">
          <SectionTitle
            eyebrow="Notifications"
            title="Alert delivery"
            body="Choose how this local workstation should surface future root-cause alerts."
          />
          <div className="space-y-5">
            <ToggleRow
              label="Email alerts"
              description="Store your preferred email-delivery toggle so notification behavior can be expanded safely later."
              checked={emailAlerts}
              onChange={setEmailAlerts}
            />
            <ToggleRow
              label="Browser alerts"
              description="Keep local in-app alerts enabled for root-cause derived events."
              checked={browserAlerts}
              onChange={setBrowserAlerts}
            />
            <div className="rounded-2xl border border-border bg-muted/40 p-4 text-sm text-muted-foreground">
              Preferences are persisted in the browser and synced to the project settings collection for this local user.
            </div>
          </div>
        </Card>
      </div>

      <div className="flex gap-4 pt-2">
        <Button onClick={saveSettings} disabled={saving}>{saving ? 'Saving...' : 'Save changes'}</Button>
        <Button variant="outline" onClick={resetSettings} disabled={saving}>Reset defaults</Button>
      </div>
    </div>
  )
}

function ToggleRow({ label, description, checked, onChange }) {
  return (
    <label className="flex items-start justify-between gap-4 rounded-2xl border border-border p-4">
      <div>
        <p className="font-medium">{label}</p>
        <p className="mt-1 text-sm text-muted-foreground">{description}</p>
      </div>
      <input
        type="checkbox"
        checked={checked}
        onChange={(event) => onChange(event.target.checked)}
        className="mt-1 h-4 w-4"
      />
    </label>
  )
}
