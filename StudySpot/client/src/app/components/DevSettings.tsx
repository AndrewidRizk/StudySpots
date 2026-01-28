"use client";

import { useState, useEffect } from 'react';
import styles from './DevSettings.module.css';

interface Location {
    name: string;
    code: string;
    type: string;
    location: [number, number]; // [lng, lat]
}

interface DevSettingsProps {
    onLocationChange: (lat: number, lng: number) => void;
    onTimeChange: (date: Date) => void;
    onReset: () => void;
    isVisible?: boolean;
}

export default function DevSettings({ onLocationChange, onTimeChange, onReset, isVisible = true }: DevSettingsProps) {
    const [isOpen, setIsOpen] = useState(false);
    const [locations, setLocations] = useState<Location[]>([]);
    const [selectedLocation, setSelectedLocation] = useState<string>('');
    const [customLat, setCustomLat] = useState<string>('');
    const [customLng, setCustomLng] = useState<string>('');
    const [selectedDate, setSelectedDate] = useState<string>('');
    const [selectedTime, setSelectedTime] = useState<string>('');
    const [isLoading, setIsLoading] = useState(false);

    useEffect(() => {
        if (isOpen && locations.length === 0) {
            fetchLocations();
        }
    }, [isOpen]);

    const fetchLocations = async () => {
        setIsLoading(true);
        try {
            // Try local backend first
            let response = await fetch('http://localhost:5001/api/locations');
            
            // If local fails, try production
            if (!response.ok) {
                console.log('Local backend not available, trying production...');
                response = await fetch('https://studyspotsbackend.vercel.app/api/locations');
            }
            
            if (response.ok) {
                const data = await response.json();
                console.log('Locations fetched:', data);
                setLocations(data);
            } else {
                console.error('Failed to fetch locations, status:', response.status);
            }
        } catch (error) {
            console.error('Failed to fetch locations:', error);
        } finally {
            setIsLoading(false);
        }
    };

    const handleLocationSelect = (e: React.ChangeEvent<HTMLSelectElement>) => {
        const value = e.target.value;
        setSelectedLocation(value);
        
        if (value) {
            const location = locations.find(loc => 
                `${loc.name}${loc.code ? ` (${loc.code})` : ''}` === value
            );
            if (location) {
                setCustomLat(location.location[1].toString());
                setCustomLng(location.location[0].toString());
            }
        }
    };

    const handleApply = () => {
        const lat = parseFloat(customLat);
        const lng = parseFloat(customLng);
        
        if (!isNaN(lat) && !isNaN(lng)) {
            onLocationChange(lat, lng);
        }

        if (selectedDate && selectedTime) {
            const dateTime = new Date(`${selectedDate}T${selectedTime}`);
            onTimeChange(dateTime);
        }
    };

    const handleReset = () => {
        setSelectedLocation('');
        setCustomLat('');
        setCustomLng('');
        setSelectedDate('');
        setSelectedTime('');
        onReset();
    };

    const getCurrentDateTime = () => {
        const now = new Date();
        const date = now.toISOString().split('T')[0];
        const time = now.toTimeString().slice(0, 5);
        setSelectedDate(date);
        setSelectedTime(time);
    };

    return (
        <div className={styles.devSettings}>
            {isVisible && (
                <button 
                    className={styles.toggleButton}
                    onClick={() => setIsOpen(!isOpen)}
                >
                    🛠️ Dev Settings
                </button>
            )}

            {isOpen && (
                <div className={styles.panel}>
                    <div className={styles.header}>
                        <h3>Development Settings</h3>
                        <button 
                            className={styles.closeButton}
                            onClick={() => setIsOpen(false)}
                        >
                            ✕
                        </button>
                    </div>

                    <div className={styles.content}>
                        <div className={styles.section}>
                            <h4>📍 Location Override</h4>
                            
                            <div className={styles.field}>
                                <label>Select Building:</label>
                                <select 
                                    value={selectedLocation}
                                    onChange={handleLocationSelect}
                                    disabled={isLoading}
                                >
                                    <option value="">-- Choose a building --</option>
                                    {locations.map((loc, idx) => (
                                        <option 
                                            key={idx} 
                                            value={`${loc.name}${loc.code ? ` (${loc.code})` : ''}`}
                                        >
                                            {loc.name} {loc.code && `(${loc.code})`} - {loc.type}
                                        </option>
                                    ))}
                                </select>
                            </div>

                            <div className={styles.coordsRow}>
                                <div className={styles.field}>
                                    <label>Latitude:</label>
                                    <input 
                                        type="number" 
                                        step="0.000001"
                                        value={customLat}
                                        onChange={(e) => setCustomLat(e.target.value)}
                                        placeholder="43.772861"
                                    />
                                </div>
                                <div className={styles.field}>
                                    <label>Longitude:</label>
                                    <input 
                                        type="number" 
                                        step="0.000001"
                                        value={customLng}
                                        onChange={(e) => setCustomLng(e.target.value)}
                                        placeholder="-79.503471"
                                    />
                                </div>
                            </div>

                            <div className={styles.hint}>
                                💡 Tip: Select a building or manually adjust coordinates to fine-tune position
                            </div>
                        </div>

                        <div className={styles.section}>
                            <h4>🕐 Time & Date Override</h4>
                            
                            <div className={styles.field}>
                                <label>Date:</label>
                                <input 
                                    type="date" 
                                    value={selectedDate}
                                    onChange={(e) => setSelectedDate(e.target.value)}
                                />
                            </div>

                            <div className={styles.field}>
                                <label>Time:</label>
                                <input 
                                    type="time" 
                                    value={selectedTime}
                                    onChange={(e) => setSelectedTime(e.target.value)}
                                />
                            </div>

                            <button 
                                className={styles.nowButton}
                                onClick={getCurrentDateTime}
                            >
                                Set to Current Time
                            </button>
                        </div>

                        <div className={styles.actions}>
                            <button 
                                className={styles.applyButton}
                                onClick={handleApply}
                            >
                                Apply Settings
                            </button>
                            <button 
                                className={styles.resetButton}
                                onClick={handleReset}
                            >
                                Reset to Default
                            </button>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
}
