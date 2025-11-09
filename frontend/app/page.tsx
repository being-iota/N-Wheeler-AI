'use client'

import { useState, useEffect } from 'react'
import Dashboard from '@/components/Dashboard'
import Chatbot from '@/components/Chatbot'
import Scheduling from '@/components/Scheduling'
import AlertPanel from '@/components/AlertPanel'
import { Activity, MessageCircle, Calendar, AlertTriangle } from 'lucide-react'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'

export default function Home() {
  const [activeTab, setActiveTab] = useState('dashboard')
  const [vehicles, setVehicles] = useState<any[]>([])
  const [alerts, setAlerts] = useState<any[]>([])

  useEffect(() => {
    // Fetch vehicles
    fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/v1/vehicles`)
      .then(res => res.json())
      .then(data => {
        if (data.status === 'success') {
          setVehicles(Object.keys(data.vehicles).map(id => ({
            id,
            ...data.vehicles[id]
          })))
        } else {
          // Use mock vehicles if API fails
          setVehicles([
            { id: 'VEH001', battery_voltage: 12.6, engine_temp: 90, oil_pressure: 50, brake_pad_thickness: 8, tire_pressure: 32 },
            { id: 'VEH002', battery_voltage: 11.5, engine_temp: 95, oil_pressure: 45, brake_pad_thickness: 2.5, tire_pressure: 31 },
            { id: 'VEH003', battery_voltage: 12.8, engine_temp: 88, oil_pressure: 52, brake_pad_thickness: 10, tire_pressure: 32 }
          ])
        }
      })
      .catch(err => {
        console.error('Error fetching vehicles:', err)
        // Use mock vehicles if API fails
        setVehicles([
          { id: 'VEH001', battery_voltage: 12.6, engine_temp: 90, oil_pressure: 50, brake_pad_thickness: 8, tire_pressure: 32 },
          { id: 'VEH002', battery_voltage: 11.5, engine_temp: 95, oil_pressure: 45, brake_pad_thickness: 2.5, tire_pressure: 31 },
          { id: 'VEH003', battery_voltage: 12.8, engine_temp: 88, oil_pressure: 52, brake_pad_thickness: 10, tire_pressure: 32 }
        ])
      })
  }, [])

  const tabs = [
    { id: 'dashboard', label: 'Dashboard', icon: Activity },
    { id: 'chatbot', label: 'Chatbot', icon: MessageCircle },
    { id: 'scheduling', label: 'Scheduling', icon: Calendar },
    { id: 'alerts', label: 'Alerts', icon: AlertTriangle },
  ]

  return (
    <div className="min-h-screen bg-background">
      <header className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
        <div className="container flex h-16 items-center">
          <div className="mr-4 flex">
            <h1 className="text-xl font-bold tracking-tight">N-Wheeler AI</h1>
          </div>
          <div className="flex flex-1 items-center justify-between space-x-2 md:justify-end">
            <nav className="flex items-center space-x-6 text-sm font-medium">
              <span className="hidden md:block text-muted-foreground">Intelligent Vehicle Maintenance System</span>
            </nav>
          </div>
        </div>
      </header>

      <div className="container py-8">
        <div className="mb-8 space-y-2">
          <h2 className="text-3xl font-bold tracking-tight">Dashboard</h2>
          <p className="text-muted-foreground">
            Monitor your vehicle health and manage maintenance schedules
          </p>
        </div>
        
        <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
          <TabsList className="grid w-full max-w-2xl grid-cols-4 mb-6">
            {tabs.map(tab => {
              const Icon = tab.icon
              return (
                <TabsTrigger key={tab.id} value={tab.id} className="flex items-center gap-2">
                  <Icon className="w-4 h-4" />
                  <span>{tab.label}</span>
                </TabsTrigger>
              )
            })}
          </TabsList>
          <TabsContent value="dashboard" className="mt-0">
            <Dashboard vehicles={vehicles} />
          </TabsContent>
          <TabsContent value="chatbot" className="mt-0">
            <Chatbot />
          </TabsContent>
          <TabsContent value="scheduling" className="mt-0">
            <Scheduling vehicles={vehicles} />
          </TabsContent>
          <TabsContent value="alerts" className="mt-0">
            <AlertPanel vehicles={vehicles} />
          </TabsContent>
        </Tabs>
      </div>
    </div>
  )
}
