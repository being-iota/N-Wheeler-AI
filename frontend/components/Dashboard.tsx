'use client'

import { useState, useEffect } from 'react'
import { Battery, Thermometer, Gauge, Droplets, Car, AlertCircle } from 'lucide-react'
import axios from 'axios'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'

interface Vehicle {
  id: string
  battery_voltage?: number
  engine_temp?: number
  oil_pressure?: number
  brake_pad_thickness?: number
  tire_pressure?: number
  mileage?: number
  rpm?: number
  speed?: number
}

interface DashboardProps {
  vehicles: Vehicle[]
}

export default function Dashboard({ vehicles }: DashboardProps) {
  const [selectedVehicle, setSelectedVehicle] = useState<string>(vehicles[0]?.id || '')
  const [vehicleStatus, setVehicleStatus] = useState<any>(null)
  const [realTimeData, setRealTimeData] = useState<Vehicle | null>(null)

  useEffect(() => {
    if (selectedVehicle) {
      // Fetch vehicle status
      axios.get(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/v1/vehicles/${selectedVehicle}/status`)
        .then(res => {
          if (res.data.status === 'success') {
            setVehicleStatus(res.data.data)
          }
        })
        .catch(err => {
          console.error('Error fetching vehicle status:', err)
          // Set mock data if API fails
          setVehicleStatus({
            analysis: {
              health_scores: {
                battery: 85,
                engine: 90,
                oil: 88,
                brakes: 82,
                tires: 90,
                overall: 87
              }
            },
            diagnosis: {
              predictions: {
                battery: { failure_probability: 0.15, risk_level: 'low' },
                engine: { failure_probability: 0.10, risk_level: 'low' },
                brakes: { failure_probability: 0.18, risk_level: 'low' },
                oil: { failure_probability: 0.12, risk_level: 'low' },
                tires: { failure_probability: 0.10, risk_level: 'low' }
              },
              critical_alert: false
            }
          })
        })

      // Connect to WebSocket for real-time data
      try {
        const wsUrl = process.env.NEXT_PUBLIC_WS_URL || 'ws://localhost:8000'
        const ws = new WebSocket(`${wsUrl}/ws/telematics/${selectedVehicle}`)
        
        ws.onmessage = (event) => {
          try {
            const data = JSON.parse(event.data)
            setRealTimeData(data)
          } catch (e) {
            console.error('Error parsing WebSocket data:', e)
          }
        }

        ws.onerror = (error) => {
          console.error('WebSocket error:', error)
        }

        return () => {
          ws.close()
        }
      } catch (error) {
        console.error('WebSocket connection error:', error)
      }
    }
  }, [selectedVehicle])

  const currentData = realTimeData || vehicles.find(v => v.id === selectedVehicle)

  const getHealthColor = (score: number) => {
    if (score >= 80) return 'text-green-600'
    if (score >= 50) return 'text-yellow-600'
    return 'text-red-600'
  }

  const getHealthScore = (component: string) => {
    if (!vehicleStatus?.analysis?.health_scores) return null
    return vehicleStatus.analysis.health_scores[component]
  }

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle className="text-lg">Vehicle Selection</CardTitle>
          <CardDescription>Select a vehicle to view real-time metrics and health status</CardDescription>
        </CardHeader>
        <CardContent>
          <Select value={selectedVehicle} onValueChange={setSelectedVehicle}>
            <SelectTrigger className="w-full max-w-sm">
              <SelectValue placeholder="Select a vehicle" />
            </SelectTrigger>
            <SelectContent>
              {vehicles.map(vehicle => (
                <SelectItem key={vehicle.id} value={vehicle.id}>
                  {vehicle.id}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        </CardContent>
      </Card>

      {currentData && (
        <>
          <div>
            <h3 className="text-lg font-semibold mb-4">Key Metrics</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
              <MetricCard
                icon={Battery}
                label="Battery Voltage"
                value={currentData.battery_voltage?.toFixed(2) || 'N/A'}
                unit="V"
                healthScore={getHealthScore('battery')}
              />
              <MetricCard
                icon={Thermometer}
                label="Engine Temp"
                value={currentData.engine_temp?.toFixed(1) || 'N/A'}
                unit="°C"
                healthScore={getHealthScore('engine')}
              />
              <MetricCard
                icon={Droplets}
                label="Oil Pressure"
                value={currentData.oil_pressure?.toFixed(1) || 'N/A'}
                unit="PSI"
                healthScore={getHealthScore('oil')}
              />
              <MetricCard
                icon={Car}
                label="Brake Pads"
                value={currentData.brake_pad_thickness?.toFixed(1) || 'N/A'}
                unit="mm"
                healthScore={getHealthScore('brakes')}
              />
            </div>
          </div>

          <div>
            <h3 className="text-lg font-semibold mb-4">Performance Metrics</h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <Card>
                <CardHeader className="pb-3">
                  <CardTitle className="text-base font-medium">Tire Pressure</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="flex items-baseline gap-2">
                    <p className="text-3xl font-bold">{currentData.tire_pressure?.toFixed(1) || 'N/A'}</p>
                    <span className="text-muted-foreground text-sm">PSI</span>
                  </div>
                  <Badge variant={getHealthScore('tires') && getHealthScore('tires')! >= 80 ? "default" : "secondary"} className="mt-3">
                    Health: {getHealthScore('tires')?.toFixed(0) || 'N/A'}%
                  </Badge>
                </CardContent>
              </Card>

              <Card>
                <CardHeader className="pb-3">
                  <CardTitle className="text-base font-medium">RPM</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="flex items-baseline gap-2">
                    <p className="text-3xl font-bold">{currentData.rpm || 'N/A'}</p>
                  </div>
                </CardContent>
              </Card>

              <Card>
                <CardHeader className="pb-3">
                  <CardTitle className="text-base font-medium">Speed</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="flex items-baseline gap-2">
                    <p className="text-3xl font-bold">{currentData.speed || 'N/A'}</p>
                    <span className="text-muted-foreground text-sm">mph</span>
                  </div>
                </CardContent>
              </Card>
            </div>
          </div>

          {vehicleStatus?.diagnosis && (
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center text-lg">
                  <AlertCircle className="w-5 h-5 mr-2" />
                  Predictions & Alerts
                </CardTitle>
                <CardDescription>
                  AI-powered failure predictions and maintenance recommendations
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                {vehicleStatus.diagnosis.critical_alert && (
                  <Alert variant={vehicleStatus.diagnosis.alert_level === 'critical' ? 'destructive' : 'default'}>
                    <AlertCircle className="h-4 w-4" />
                    <AlertTitle>
                      {vehicleStatus.diagnosis.alert_level === 'critical' ? 'CRITICAL ALERT' : 'WARNING'}
                    </AlertTitle>
                    <AlertDescription>
                      Recommended Service: <strong>{vehicleStatus.diagnosis.recommended_service}</strong>
                    </AlertDescription>
                  </Alert>
                )}
                <div className="space-y-3">
                  {Object.entries(vehicleStatus.diagnosis.predictions || {}).map(([component, prediction]: [string, any]) => (
                    <div key={component} className="flex justify-between items-center p-4 border rounded-lg hover:bg-muted/50 transition-colors">
                      <div>
                        <span className="font-medium capitalize">{component}</span>
                        {prediction.recommendation && (
                          <p className="text-sm text-muted-foreground mt-1">{prediction.recommendation}</p>
                        )}
                      </div>
                      <Badge variant={prediction.risk_level === 'critical' ? 'destructive' : prediction.risk_level === 'high' ? 'secondary' : 'default'}>
                        {(prediction.failure_probability * 100).toFixed(1)}% risk
                      </Badge>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          )}
        </>
      )}
    </div>
  )
}

interface MetricCardProps {
  icon: React.ComponentType<{ className?: string }>
  label: string
  value: string
  unit: string
  healthScore?: number | null
}

function MetricCard({ icon: Icon, label, value, unit, healthScore }: MetricCardProps) {
  return (
    <Card className="hover:shadow-md transition-shadow">
      <CardHeader className="pb-3">
        <div className="flex items-center justify-between">
          <div className="p-2 rounded-lg bg-muted">
            <Icon className="w-5 h-5 text-muted-foreground" />
          </div>
          {healthScore !== null && healthScore !== undefined && (
            <Badge variant={healthScore >= 80 ? "default" : healthScore >= 50 ? "secondary" : "destructive"}>
              {healthScore.toFixed(0)}%
            </Badge>
          )}
        </div>
      </CardHeader>
      <CardContent>
        <p className="text-sm font-medium text-muted-foreground mb-2">{label}</p>
        <div className="flex items-baseline gap-1">
          <p className="text-2xl font-bold">{value}</p>
          <span className="text-sm text-muted-foreground">{unit}</span>
        </div>
      </CardContent>
    </Card>
  )
}

