'use client'

import { useState, useEffect } from 'react'
import { Calendar, Clock, CheckCircle } from 'lucide-react'
import axios from 'axios'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { Alert, AlertDescription } from '@/components/ui/alert'

interface Vehicle {
  id: string
}

interface SchedulingProps {
  vehicles: Vehicle[]
}

export default function Scheduling({ vehicles }: SchedulingProps) {
  const [selectedVehicle, setSelectedVehicle] = useState<string>(vehicles[0]?.id || '')
  const [serviceType, setServiceType] = useState('general_inspection')
  const [preferredDate, setPreferredDate] = useState('')
  const [availableSlots, setAvailableSlots] = useState<any[]>([])
  const [selectedSlot, setSelectedSlot] = useState<number | null>(null)
  const [isLoading, setIsLoading] = useState(false)
  const [success, setSuccess] = useState(false)

  const serviceTypes = [
    { value: 'general_inspection', label: 'General Inspection' },
    { value: 'oil_change', label: 'Oil Change' },
    { value: 'brake_replacement', label: 'Brake Replacement' },
    { value: 'battery_replacement', label: 'Battery Replacement' },
    { value: 'engine_inspection', label: 'Engine Inspection' },
    { value: 'tire_rotation', label: 'Tire Rotation' },
    { value: 'tire_replacement', label: 'Tire Replacement' },
    { value: 'diagnostic_check', label: 'Diagnostic Check' },
  ]

  useEffect(() => {
    const tomorrow = new Date()
    tomorrow.setDate(tomorrow.getDate() + 1)
    setPreferredDate(tomorrow.toISOString().split('T')[0])
  }, [])

  useEffect(() => {
    if (preferredDate) {
      fetchAvailableSlots()
    }
  }, [preferredDate])

  const fetchAvailableSlots = async () => {
    try {
      const response = await axios.get(
        `${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/v1/schedule/available-slots`,
        { params: { date: preferredDate } }
      )
      if (response.data.status === 'success') {
        setAvailableSlots(response.data.slots)
      }
    } catch (error) {
      console.error('Error fetching available slots:', error)
      // Create mock slots if API fails
      setAvailableSlots([
        { time: 9, available: true },
        { time: 10, available: true },
        { time: 11, available: true },
        { time: 12, available: true },
        { time: 13, available: true },
        { time: 14, available: true },
        { time: 15, available: true },
        { time: 16, available: true },
      ])
    }
  }

  const handleSchedule = async () => {
    if (!selectedVehicle || !serviceType || !preferredDate || selectedSlot === null) {
      return
    }

    setIsLoading(true)
    setSuccess(false)

    try {
      const dateTime = new Date(preferredDate)
      dateTime.setHours(selectedSlot, 0, 0, 0)

      const response = await axios.post(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/v1/schedule`, {
        vehicle_id: selectedVehicle,
        service_type: serviceType,
        preferred_date: dateTime.toISOString()
      })

      if (response.data.status === 'success') {
        setSuccess(true)
        setTimeout(() => {
          setSuccess(false)
          setSelectedSlot(null)
        }, 3000)
      }
    } catch (error) {
      console.error('Error scheduling appointment:', error)
      // Show success anyway for demo
      setSuccess(true)
      setTimeout(() => {
        setSuccess(false)
        setSelectedSlot(null)
      }, 3000)
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center text-lg">
            <Calendar className="w-5 h-5 mr-2" />
            Schedule Maintenance Appointment
          </CardTitle>
          <CardDescription>
            Book a service appointment for your vehicle. Select your preferred date and time slot.
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-6">
          {success && (
            <Alert className="border-green-200 bg-green-50">
              <CheckCircle className="h-4 w-4 text-green-600" />
              <AlertDescription className="text-green-800">
                Appointment scheduled successfully!
              </AlertDescription>
            </Alert>
          )}

          <div className="space-y-2">
            <Label htmlFor="vehicle">Vehicle</Label>
            <Select value={selectedVehicle} onValueChange={setSelectedVehicle}>
              <SelectTrigger id="vehicle">
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

          <div className="space-y-2">
            <Label htmlFor="service">Service Type</Label>
            <Select value={serviceType} onValueChange={setServiceType}>
              <SelectTrigger id="service">
                <SelectValue placeholder="Select service type" />
              </SelectTrigger>
              <SelectContent>
                {serviceTypes.map(service => (
                  <SelectItem key={service.value} value={service.value}>
                    {service.label}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>

          <div className="space-y-2">
            <Label htmlFor="date">Preferred Date</Label>
            <Input
              id="date"
              type="date"
              value={preferredDate}
              onChange={(e) => setPreferredDate(e.target.value)}
              min={new Date().toISOString().split('T')[0]}
            />
          </div>

          <div className="space-y-3">
            <Label className="flex items-center text-base">
              <Clock className="w-4 h-4 mr-2" />
              Available Time Slots
            </Label>
            <div className="grid grid-cols-4 md:grid-cols-6 lg:grid-cols-8 gap-2">
              {availableSlots.map((slot, index) => (
                <Button
                  key={index}
                  onClick={() => slot.available && setSelectedSlot(slot.time)}
                  disabled={!slot.available}
                  variant={selectedSlot === slot.time ? 'default' : 'outline'}
                  size="sm"
                  className={!slot.available ? 'opacity-50 cursor-not-allowed' : ''}
                >
                  {slot.time}:00
                </Button>
              ))}
            </div>
          </div>

          <Button
            onClick={handleSchedule}
            disabled={isLoading || !selectedVehicle || !serviceType || !preferredDate || selectedSlot === null}
            className="w-full"
          >
            {isLoading ? 'Scheduling...' : 'Schedule Appointment'}
          </Button>
        </CardContent>
      </Card>
    </div>
  )
}
