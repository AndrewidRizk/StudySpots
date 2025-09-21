"use client";

import React, { useMemo } from "react";
import styles from "./RoomTimeline.module.css";

// Reuse the same Slot shape as page.tsx
export interface Slot {
  StartTime: string; // "HH:mm"
  EndTime: string;   // "HH:mm"
  Status?: string;
}

interface RoomTimelineProps {
  freeSlots: Slot[]; // Free/available intervals to render in green
  dayStart?: string; // default 08:30
  dayEnd?: string;   // default 22:30
  showLabels?: boolean; // show start/end labels under the bar
  showNowIndicator?: boolean; // vertical dashed line for current time
}

const DEFAULT_START = "08:30";
const DEFAULT_END = "22:30";

const toMinutes = (time: string) => {
  const [h, m] = time.split(":").map((n) => parseInt(n, 10));
  return h * 60 + m;
};

const clamp = (val: number, min: number, max: number) => Math.max(min, Math.min(max, val));

// Merge overlapping or touching intervals to clean input
const mergeIntervals = (intervals: [number, number][]) => {
  if (intervals.length === 0) return [] as [number, number][];
  const sorted = intervals
    .slice()
    .sort((a, b) => a[0] - b[0]);
  const merged: [number, number][] = [sorted[0]];
  for (let i = 1; i < sorted.length; i++) {
    const prev = merged[merged.length - 1];
    const cur = sorted[i];
    if (cur[0] <= prev[1]) {
      // overlap or touch
      prev[1] = Math.max(prev[1], cur[1]);
    } else {
      merged.push([cur[0], cur[1]]);
    }
  }
  return merged;
};

export default function RoomTimeline({
  freeSlots,
  dayStart = DEFAULT_START,
  dayEnd = DEFAULT_END,
  showLabels = true,
  showNowIndicator = true,
}: RoomTimelineProps) {
  const dayStartMin = toMinutes(dayStart);
  const dayEndMin = toMinutes(dayEnd);
  const daySpan = Math.max(1, dayEndMin - dayStartMin); // avoid division by zero

  // Normalize, clamp to day range, and merge free intervals
  const freeIntervals = useMemo(() => {
    const ints: [number, number][] = freeSlots
      .map((s) => [toMinutes(s.StartTime), toMinutes(s.EndTime)] as [number, number])
      .map(([s, e]) => [clamp(s, dayStartMin, dayEndMin), clamp(e, dayStartMin, dayEndMin)] as [number, number])
      .filter(([s, e]) => e > s); // drop zero/negative spans or fully outside
    return mergeIntervals(ints);
  }, [freeSlots, dayStartMin, dayEndMin]);

  // Compute busy as complement of free within day range
  const busyIntervals = useMemo(() => {
    const result: [number, number][] = [];
    let cursor = dayStartMin;
    for (const [fs, fe] of freeIntervals) {
      if (fs > cursor) result.push([cursor, fs]);
      cursor = Math.max(cursor, fe);
    }
    if (cursor < dayEndMin) result.push([cursor, dayEndMin]);
    return result;
  }, [freeIntervals, dayStartMin, dayEndMin]);

  // Now indicator position
  const now = new Date();
  const nowMinutes = now.getHours() * 60 + now.getMinutes();
  const nowPosPct = ((clamp(nowMinutes, dayStartMin, dayEndMin) - dayStartMin) / daySpan) * 100;
  const showNow = showNowIndicator && nowMinutes >= dayStartMin && nowMinutes <= dayEndMin;

  return (
    <div className={styles.wrapper}>
      <div className={styles.timeline}>
        {/* Busy segments (red, behind) */}
        {busyIntervals.map(([s, e], i) => {
          const left = ((s - dayStartMin) / daySpan) * 100;
          const width = ((e - s) / daySpan) * 100;
          return (
            <span
              key={`busy-${i}`}
              className={`${styles.segment} ${styles.busy}`}
              style={{ left: `${left}%`, width: `${width}%` }}
            />
          );
        })}
        {/* Free segments (green, on top) */}
        {freeIntervals.map(([s, e], i) => {
          const left = ((s - dayStartMin) / daySpan) * 100;
          const width = ((e - s) / daySpan) * 100;
          return (
            <span
              key={`free-${i}`}
              className={`${styles.segment} ${styles.free}`}
              style={{ left: `${left}%`, width: `${width}%` }}
            />
          );
        })}
        {/* Now indicator */}
        {showNow && (
          <span
            className={styles.now}
            style={{ left: `${nowPosPct}%` }}
            aria-hidden
          />
        )}
      </div>
      {showLabels && (
        <div className={styles.labels}>
          <span>{dayStart}</span>
          <span>{dayEnd}</span>
        </div>
      )}
    </div>
  );
}
