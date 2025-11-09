'use client'

import { useState, useEffect } from 'react'
import { AlertTriangle, Info, AlertCircle } from 'lucide-react'
import axios from 'axios'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { Label } from '@/components/ui/label'
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert'
import { Badge } from '@/components/ui/badge'

interface Vehicle {
  id: string
}

interface AlertPanelProps {
  vehicles: Vehicle[]
}

export default function AlertPanel({ vehicles }: AlertPanelProps) {
  const [selectedVehicle, setSelectedVehicle] = useState<string>(vehicles[0]?.id || '')
  const [alerts, setAlerts] = useState<any[]>([])
  const [vehicleStatus, setVehicleStatus] = useState<any>(null)

  useEffect(() => {
    if (selectedVehicle) {
      fetchAlerts()
      fetchVehicleStatus()
    }
  }, [selectedVehicle])

  const fetchAlerts = async () => {
    try {
      const response = await axios.get(
        `${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/v1/vehicles/${selectedVehicle}/alerts`
      )
      if (response.data.status === 'success') {
        setAlerts(response.data.alerts)
      }
    } catch (error) {
      console.error('Error fetching alerts:', error)
    }
  }

  const fetchVehicleStatus = async () => {
    try {
      const response = await axios.get(
        `${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/v1/vehicles/${selectedVehicle}/status`
      )
      if (response.data.status === 'success') {
        setVehicleStatus(response.data.data)
      }
    } catch (error) {
      console.error('Error fetching vehicle status:', error)
    }
  }

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center text-lg">
            <AlertTriangle className="w-5 h-5 mr-2" />
            Alerts & Notifications
          </CardTitle>
          <CardDescription>
            View real-time alerts, predictions, and maintenance recommendations for your vehicle
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-6">
          <div className="space-y-2">
            <Label htmlFor="alert-vehicle">Vehicle</Label>
            <Select value={selectedVehicle} onValueChange={setSelectedVehicle}>
              <SelectTrigger id="alert-vehicle">
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
          </div>

          {vehicleStatus?.diagnosis && vehicleStatus.diagnosis.critical_alert && (
            <Alert variant={vehicleStatus.diagnosis.alert_level === 'critical' ? 'destructive' : 'default'}>
              <AlertCircle className="h-4 w-4" />
              <AlertTitle>
                {vehicleStatus.diagnosis.alert_level === 'critical' ? 'CRITICAL ALERT' : 'WARNING'}
              </AlertTitle>
              <AlertDescription>
                Recommended Service: <strong>{vehicleStatus.diagnosis.recommended_service}</strong>
                {vehicleStatus.diagnosis.auto_schedule && (
                  <span className="block mt-2 text-sm">
                    Auto-scheduling has been initiated for this issue.
                  </span>
                )}
              </AlertDescription>
            </Alert>
          )}

          {vehicleStatus?.diagnosis?.predictions && (
            <div className="space-y-4">
              <h3 className="font-semibold text-lg">Failure Predictions</h3>
              <div className="space-y-3">
                {Object.entries(vehicleStatus.diagnosis.predictions).map(([component, prediction]: [string, any]) => (
                  <Card key={component} className={
                    prediction.risk_level === 'critical' ? 'border-destructive' :
                    prediction.risk_level === 'high' ? 'border-yellow-500' : ''
                  }>
                    <CardContent className="pt-4">
                      <div className="flex items-center justify-between">
                        <div className="flex-1">
                          <h4 className="font-semibold capitalize">{component}</h4>
                          <p className="text-sm text-muted-foreground mt-1">{prediction.recommendation}</p>
                        </div>
                        <div className="text-right ml-4">
                          <Badge variant={
                            prediction.risk_level === 'critical' ? 'destructive' :
                            prediction.risk_level === 'high' ? 'secondary' : 'default'
                          }>
                            {(prediction.failure_probability * 100).toFixed(1)}% risk
                          </Badge>
                          <p className="text-xs text-muted-foreground mt-1 capitalize">{prediction.risk_level}</p>
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </div>
            </div>
          )}

          {(!vehicleStatus?.diagnosis?.critical_alert && (!vehicleStatus?.diagnosis?.predictions || Object.keys(vehicleStatus.diagnosis.predictions).length === 0)) && (
            <Alert>
              <Info className="h-4 w-4" />
              <AlertTitle>No Alerts</AlertTitle>
              <AlertDescription>
                No alerts or predictions for this vehicle at this time.
              </AlertDescription>
            </Alert>
          )}
        </CardContent>
      </Card>
    </div>
  )
}
